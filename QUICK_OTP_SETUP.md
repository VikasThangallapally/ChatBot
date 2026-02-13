# ⚡ OTP Password Reset - Quick Setup (5 Minutes)

## 1️⃣ Database Setup (1 minute)

**Go to:** https://app.supabase.com → Your Project → SQL Editor

**Copy & Paste:**
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

**Click:** Run ✅

---

## 2️⃣ SendGrid API Key (1 minute)

**Go to:** https://app.sendgrid.com/settings/api_keys

1. Click **Create API Key**
2. Give it a name (e.g., "Brain Tumor MRI App")
3. Select **Full Access** or **Mail Send** permission
4. Click **Create & View**
5. Copy the API key (starts with `SG.`)

**Also verify your sender email:**
1. Go to **Sender Authentication**
2. Verify your email address (`vikasthangallapally.8380@gmail.com`)
3. Use this verified email in `.env` as `SENDGRID_FROM_EMAIL`

---

## 3️⃣ Environment Variables (1 minute)

**Update your `.env` file:**

```bash
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=vikasthangallapally.8380@gmail.com
```

---

## 4️⃣ Test It (1 minute)

```bash
# Terminal 1:
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2:
cd frontend && npm run dev

# Then visit: http://localhost:5174
# Click Login → Forgot password? → Enter email → Check Gmail
```

---

## ✍️ That's It! 

All files are already created. Just:
1. ✅ Create table in Supabase
2. ✅ Get Gmail app password
3. ✅ Update .env file
4. ✅ Start backend & frontend
5. ✅ Test at `/forgot-password`

---

## 📋 File Checklist

Backend files exist:
- ✅ `app/services/email_service.py`
- ✅ `app/schemas/password_reset.py`
- ✅ `app/api/routes/auth.py` (updated)
- ✅ `app/config.py` (updated)

Frontend files exist:
- ✅ `frontend/src/pages/ForgotPassword.jsx`
- ✅ `frontend/src/pages/ResetPassword.jsx`
- ✅ `frontend/src/App.jsx` (updated)
- ✅ `frontend/src/pages/Login.jsx` (updated)

Reference docs:
- 📖 `OTP_PASSWORD_RESET_SETUP.md` (detailed guide)
- 📖 `OTP_IMPLEMENTATION_SUMMARY.md` (what was built)
- 📖 `setup_password_reset_table.sql` (SQL script)
- 🧪 `test_otp_password_reset.py` (test script)
- 📋 `.env.example` (environment template)

---

## 🔗 User Flow

```
Login Page
    ↓
[Forgot password?]
    ↓
Enter email → Send OTP
    ↓
📧 Check Gmail
    ↓
Reset Password Page
    ↓
Enter OTP + New Password
    ↓
✅ Success → Back to Login
    ↓
Login with new password
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| Email not sent | Check `SMTP_EMAIL` and `SMTP_PASSWORD` in `.env` |
| "Invalid API key" | Use service_role key, not anon key |
| "Table not found" | Run SQL from Step 1 |
| Gmail rejected | Use App Password, not account password |
| OTP expired | Expires in 10 mins, request new one |

---

## 📞 Support

See `OTP_PASSWORD_RESET_SETUP.md` for:
- Detailed troubleshooting
- API endpoint docs
- Security best practices
- Production deployment guide

---

✅ **Ready!** Your app now has OTP-based password reset! 🎉
