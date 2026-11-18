# AssetTrack

AssetTrack is a Django web application for managing company-owned devices and the
full lifecycle of lending them to employees. It uses PostgreSQL (Supabase) for
persistence and a Bootstrap-based high-contrast dark UI.

## Core Feature — Device Checkout Lifecycle (Vertical Slice)

The core feature is the **device checkout lifecycle**, implemented end to end:

- **Database:** `Device`, `Category`, `Checkout`, and `MaintenanceLog` models with
  foreign keys to `accounts.User` (creator/requester/approver/reporter) and
  `accounts.Company`, plus migrations in `assets/migrations/`.
- **Backend:** Django forms, views, and URL routes in `assets/` handle inventory
  CRUD, checkout requests, approvals/rejections, direct assignment, returns,
  maintenance, reports, and settings. All views require login and enforce role
  and company scoping.
- **Frontend:** Templates in `templates/assets/` and `templates/base.html` let
  users click through the entire flow: add/edit/delete a device, request a
  device, approve or reject a request, assign an available device, mark a loan
  returned, and log maintenance.

### Admin flow

1. Log in as an IT Admin and set up a company (or join the seeded one).
2. **Devices → Add Device** (Create), **Devices** list (Read), row **Edit** (Update),
   row **Delete** (Delete; blocked for devices with checkout history).
3. **Checkouts → Review Requests** to approve or reject employee requests.
4. **Checkouts → Assign Device** for direct assignment.
5. **Checkouts → Active** → **Mark Returned** to close a loan.
6. **Maintenance** to report damage and resolve it.

### Employee flow

1. Log in as an Employee joined to a company.
2. The employee dashboard shows active loans, pending requests, and available pool.
3. **Request a Device** submits a checkout request (existing inventory item or a
   requested new model/category). If no matching device exists, the admin is
   redirected to a prefilled **Add Device** form that fulfills the request.
4. Requests are linked to the employee (`Checkout.employee` and `created_by`).
   Employees only ever see their own records on their dashboard.

### Validation and business rules

- Required fields, model uniqueness, and date input formats are validated by forms.
- A checkout request must name an available device **or** a requested model.
- Due dates cannot be in the past.
- Devices with checkout history cannot be deleted.
- Only available devices can be requested or assigned; returning a device makes it
  available again; reporting damage moves it to Under Repair.
- Self-checkout can be enabled/disabled by an admin in **Settings**.

## Standard Features (Project Development 1)

- Account registration (`accounts/register/`)
- Login / logout (`accounts/login/`, `accounts/logout/`)
- Role-based dashboards (`accounts/dashboard/admin/`, `accounts/dashboard/employee/`)
- User profile view and edit (`accounts/profile/`, `accounts/profile/edit/`)

## Tech Stack

- Python 3.12+, Django 5.1.5
- PostgreSQL via Supabase (`psycopg[binary]`), environment-driven configuration
- `python-dotenv`, `Pillow`, Bootstrap 5 + Bootstrap Icons (CDN)

## Setup

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/vanderken/AssetTrack-Bucog-KenEdrian-G1.git
   cd AssetTrack-Bucog-KenEdrian-G1
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file beside `manage.py` (see `SETUP.md` for details):

   ```env
   DJANGO_SECRET_KEY=replace-with-a-long-random-string
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
   DB_NAME=postgres
   DB_USER=postgres.your-project-ref
   DB_PASSWORD=your-supabase-password
   DB_HOST=aws-1-xxx.pooler.supabase.com
   DB_PORT=6543
   ```

   `.env` is gitignored and must never be committed.

5. Apply migrations and start the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   Open http://127.0.0.1:8000/ — you will be redirected to the login page.

6. Run the automated test suite (uses an in-memory SQLite test database, so it
   does not affect Supabase):

   ```bash
   python manage.py test
   ```

## Test Accounts

Create these through the registration page, then set up the company so employees
can join with its code:

| Role | Username | Password | Purpose |
| --- | --- | --- | --- |
| IT Admin | `admin_test` | `AssetTrack123!` | Inventory, approvals, reports, settings |
| Employee | `employee_test` | `AssetTrack123!` | Request and track own devices |

## Branching / Contribution Workflow

- `main` — stable, released code only; changed only by a PR from `develop`.
- `develop` — integration branch; created from `main`.
- `feature/<name>` — one branch per feature, created from `develop`.

Flow: `feature/*` → PR into `develop` → PR from `develop` into `main`.
Merged feature branches are kept, not deleted.

## Documentation

- `SETUP.md` — detailed Supabase configuration walkthrough.
- `docs/` — Project Development 2 completion report (PDF).
