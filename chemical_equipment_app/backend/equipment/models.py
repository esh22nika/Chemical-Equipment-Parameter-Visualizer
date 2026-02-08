from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.

class Dataset(models.Model):
    # model to store uploaded datasets
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    # summary statistics
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    equipment_type_distribution = models.JSONField(default=dict)
    
    # store actual data as JSON for history
    data = models.JSONField(default=list)
    
    class Meta:
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"

class Equipment(models.Model):
    # model to store individual equipment records
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment_items')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"