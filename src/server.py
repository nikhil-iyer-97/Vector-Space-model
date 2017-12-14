from flask import Flask
from flask import render_template
from flask import request
from vectorspace import VectorSpaceModel
import string_processing
import sqlalchemy
import pandas
import time

app = Flask(__name__)

doc_limit = 500

@app.route('/')
def index():
	return render_template('index.html', process_time=process_time, 
		stats={'doc_count': stats[0], 'word_count': stats[1]})

@app.route('/search')
def search():
	query = request.args.get('query')
	size = request.args.get('size')
	query1 = string_processing.process_0(query)
	
	start_time = time.time()
	songs_info = getSongsInfo(m.getSimilarDocuments(query1, min(int(size), stats[0])))
	end_time = time.time()
	
	return render_template('search.html', query=query, size=size, 
		query_time=end_time - start_time, songs_info=songs_info)

@app.route('/song')
def song():
	size = request.args.get('size', '')
	query = request.args.get('query', '')

	song_id = request.args.get('song_id', '')
	song_info = getSong(song_id)
	song_info['lyrics'] = song_info['lyrics'].replace('\n', '<br>')
	song_info['song_id'] = song_id
	
	return render_template('song.html', song_info=song_info, query=query, size=size)
		
def getDocuments():
	""" List of tuples (song_id, lyrics)
	"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	pd = pandas.read_sql("select song_id,text from song_lyrics limit " + str(doc_limit),conn)
	l = [(pd.iloc[i,0], pd.iloc[i,1]) for i in pd.index]
	return l

def getSongsInfo(song_ids):
	""" List of tuples (song_id, song, artist)
	"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	l =[]
	for song_id in song_ids:
		pd = pandas.read_sql("select song_id, song, artist from song_lyrics where song_id = ?",conn, params=[song_id[1]])
		l.append((pd.iloc[0,0], pd.iloc[0,1], pd.iloc[0,2], -(100 * song_id[0]))) 
	return l

def getSong(song_id):
	"""
	{
		'song': ;
		'artist':;
		'text':;
	}"""
	engine = sqlalchemy.create_engine('sqlite:///../data/data.db')
	conn = engine.connect()
	pd = pandas.read_sql("select song, artist, text from song_lyrics where song_id = ?",conn, params=[song_id])
	d = {"song":pd.iloc[0,0], "artist":pd.iloc[0,1], "lyrics":pd.iloc[0,2]}
	return d

m = VectorSpaceModel()
d = getDocuments()
dc = []
for i in range(len(d)):
	dc.append((d[i][0], string_processing.process_0(d[i][1])))
start_time = time.time()
m.processDocuments(dc)

process_time = time.time() - start_time
stats = m.getStats()
print(m._VectorSpaceModel__sparsitycount)
print(stats[0]*stats[1])
with open("sparsetest.data","a") as f:
	f.write("\n{},{},{},{},".format(stats[0],stats[1],process_time,m._VectorSpaceModel__sparsitycount/(stats[0]*stats[1])))