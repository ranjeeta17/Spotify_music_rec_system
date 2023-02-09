from flask import Flask, request, jsonify, render_template, redirect, url_for,request 
from flask_table import Table,Col
import numpy as np
import pandas as pd

### Integrate HTML With Flask
### HTTP verb GET And POST

##Jinja2 template engine
dataset = pd.read_csv('./static/dataset.csv')

df = dataset.drop(columns=['id', 'name', 'artists', 'release_date', 'year'])
dataset['name'] = dataset['name'].str.lower()
class Spotify_Recommendation():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount=1):
        distance = []
        print(dataset.shape)
        songs = songs.lower()
        if songs in dataset['name'].values:
            song = self.dataset[(self.dataset.name.str.lower() == songs.lower())].head(1).values[0]
            rec = self.dataset[self.dataset.name.str.lower() != songs.lower()]
            for songs in rec.values:
                d = 0
                for col in np.arange(len(rec.columns)):
                    if not col in [1, 6, 12, 14, 18]:
                        d = d + np.absolute(float(song[col]) - float(songs[col]))
                distance.append(d)
            rec['distance'] = distance
            rec = rec.sort_values('distance')
            columns = ['artists', 'name']
            
            return rec[columns][:amount]
        else:
            return ['no song available']

  

app=Flask(__name__)

class ItemTable(Table):
    index = Col('index')
    artists = Col('artists')
    song = Col('song')


@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    list=[]
    if request.method=='POST':
        songs = str(request.form['song'])
        number = int(request.form['number'])
        if songs == "" or number == "":
            return redirect(request.url)
    recommendations = Spotify_Recommendation(dataset)
    s = recommendations.recommend(songs, number)
    if ('no song available' in s):
        return render_template('index.html',table=s)
    else:
        df = pd.DataFrame(s)
        for index,row in df.iterrows():
            list.append(dict(index = dataset.index[dataset['artists']== str(row["artists"])][0],artists = row["artists"],song=row["name"]))
        table = ItemTable(list)
        return render_template('index.html',table=table)

if __name__=='__main__':
    app.run(debug=True)
    


# Declare your table


# Populate the table
