from rest_framework import serializers
from .models import Dataset, Equipment
from django.contrib.auth.models import User

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment_items = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_type_distribution', 'data', 'equipment_items'
        ]
        read_only_fields = ['upload_date']


class DatasetSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer for history list"""
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'upload_date', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_type_distribution'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user