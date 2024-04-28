from fastapi import FastAPI
from predict import Evaluator
from typing import List
from pydantic import BaseModel

PROD_MODEL_PATH = '../models/prod_model.pkl'


class Body(BaseModel):
    inputs: List[List[float]]


app = FastAPI()


@app.post("/make_predictions/")
async def predict(body: Body):
    evaluator = Evaluator(PROD_MODEL_PATH)

    predictions = evaluator.predict(body.inputs)

    response = {
        'predictions': predictions
    }

    print(response)

    return response
