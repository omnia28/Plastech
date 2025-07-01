import pandas as pd
import numpy as np
import os
import joblib
def clean_data(data):


    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    preprocessor = joblib.load(os.path.join(BASE_DIR, 'predictions/models/preprocessing_pipeline_1.pkl'))

    df = pd.DataFrame([data])

    
    df.columns = [col.strip().lower() for col in df.columns]


    expected_columns = ['ph', 'temperature', 'turbidity_ntu', 'turbidity_voltage']

    
    df = df[expected_columns]

    df = df.astype(float)
    df = preprocessor.transform(df)
    print("✅ Preprocessed Data:\n", df)

    return df

def clean_data_reg(data):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    preprocessor = joblib.load(os.path.join(BASE_DIR, 'predictions/models/regression_preporcessor.pkl'))
    
    df = pd.DataFrame([data])

    
    df.columns = [col.strip().lower() for col in df.columns]


    expected_columns = ['ph', 'temperature', 'turbidity_ntu', 'turbidity_voltage']

    
    df = df[expected_columns]

    df = df.astype(float)
    df = preprocessor.transform(df)
    # print("✅ Preprocessed Data:\n", df)
    
    # values = [
    #     float(data['ph']),
    #     float(data['temperature']),
    #     float(data['turbidity_ntu']),
    #     float(data['turbidity_voltage'])
    # ]
    # X = np.array([values], dtype=np.float32)
    # result = preprocessor.predict(X)

    return df