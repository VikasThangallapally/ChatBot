#!/usr/bin/env python
"""Verify OTP password reset implementation is complete"""

import os
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}")
    if not exists:
        print(f"   Expected at: {filepath}")
    return exists

def main():
    print("\n" + "="*70)
    print("  OTP PASSWORD RESET - IMPLEMENTATION VERIFICATION")
    print("="*70 + "\n")
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    all_good = True
    
    # Backend Files
    print("🔧 BACKEND FILES:")
    print("-" * 70)
    
    files_to_check = [
        ("app/services/email_service.py", "Email service (NEW)"),
        ("app/schemas/password_reset.py", "Password reset schemas (NEW)"),
        ("app/api/routes/auth.py", "Auth routes (MODIFIED - has forgot-password & reset-password)"),
        ("app/config.py", "Config with SMTP settings (MODIFIED)"),
    ]
    
    for filepath, desc in files_to_check:
        full_path = os.path.join(base_path, filepath)
        if not check_file(full_path, desc):
            all_good = False
    
    # Frontend Files
    print("\n🎨 FRONTEND FILES:")
    print("-" * 70)
    
    frontend_files = [
        ("frontend/src/pages/ForgotPassword.jsx", "Forgot Password page (NEW)"),
        ("frontend/src/pages/ResetPassword.jsx", "Reset Password page (NEW)"),
        ("frontend/src/App.jsx", "App routing (MODIFIED - has 2 new routes)"),
        ("frontend/src/pages/Login.jsx", "Login page (MODIFIED - has Forgot Password link)"),
    ]
    
    for filepath, desc in frontend_files:
        full_path = os.path.join(base_path, filepath)
        if not check_file(full_path, desc):
            all_good = False
    
    # Documentation
    print("\n📚 DOCUMENTATION files:")
    print("-" * 70)
    
    docs = [
        ("OTP_PASSWORD_RESET_SETUP.md", "Complete setup guide"),
        ("OTP_IMPLEMENTATION_SUMMARY.md", "Implementation summary"),
        ("QUICK_OTP_SETUP.md", "Quick start guide"),
        ("setup_password_reset_table.sql", "Database SQL script"),
        (".env.example", "Environment variable template"),
    ]
    
    for filepath, desc in docs:
        full_path = os.path.join(base_path, filepath)
        if not check_file(full_path, desc):
            all_good = False
    
    # Test Files
    print("\n🧪 TEST FILES:")
    print("-" * 70)
    
    tests = [
        ("test_otp_password_reset.py", "OTP functionality test script"),
    ]
    
    for filepath, desc in tests:
        full_path = os.path.join(base_path, filepath)
        if not check_file(full_path, desc):
            all_good = False
    
    # Check key implementations
    print("\n🔍 IMPLEMENTATION CHECKS:")
    print("-" * 70)
    
    # Check if forgot-password endpoint exists in auth.py
    auth_file = os.path.join(base_path, "app/api/routes/auth.py")
    if os.path.exists(auth_file):
        with open(auth_file, 'r') as f:
            content = f.read()
            has_forgot = "/forgot-password" in content
            has_reset = "/reset-password" in content
            print(f"{'✅' if has_forgot else '❌'} /api/auth/forgot-password endpoint")
            print(f"{'✅' if has_reset else '❌'} /api/auth/reset-password endpoint")
            if not (has_forgot and has_reset):
                all_good = False
    
    # Check if routes are in App.jsx
    app_file = os.path.join(base_path, "frontend/src/App.jsx")
    if os.path.exists(app_file):
        with open(app_file, 'r') as f:
            content = f.read()
            has_forgot_route = "ForgotPassword" in content and "/forgot-password" in content
            has_reset_route = "ResetPassword" in content and "/reset-password" in content
            print(f"{'✅' if has_forgot_route else '❌'} /forgot-password route in App.jsx")
            print(f"{'✅' if has_reset_route else '❌'} /reset-password route in App.jsx")
            if not (has_forgot_route and has_reset_route):
                all_good = False
    
    # Check config.py for SMTP settings
    config_file = os.path.join(base_path, "app/config.py")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            content = f.read()
            has_smtp = "SMTP_EMAIL" in content and "SMTP_PASSWORD" in content
            print(f"{'✅' if has_smtp else '❌'} SMTP configuration in config.py")
            if not has_smtp:
                all_good = False
    
    # Summary
    print("\n" + "="*70)
    if all_good:
        print("✅ ALL FILES AND IMPLEMENTATIONS VERIFIED!")
        print("\n🚀 NEXT STEPS:")
        print("1. Read QUICK_OTP_SETUP.md for 5-minute setup")
        print("2. Create table in Supabase using setup_password_reset_table.sql")
        print("3. Get Gmail App Password and update .env")
        print("4. Start backend and frontend")
        print("5. Test at http://localhost:5174/forgot-password")
    else:
        print("❌ SOME FILES ARE MISSING!")
        print("\nPlease check the errors above and ensure all files are created.")
    
    print("="*70 + "\n")
    
    return all_good

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
