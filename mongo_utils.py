import pymongo
import pandas as pd
import joblib


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
    songs_features = data.drop(['_id'], axis=1)
    # Load KMeans model trained on Google Collab
    model = joblib.load('genres_clustering.pkl')
    genres = model.predict(songs_features)
    data_genre = data.copy()
    data_genre.insert(1, 'Genre', genres)
    print(genres.max())
    return data
