# OTP-Based Password Reset Setup Guide

## Overview
This guide walks you through setting up OTP-based password reset for your Brain Tumor MRI Analyzer application with Supabase and Gmail SMTP.

**Features:**
- ✅ 6-digit OTP generation and email delivery
- ✅ 10-minute OTP expiration
- ✅ Secure password hashing with bcrypt
- ✅ React UI for forgot password and reset password flows
- ✅ Full backend validation and error handling

---

## Step 1: Set Up Supabase Table

### 1.1 Create the `password_reset_otps` Table

Go to your Supabase project:
1. Navigate to **SQL Editor**
2. Create a new query
3. Copy and paste the SQL from `setup_password_reset_table.sql`:

```sql
CREATE TABLE IF NOT EXISTS public.password_reset_otps (
  id BIGSERIAL PRIMARY KEY,
  user_email TEXT NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
  otp_code VARCHAR(6) NOT NULL,
  is_used BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  UNIQUE(user_email, is_used)
);

CREATE INDEX IF NOT EXISTS idx_otp_email ON public.password_reset_otps(user_email);
CREATE INDEX IF NOT EXISTS idx_otp_unused ON public.password_reset_otps(user_email, is_used);

ALTER TABLE public.password_reset_otps DISABLE ROW LEVEL SECURITY;
```

4. Click **Run**
5. Verify success (should see "Success" message)

---

## Step 2: Configure Gmail SMTP

### 2.1 Get Gmail App Password

Gmail no longer allows direct password login from third-party apps. You need an **App Password**:

1. Go to https://myaccount.google.com/apppasswords
2. You may need to enable 2-Factor Authentication first (if not already enabled)
3. Select:
   - **App:** Mail
   - **Device:** Windows Computer (or your device)
4. Click **Generate**
5. Copy the 16-character password (ignore spaces)
6. Save this for Step 3

### 2.2 Alternative: Use Your Email Provider

If not using Gmail, get your SMTP credentials:
- **Gmail:** `smtp.gmail.com` port 465 (SSL)
- **Outlook:** `smtp-mail.outlook.com` port 587 (TLS)
- **Yahoo:** `smtp.mail.yahoo.com` port 465/587
- **Custom:** Contact your email provider

---

## Step 3: Update Environment Variables

### 3.1 Update Your `.env` File

Located at the project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_service_role_secret_key

# JWT Configuration
SECRET_KEY=ae9d1e30-5bf2-423a-954c-13c8c759452a
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# SMTP Configuration for Password Reset Emails
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your_16_char_app_password_no_spaces

# Other settings...
```

**Important:** Never commit these credentials to Git. Add `.env` to `.gitignore`:

```
.env
.env.local
```

---

## Step 4: Verify Backend Implementation

### 4.1 Check Backend Files

Verify these files exist and are properly configured:

```
app/
├── core/
│   └── auth.py                  # Updated with password reset logic
├── api/
│   └── routes/
│       └── auth.py              # New endpoints: /forgot-password, /reset-password
├── services/
│   └── email_service.py         # NEW: Email sending utility
├── schemas/
│   └── password_reset.py        # NEW: Request/response schemas
└── config.py                    # UPDATED: Added SMTP settings
```

### 4.2 Backend Endpoints

**POST `/api/auth/forgot-password`**
- Request: `{ "email": "user@example.com" }`
- Response: `{ "message": "...", "status": "success" }`
- Generates OTP and sends via email

**POST `/api/auth/reset-password`**
- Request: `{ "email": "user@example.com", "otp_code": "123456", "new_password": "..." }`
- Response: `{ "message": "Password reset successfully", "status": "success" }`
- Validates OTP and updates password

---

## Step 5: Verify Frontend Implementation

### 5.1 Check Frontend Files

Verify these files exist:

```
frontend/src/
├── pages/
│   ├── Login.jsx                # UPDATED: Added "Forgot Password?" link
│   ├── Register.jsx             # Unchanged
│   ├── ForgotPassword.jsx       # NEW: OTP request page
│   └── ResetPassword.jsx        # NEW: Password reset page
└── App.jsx                      # UPDATED: Added new routes
```

### 5.2 Frontend Routes

```
/login              → Login page
/register           → Register page
/forgot-password    → Request OTP
/reset-password     → Reset password with OTP
```

---

## Step 6: Testing

### Test Flow 1: Successful Password Reset

1. **Start both servers:**
   ```bash
   # Terminal 1: Backend
   cd neuroAssist-main
   python -m uvicorn app.main:app --reload --port 8000
   
   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

2. **Navigate to frontend:** http://localhost:5174

3. **Test the flow:**
   - Click **Login** → "Forgot password?" link
   - Enter registered email
   - Check Gmail for OTP email
   - Copy 6-digit OTP
   - Go to Reset Password page
   - Enter email, OTP, new password
   - Click "Reset Password"
   - Should see success message and redirect to login
   - Login with new password

### Test Flow 2: Test Invalid OTP

1. Go to /forgot-password
2. Request OTP
3. Go to /reset-password
4. Enter wrong OTP (e.g., 000000)
5. Should see error: "Invalid OTP code"

### Test Flow 3: Test Expired OTP

1. Request OTP
2. Wait 10+ minutes
3. Try to reset password
4. Should see error: "OTP has expired"

### Test Flow 4: Email Not Configured

If SMTP is not configured:
1. OTP will be generated but email will fail silently
2. Check backend logs for email send failure
3. In development, you can:
   - Query Supabase directly for OTP code
   - Or check backend console logs

---

## Step 7: Production Deployment

### 7.1 Environment Variables

On your hosting platform (Render, Vercel, etc.), set:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SMTP_EMAIL`
- `SMTP_PASSWORD`
- All other variables from `.env`

### 7.2 Email Considerations

**For Gmail:**
- Send limit: ~300 emails per day
- Recommended for development/testing
- For production: Use SendGrid, AWS SES, or dedicated email service

**Email Service Alternatives:**
```python
# Instead of SMTP, you could use:
# - SendGrid API
# - AWS SES
# - Mailgun
# - Twilio SendGrid
```

---

## Troubleshooting

### Issue: "SMTP Authentication failed"
**Solution:**
- Verify `SMTP_EMAIL` and `SMTP_PASSWORD` in `.env`
- For Gmail, ensure you're using the 16-char App Password, not your account password
- Enable "Less secure app access" if not using App Password (not recommended)

### Issue: "OTP email not received"
**Solution:**
- Check spam/junk folder
- Verify email address is correct
- Check backend logs for email send errors
- Ensure backend is running and .env variables are loaded

### Issue: "No active OTP found"
**Solution:**
- User needs to request new OTP first (via /forgot-password)
- OTP expires after 10 minutes
- Each email can only have one active OTP at a time

### Issue: "Could not find the table"
**Solution:**
- Run the SQL from Step 1 to create the table
- Verify Supabase connection is working
- Check that SUPABASE_KEY is a service_role key (not anon key)

---

## File Reference

### New Files Created

1. **`setup_password_reset_table.sql`** - Database table creation
2. **`app/services/email_service.py`** - SMTP email utility
3. **`app/schemas/password_reset.py`** - Request/response schemas
4. **`frontend/src/pages/ForgotPassword.jsx`** - OTP request UI
5. **`frontend/src/pages/ResetPassword.jsx`** - Password reset UI
6. **`.env.example`** - Environment variable template

### Modified Files

1. **`app/config.py`** - Added SMTP settings
2. **`app/api/routes/auth.py`** - Added 2 new endpoints
3. **`app/main.py`** - No changes needed (auto-includes routes)
4. **`frontend/src/App.jsx`** - Added new routes
5. **`frontend/src/pages/Login.jsx`** - Added "Forgot Password?" link

---

## API Documentation

### Endpoint: POST `/api/auth/forgot-password`

**Purpose:** Request OTP for password reset

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Success Response (200):**
```json
{
  "message": "If this email exists, an OTP has been sent. Check your email.",
  "status": "success"
}
```

**Error Response (400):**
```json
{
  "detail": "Email already has an active OTP. Please wait before requesting another."
}
```

**Error Response (500):**
```json
{
  "detail": "Failed to generate OTP"
}
```

---

### Endpoint: POST `/api/auth/reset-password`

**Purpose:** Reset password using OTP

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp_code": "123456",
  "new_password": "NewSecurePassword123!"
}
```

**Success Response (200):**
```json
{
  "message": "Password has been reset successfully. Please login with your new password.",
  "status": "success"
}
```

**Error Responses:**
```json
// Invalid OTP
{ "detail": "Invalid OTP code" }

// OTP expired
{ "detail": "OTP has expired. Request a new one." }

// OTP already used
{ "detail": "This OTP has already been used" }

// User not found
{ "detail": "User not found" }

// No active OTP
{ "detail": "No active OTP found. Request a new one." }
```

---

## Security Best Practices

✅ **Implemented:**
- OTP expires after 10 minutes
- OTP codes are 6 digits (cryptographically random)
- Passwords are hashed with bcrypt
- Email validation with Pydantic `EmailStr`
- One active OTP per email at a time
- OTP marked as "used" after successful reset
- HTTPS for all communications (in production)

⚠️ **Additional Recommendations:**
- Rate limit OTP requests (implement in production)
- Log all password reset attempts for audit trail
- Consider adding email verification step before account activation
- Use environment variables for all sensitive data
- Rotate secrets periodically
- Monitor for suspicious OTP requests

---

## Performance Considerations

- **Database Indexes:** Created on `user_email` and `is_used` for fast queries
- **OTP Expiration:** Automatic cleanup can be added with database triggers
- **Email Rate Limit:** Currently unlimited - add rate limiting in production
- **Concurrent Requests:** Can be improved with async email sending

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review backend logs: `python -m uvicorn app.main:app --reload`
3. Check browser console for frontend errors
4. Verify Supabase connection in dashboard
5. Test email credentials separately

---

**Last Updated:** 2026-02-09  
**Version:** 1.0.0
