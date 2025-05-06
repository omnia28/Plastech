from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=255)
    work_email_address = models.EmailField()
    phone_number = models.CharField(max_length=20)
    details = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.first_name} {self.last_name} ({self.company})"