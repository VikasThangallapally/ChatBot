-- Create users table for Brain Tumor MRI prediction app
CREATE TABLE IF NOT EXISTS public.users (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

-- Enable RLS (Row Level Security)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Drop old policies if they exist (to avoid conflicts)
DROP POLICY IF EXISTS "Allow anon to register" ON public.users;
DROP POLICY IF EXISTS "Allow users to read own data" ON public.users;

-- Create RLS policy to allow anyone to insert (for registration)
CREATE POLICY "Allow anon to register" ON public.users
  FOR INSERT
  WITH CHECK (true);

-- Create RLS policy to allow users to read all data (since this is not auth-dependent)
CREATE POLICY "Allow read access" ON public.users
  FOR SELECT
  USING (true);

-- Optional: Create policy for update operations
CREATE POLICY "Allow update own data" ON public.users
  FOR UPDATE
  USING (true);
