# AssetTrack — Setup Guide (Supabase + Django)

This walks you through connecting this project to Supabase and running it, step by step. No prior Django experience assumed.

---

## Part 1 — Create your Supabase project

1. Go to https://supabase.com and sign in (or create a free account).
2. Click **New Project**.
3. Fill in:
   - **Name**: `assettrack` (or anything you like)
   - **Database Password**: create a strong password and **save it somewhere safe** — you'll need it in a moment.
   - **Region**: pick the one closest to you.
4. Click **Create new project** and wait 1–2 minutes while Supabase sets it up.

## Part 2 — Get your database connection details

1. Once the project is ready, click the **Connect** button near the top of the project page (or go to **Project Settings → Database**).
2. Look for the **Connection string** section and switch it to **Session pooler** (recommended for Django) or **Transaction pooler**.
3. You'll see something like:
   ```
   postgresql://postgres.abcdefghijk:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```
4. From that string, note down these 5 pieces:
   - **DB_USER** → the part after `postgresql://` and before `:` → e.g. `postgres.abcdefghijk`
   - **DB_PASSWORD** → the password you created in Part 1
   - **DB_HOST** → the part after `@` and before `:` → e.g. `aws-0-ap-southeast-1.pooler.supabase.com`
   - **DB_PORT** → the number after the host → `6543` (pooler) or `5432` (direct)
   - **DB_NAME** → the part after the last `/` → usually `postgres`

## Part 3 — Configure the project

1. In the project folder, find the file named `.env.example`.
2. Make a copy of it and rename the copy to `.env` (same folder, same level as `manage.py`).
3. Open `.env` and fill in the values you collected in Part 2:
   ```
   DJANGO_SECRET_KEY=replace-with-a-long-random-string
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

   DB_NAME=postgres
   DB_USER=postgres.abcdefghijk
   DB_PASSWORD=your-real-password
   DB_HOST=aws-0-ap-southeast-1.pooler.supabase.com
   DB_PORT=6543
   ```
4. For `DJANGO_SECRET_KEY`, you can generate one by running this in a terminal:
   ```
   python3 -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Paste the result into `.env`.

## Part 4 — Install everything and run the app

Open a terminal inside the project folder, then run these one at a time:

```bash
python3 -m venv venv
source venv/bin/activate          # on Windows: venv\Scripts\activate

pip install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py createsuperuser  # creates your first admin login for /admin/
```

When `createsuperuser` asks for details, you can use any username/email/password — this account is separate from the in-app "IT Admin" role, and only used for the Django admin panel at `/admin/`.

Then start the server:

```bash
python3 manage.py runserver
```

Open your browser to **http://127.0.0.1:8000/** — you'll land on the login page.

## Part 5 — Create your first real accounts

1. Click **Register here** on the login page.
2. Create one account with role **IT Admin** — this is the account you'll use to manage devices, approve checkouts, and configure settings.
3. Create a second account with role **Employee** to test the employee side.
4. Log in as the IT Admin, go to **Categories** and **Departments** in the sidebar to add a few starter entries (e.g. Laptop, Monitor), then go to **Devices → Add Device** to start building your inventory.
5. Go to **Settings** in the sidebar to turn self-checkout on/off and set the overdue threshold (default is 7 days).

## Troubleshooting

- **"could not connect to server" / connection refused**: double-check `DB_HOST` and `DB_PORT` in `.env` — make sure you copied the pooler host, not something else.
- **"password authentication failed"**: your `DB_PASSWORD` in `.env` doesn't match your Supabase database password. You can reset it from **Project Settings → Database → Reset Database Password**.
- **Static files / styling look broken**: run `python3 manage.py collectstatic` (only needed in production, not for local `runserver`).
- **Changed a model and now migrations complain**: run `python3 manage.py makemigrations` then `python3 manage.py migrate` again.

## Notes

- This project always uses PostgreSQL (your Supabase database) — there is no SQLite fallback, by design.
- Uploaded images (profile photos, maintenance/damage photos) are saved to the local `media/` folder when running locally. For a real deployment, point `MEDIA_ROOT`/`MEDIA_URL` at Supabase Storage or another file host.
