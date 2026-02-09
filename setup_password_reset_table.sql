-- SQL to create password_reset_otps table in Supabase
-- Run this in Supabase SQL Editor

CREATE TABLE IF NOT EXISTS public.password_reset_otps (
  id BIGSERIAL PRIMARY KEY,
  user_email TEXT NOT NULL REFERENCES public.users(email) ON DELETE CASCADE,
  otp_code VARCHAR(6) NOT NULL,
  is_used BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  UNIQUE(user_email, is_used) -- Only one active OTP per email
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_otp_email ON public.password_reset_otps(user_email);
CREATE INDEX IF NOT EXISTS idx_otp_unused ON public.password_reset_otps(user_email, is_used);

-- Disable RLS for simplicity
ALTER TABLE public.password_reset_otps DISABLE ROW LEVEL SECURITY;
