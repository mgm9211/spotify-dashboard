import pymongo
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Connect with MongoDB Atlas to extract songs info
client = pymongo.MongoClient("mongodb+srv://g4s:g4s@cluster0.hadvx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
                             ssl=True, ssl_cert_reqs='CERT_NONE')
print('Connected')
# Select database in cluster
db = client['G4S-Spotify']
# Select collection
collection = db['songs']
# Get all songs Features and ID
pipeline = [{
    '$project': {
        'Acousticness': '$Features.Acousticness',
        'Danceability': '$Features.Danceability',
        'Energy': '$Features.Energy',
        'Instrumentalness': '$Features.Instrumentalness',
        'Liveness': '$Features.Liveness',
        'Loudness': '$Features.Loudness',
        'Speechiness': '$Features.Speechiness',
        'Tempo': '$Features.Tempo',
        'Valence': '$Features.Tempo'
    }
}]
cursor = collection.aggregate(pipeline=pipeline)

# Create Dataframe structure to save songs info
data = pd.DataFrame(list(cursor))
data.to_csv('songs.csv', index=False)
print(data.describe())
