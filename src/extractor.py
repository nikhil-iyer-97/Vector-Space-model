import sqlalchemy
import pandas as pd

df = pd.read_csv('data/dataset.csv')

engine = sqlalchemy.create_engine('sqlite:///data/data.db')
conn = engine.connect()
df.to_sql('song_lyrics', conn, index_label='song_id')