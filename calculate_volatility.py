# Importing necessary libraries
import pandas as pd
import numpy as np
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

def calculate_volatility(data):
    # Calculate Daily Returns
    data['Daily Returns'] = data['Close'].pct_change()

    # Calculate Daily Volatility
    daily_volatility = np.std(data['Daily Returns'].dropna())

    # Calculate Annualized Volatility
    annualized_volatility = daily_volatility * np.sqrt(len(data))

    return daily_volatility, annualized_volatility

@app.post("/calculate_volatility") 
async def calculate_volatility_endpoint(file: UploadFile = File(...)):
    # Read CSV file
    data = pd.read_csv(file.file)

    # Calculate Volatility
    daily_volatility, annualized_volatility = calculate_volatility(data)

    return {
        "Daily Volatility": daily_volatility,
        "Annualized Volatility": annualized_volatility
    }
