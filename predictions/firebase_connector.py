import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://microplastic-detection-default-rtdb.europe-west1.firebasedatabase.app/'
})

"""def get_realtime_data():
    ref = db.reference('/sensorData')
    return ref.get()"""

def get_all_readings(sensor_id):
    ref = db.reference(f'sensors/{sensor_id}/readings')
    return ref.get()

def get_realtime_data(sensor_id):
    ref = db.reference(f'sensors/{sensor_id}/readings/')
    return ref.get() or {}
