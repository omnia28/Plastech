from django.db import models

class SensorReading(models.Model):
    sensor_id = models.CharField(max_length=100, default='sensor_id_1')
    unique_sensor_id = models.CharField(max_length=100, null=True)
    temperature = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    turbidity_ntu = models.FloatField(null=True, blank=True)
    turbidity_voltage = models.FloatField(null=True, blank=True)
    presence = models.BooleanField()
    source = models.CharField(max_length=50, default='manual')
    regression_result = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor_id} - {self.timestamp}"
