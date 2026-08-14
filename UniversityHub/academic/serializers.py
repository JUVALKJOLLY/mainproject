from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'


class courseSerializer(serializers.ModelSerializer):
    class Meta:
        model= Course
        fields= ['id','name','code','credits','department','semester','syllabus']

class studentserializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['id','first_name','last_name','email','courses','profile_picture','enrollment_date']

