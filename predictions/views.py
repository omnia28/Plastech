from django.shortcuts import render, redirect
from .firebase_connector import get_realtime_data
from .preprocessing import clean_data, clean_data_reg
from .firebase_connector import get_all_readings
from django.contrib import messages
from orders.models import AssignedProduct
from .models import SensorReading
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
regression_model = joblib.load(os.path.join(BASE_DIR, 'predictions/models/deep_learning_regression_model.pkl'))
classification_model = joblib.load(os.path.join(BASE_DIR, 'predictions/models/classification_model_1.pkl'))

def select_sensor(request):
    if request.method == 'POST':
        sensor_id = request.POST.get('sensor_id')
        input_type = request.POST.get('input_type')

        assigned = AssignedProduct.objects.filter(
            unique_product_id=sensor_id,
            order_item__order__user=request.user
        ).first()

        if assigned:
            request.session['sensor_id'] = assigned.actual_product_id
            request.session['unique_id'] = assigned.unique_product_id
            request.session['input_type'] = input_type
            
            if input_type == 'manual':
                request.session['manual_data'] = {
                    'pH': request.POST.get('pH'),
                    'temperature': request.POST.get('temperature'),
                    'turbidity_NTU': request.POST.get('turbidity_NTU'),
                    'turbidity_Voltage': request.POST.get('turbidity_Voltage')
                } 
            return redirect('dashboard')
        else:
            messages.error(request, "You're not authorized to access this sensor's data")
            return redirect('select_sensor')

    return render(request, 'select_sensor.html')


def sensor_history(request):
    sensor_id = request.GET.get('sensor_id') or request.session.get('sensor_id')
    readings = []

    if sensor_id:
        raw_data = get_all_readings(sensor_id)
        if raw_data:
            for _, values in sorted(raw_data.items()):
                data = {k.strip(): v for k, v in values.items()}
                
                exists = SensorReading.objects.filter(
                    sensor_id=sensor_id,
                    temperature=data.get("temperature"),
                    ph=data.get("ph"),
                    turbidity_ntu=data.get("turbidity_ntu"),
                    turbidity_voltage=data.get("turbidity_voltage")
                ).exists()

                if not exists:
                    X = clean_data(data)
                    classification_result = classification_model.predict(X)[0]
                    if classification_result == 1:
                        X = clean_data_reg(data)
                        regression_result = regression_model.predict(X)[0]
                    else:
                        regression_result = 0

                    SensorReading.objects.create(
                        sensor_id=sensor_id,
                        source='firebase',
                        temperature=data.get("temperature"),
                        ph=data.get("ph"),
                        turbidity_ntu=data.get("turbidity_ntu"),
                        turbidity_voltage=data.get("turbidity_voltage"),
                        presence=(classification_result == 1),
                        regression_result=str(regression_result)
                    )
                else:
                    existing = SensorReading.objects.filter(
                        sensor_id=sensor_id,
                        temperature=data.get("temperature"),
                        ph=data.get("ph"),
                        turbidity_ntu=data.get("turbidity_ntu"),
                        turbidity_voltage=data.get("turbidity_voltage")
                    ).first()
                    regression_result = existing.regression_result if existing else 'N/A'
                    classification_result = existing.presence if existing else False

                readings.append({
                    'source': 'firebase',
                    'temperature': data.get("temperature"),
                    'ph': data.get("ph"),
                    'turbidity_ntu': data.get("turbidity_ntu"),
                    'turbidity_voltage': data.get("turbidity_voltage"),
                    'presence': classification_result,
                    'regression_result': regression_result
                })

        db_readings = SensorReading.objects.filter(sensor_id=sensor_id, source='manual').order_by('-timestamp')
        for item in db_readings:
            readings.append({
                'source': 'manual',
                'temperature': item.temperature,
                'ph': item.ph,
                'turbidity_ntu': item.turbidity_ntu,
                'turbidity_voltage': item.turbidity_voltage,
                'presence': item.presence,
                'regression_result': item.regression_result
            })

    return render(request, 'predictions/history.html', {
        'sensor_id': sensor_id,
        'readings': readings
    })



def dashboard(request):
    classification_result = regression_result = 'No data available'
    raw_data = {}
    show_form = False

    sensor_id = request.session.get('sensor_id')
    input_type = request.session.get('input_type')

    if not sensor_id:
        return redirect('select_sensor')

    if input_type == "manual":
        if request.method == "POST":
            try:
                manual_data = {
                    "ph": float(request.POST.get("pH")),
                    "temperature": float(request.POST.get("temperature")),
                    "turbidity_ntu": float(request.POST.get("turbidity_NTU")),
                    "turbidity_voltage": float(request.POST.get("turbidity_Voltage")),
                }
                raw_data = manual_data
                X = clean_data(manual_data)

                classification_result = classification_model.predict(X)[0]
                if classification_result == 1:
                    X = clean_data_reg(manual_data)
                    regression_result = regression_model.predict(X)[0]
                else:
                    regression_result = 0

                exists = SensorReading.objects.filter(
                    sensor_id=sensor_id,
                    temperature=manual_data["temperature"],
                    ph=manual_data["ph"],
                    turbidity_ntu=manual_data["turbidity_ntu"],
                    turbidity_voltage=manual_data["turbidity_voltage"],
                    source='manual'
                ).exists()

                if not exists:
                    SensorReading.objects.create(
                        sensor_id=sensor_id,
                        source='manual',
                        temperature=manual_data["temperature"],
                        ph=manual_data["ph"],
                        turbidity_ntu=manual_data["turbidity_ntu"],
                        turbidity_voltage=manual_data["turbidity_voltage"],
                        presence=(classification_result == 1),
                        regression_result=str(regression_result)
                    )
            except Exception as e:
                classification_result = regression_result = f"Manual input error: {e}"
        else:
            show_form = True

    elif input_type == "firebase":
        raw_data = get_all_readings(sensor_id)
        if raw_data:
            try:
                latest_key = sorted(raw_data.keys())[-1]
                latest_data = raw_data[latest_key]
                # raw_data = latest_data

                X = clean_data(latest_data)

                classification_result = classification_model.predict(X)[0]
                if classification_result == 1:
                    X = clean_data_reg(latest_data)
                    regression_result = regression_model.predict(X)[0]
                else:
                    regression_result = 0

                exists = SensorReading.objects.filter(
                    sensor_id=sensor_id,
                    temperature=latest_data["temperature"],
                    ph=latest_data["ph"],
                    turbidity_ntu=latest_data["turbidity_ntu"],
                    turbidity_voltage=latest_data["turbidity_voltage"],
                    source='firebase'
                ).exists()

                if not exists:
                    SensorReading.objects.create(
                        sensor_id=sensor_id,
                        source='firebase',
                        temperature=latest_data["temperature"],
                        ph=latest_data["ph"],
                        turbidity_ntu=latest_data["turbidity_ntu"],
                        turbidity_voltage=latest_data["turbidity_voltage"],
                        presence=(classification_result == 1),
                        regression_result=str(regression_result)
                    )

                latest_reading = SensorReading.objects.filter(
                    sensor_id=sensor_id,
                    source='firebase'
                ).latest('timestamp')

                raw_data = {
                    'ph': latest_reading.ph,
                    'temperature': latest_reading.temperature,
                    'turbidity_ntu': latest_reading.turbidity_ntu,
                    'turbidity_voltage': latest_reading.turbidity_voltage
                }
                classification_result = "Yes" if latest_reading.presence else "No"
                regression_result = latest_reading.regression_result
                

            except Exception as e:
                classification_result = regression_result = f"Firebase error: {e}"
        else:
            classification_result = regression_result = 'No Firebase data found'

    context = {
        'raw': raw_data,
        'classification': classification_result,
        'regression': regression_result,
        'sensor_id': sensor_id,
        'input_type': input_type,
        'show_form': show_form,
    }

    return render(request, 'predictions/results.html', context)
