from joblib import load

clf_model = load('predictions/models/classification_model_1.pkl')
reg_model = load('predictions/models/regression_model_1.pkl')

def make_predictions(df):
    classification_result = clf_model.predict(df)
    regression_result = reg_model.predict(df)

    return classification_result[0], regression_result[0]  # or however you display them
