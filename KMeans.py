import pymongo


client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.hadvx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
print('Connected')
db = client['G4S-Spotify']
print(db)
collection = db['songs']
for c in collection.find():
    print(c)
