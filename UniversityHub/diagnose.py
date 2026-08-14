#!/usr/bin/env python
"""
Diagnostic script: Check Django setup, migrations, and token endpoint
Run from UniversityHub: python diagnose.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UniversityHub.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests

print("\n" + "="*70)
print("🔍 DJANGO DIAGNOSTICS")
print("="*70)

# 1. Check migrations
print("\n1️⃣  Checking migrations...")
try:
    from django.core.management import call_command
    from io import StringIO
    output = StringIO()
    call_command('showmigrations', verbosity=0, stdout=output)
    print("   ✅ Migrations appear OK")
except Exception as e:
    print(f"   ❌ Migration check failed: {e}")

# 2. Check users
print("\n2️⃣  Checking users...")
users = User.objects.all()
if users.exists():
    print(f"   ✅ Found {users.count()} user(s):")
    for u in users:
        has_token = Token.objects.filter(user=u).exists()
        token_status = "✅ Has token" if has_token else "⚠️ No token"
        print(f"      - {u.username} ({token_status})")
else:
    print("   ❌ No users found! Run setup.py to create users.")

# 3. Check token auth setting
print("\n3️⃣  Checking DRF settings...")
from django.conf import settings
auth_classes = settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])
if auth_classes:
    print(f"   ✅ Authentication classes configured:")
    for cls in auth_classes:
        print(f"      - {cls}")
else:
    print("   ⚠️  No default authentication configured")

# 4. Test token endpoint
print("\n4️⃣  Testing token endpoint...")
try:
    # First ensure user exists
    user, _ = User.objects.get_or_create(username='user')
    user.set_password('user123')
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    print(f"   ✅ User 'user' ready with token")
    
    # Test endpoint
    resp = requests.post(
        'http://127.0.0.1:8000/api-token-auth/',
        data={'username': 'user', 'password': 'user123'},
        timeout=3
    )
    if resp.status_code == 200:
        data = resp.json()
        print(f"   ✅ Token endpoint works!")
        print(f"      Token: {data.get('token', 'N/A')[:30]}...")
    else:
        print(f"   ❌ Token endpoint error: {resp.status_code}")
        print(f"      Response: {resp.text[:200]}")
except requests.exceptions.ConnectionError:
    print("   ⚠️  Django server not reachable at http://127.0.0.1:8000")
    print("      Make sure Django is running: python manage.py runserver 0.0.0.0:8000")
except Exception as e:
    print(f"   ❌ Error: {e}")

# 5. Summary
print("\n" + "="*70)
print("✅ DIAGNOSTICS COMPLETE")
print("="*70)
print("\n📝 Next steps:")
print("   1. Make sure Django is running: python manage.py runserver 0.0.0.0:8000")
print("   2. Check browser console (F12) for detailed error messages")
print("   3. Try logging in with username='user' password='user123'")
print("="*70 + "\n")
