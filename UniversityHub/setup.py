#!/usr/bin/env python
"""
Complete setup script: migrate DB, create user, and test token auth.
Run from UniversityHub directory: python setup.py
"""
import os
import django
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniversityHub.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

print("\n" + "="*60)
print("🔧 DJANGO SETUP SCRIPT")
print("="*60)

# Step 1: Run migrations
print("\n1️⃣  Running migrations...")
try:
    from django.core.management import call_command
    call_command('migrate', verbosity=0)
    print("   ✅ Migrations completed")
except Exception as e:
    print(f"   ❌ Migration error: {e}")
    sys.exit(1)

# Step 2: Create user
print("\n2️⃣  Creating user 'user' with password 'user123'...")
try:
    user, created = User.objects.get_or_create(username='user')
    user.set_password('user123')
    user.email = 'user@example.com'
    user.save()
    
    # Create token for the user
    token, _ = Token.objects.get_or_create(user=user)
    
    if created:
        print(f"   ✅ User created: {user.username}")
    else:
        print(f"   ✅ User password updated: {user.username}")
    print(f"   📋 Token: {token.key}")
except Exception as e:
    print(f"   ❌ User creation error: {e}")
    sys.exit(1)

# Step 3: Test token auth endpoint
print("\n3️⃣  Testing token auth endpoint...")
try:
    import requests
    import json
    
    # Test with form-encoded data
    response = requests.post(
        'http://127.0.0.1:8000/api-token-auth/',
        data={'username': 'user', 'password': 'user123'}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Token auth works!")
        print(f"   📋 Token received: {data.get('token', 'N/A')[:20]}...")
    else:
        print(f"   ⚠️  Status {response.status_code}: {response.text}")
except Exception as e:
    print(f"   ⚠️  Could not test endpoint (Django server may not be running)")
    print(f"      Error: {e}")

print("\n" + "="*60)
print("✅ SETUP COMPLETE!")
print("="*60)
print("\n📝 Login credentials:")
print("   Username: user")
print("   Password: user123")
print("\n🌐 Login at: http://10.64.168.118:3001/login")
print("="*60 + "\n")
