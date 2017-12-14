# Vector-Space-model

This is a domain specific search engine where a user can enter song lyrics and a list of songs is displayed 
along with their accuracy. Clicking the song results in the song lyrics being displayed. 

The dataset contains song lyics and its corresponding artist.NLTK preprocessing techniques such as stemming
and stop words removal have been utilized to convert the dataset into bag of words model and apply TF-IDF score
to get accurate results for the user query. Vector space model has been deployed to match the query with the
documents for maximum accuracy.

File structure:
---------------
-data folder – data that builds the model
-src/vectorspacemodel.py – The implementation of the vectorspace model
-src/stringprocessing.py – The various pre-processing functions using NLTK
-src/server.py – The file to run to start the program with the web-ui

Usage:
------
- Download/Clone this repository
- Change working directory to the where the repository is located
- Install dependencies:
	```
	pip install -r requirements.txt
	```
- Change working directory to `src`:
	```
	cd src
	```
- Start the server:
	```
	export FLASK_APP="server.py"
	flask run
	```
- Navigate to `http://localhost:5000`

Link to actual dataset:
-----------------------
https://www.kaggle.com/mousehead/songlyrics
