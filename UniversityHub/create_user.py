#!/usr/bin/env python
"""
Script to create a Django user for login.
Run this from the UniversityHub directory: python create_user.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniversityHub.settings')
django.setup()

from django.contrib.auth.models import User

# Delete existing user if exists
User.objects.filter(username='user').delete()

# Create new user
user = User.objects.create_user(
    username='user',
    email='user@example.com',
    password='user123'
)

print(f"✅ User created successfully!")
print(f"   Username: {user.username}")
print(f"   Email: {user.email}")
print(f"   Password: user123")
