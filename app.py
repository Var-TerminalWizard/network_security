import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL") or os.getenv("MONGODB_URL_KEY")
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FINAL_MODEL_DIR = os.path.join(BASE_DIR, "final_model")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request,file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file)
        if "Result" in df.columns:
            df = df.drop(columns=["Result"])

        preprocessor_path = os.path.join(FINAL_MODEL_DIR, "preprocessor.pkl")
        model_path = os.path.join(FINAL_MODEL_DIR, "model.pkl")
        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"Missing preprocessor file: {preprocessor_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Missing model file: {model_path}")

        preprocesor=load_object(preprocessor_path)
        final_model=load_object(model_path)
        expected_features = getattr(preprocesor, "feature_names_in_", None)
        if expected_features is not None:
            df = df.reindex(columns=list(expected_features))

        network_model = NetworkModel(preprocessor=preprocesor,model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        output_dir = os.path.join(BASE_DIR, "prediction_output")
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(os.path.join(output_dir, "output.csv"), index=False)
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse(request=request, name="table.html", context={"table": table_html})
        
    except Exception as e:
            logging.exception("Prediction failed")
            raise NetworkSecurityException(e,sys)

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
