import joblib
import gzip

model = joblib.load("fifa_value_model.pkl")

with gzip.open("fifa_value_model_compressed.pkl.gz", "wb") as f:
    joblib.dump(model, f, compress=("gzip", 3))