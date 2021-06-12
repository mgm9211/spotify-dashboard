import pymongo
import pandas as pd
import joblib
from predict import predict


def load_features_time_series():
    # Connect with MongoDB Atlas to extract songs info
    client = pymongo.MongoClient(
        "mongodb+srv://g4s:g4s@cluster0.hadvx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
        ssl=True, ssl_cert_reqs='CERT_NONE')
    print('Connected')
    # Select database in cluster
    db = client['G4S-Spotify']
    # Select collection
    collection = db['songs']
    # Get all songs Features and ID
    pipeline = [{
        '$project': {
            'Date': '$ReleaseDate',
            'Popularity': '$Popularity',
            'Title': '$Title',
            'Artist(s)': '$Artists',
            'Acousticness': '$Features.Acousticness',
            'Danceability': '$Features.Danceability',
            'Energy': '$Features.Energy',
            'Instrumentalness': '$Features.Instrumentalness',
            'Liveness': '$Features.Liveness',
            'Loudness': '$Features.Loudness',
            'Speechiness': '$Features.Speechiness',
            'Tempo': '$Features.Tempo',
            'Valence': '$Features.Valence'
        }
    }]
    cursor = collection.aggregate(pipeline=pipeline)

    # Create Dataframe structure to save songs info
    data = pd.DataFrame(list(cursor))
    data_to_predict = data.drop(['_id', 'Popularity', 'Title', 'Artist(s)', 'Date'], axis=1)
    songs_features = data.drop(['_id', 'Popularity', 'Title', 'Artist(s)'], axis=1)
    genres = predict(data_to_predict)
    data_genre = data.copy()
    data_genre.insert(1, 'Genre', genres)
    songs_features.to_csv('songs_features.csv', index=False)
    data_genre.to_csv('data_genre.csv', index=False)
    return songs_features, data_genre
