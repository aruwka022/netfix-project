# NetFix

A Django-based service marketplace: companies list home services (plumbing,
electricity, cleaning, and more), customers browse and request them.

## Features

- Two account types: **Company** (creates services) and **Customer** (requests them)
- Registration with unique email/username validation
- Services restricted to a company's field of work
- Most-requested services on the homepage, full catalog with search & sort,
  per-category browsing with pagination
- Customers can request a service (address + hours) with automatic cost calculation
- 1-5 star rating system for completed requests, averaged into service/company ratings
- Companies can edit or delete their own services, and see who requested them
- Full profile pages for both account types

## Tech stack

- Python 3 / Django 3.1.14
- SQLite (default dev database)

## Setup

```bash
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver