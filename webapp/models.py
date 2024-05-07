from django.db import models
from django.utils import timezone

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    firstUser = models.BooleanField(default=False)
    botAnswer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Conversation with {self.username}"

class Patient(models.Model):
    ID = models.AutoField(primary_key=True)
    Full_Name = models.CharField(max_length=100, null=True, blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    Ph_number = models.CharField(max_length=15, null=True, blank=True)  # Assuming phone number can be a string
    Aadhar_number = models.CharField(max_length=12, unique=True)
    Address = models.TextField(null=True, blank=True)
    STATE_CHOICES = [
        ('TN', 'Tamil Nadu'),
        ('KL', 'Kerala'),
        ('AP', 'Andhra Pradesh'),
        ('MH', 'Maharashtra'),
        ('DL', 'Delhi'),
        # Add more states as needed
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, null=True, blank=True)
    LANGUAGE_CHOICES = [
        ('TA', 'Tamil'),
        ('TE', 'Telugu'),
        ('ML', 'Malayalam'),
        ('HI', 'Hindi'),
        # Add more languages as needed
    ]
    Language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Patient: {self.Full_Name} (ID: {self.ID})"
