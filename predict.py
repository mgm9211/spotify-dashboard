import joblib

model = joblib.load('genres_clustering.pkl')


def predict(features):
    return model.predict(features)
