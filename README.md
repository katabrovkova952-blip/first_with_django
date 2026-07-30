# BookShelf
 ![CI](https://github.com/katabrovkova952-blip/first_with_django/actions/workflows/tests.yml/badge.svg)

BookShelf is a Django REST API for tracking a personal reading life: browse a shared book catalog, keep your own shelf of books you want to read / are reading / have finished, track your page progress, and leave a rating and review once you're done. It also includes an AI-powered assistant that recommends and discusses books grounded in the actual catalog data.
 
**Live demo:** https://first-with-django.onrender.com/api/docs/
 
## Tech stack
 
- **Backend:** Python, Django, Django REST Framework
- **Auth:** JWT via `djangorestframework-simplejwt`
- **Database:** PostgreSQL
- **Filtering/search:** `django-filter`, DRF `SearchFilter` / `OrderingFilter`
- **AI:** OpenAI API (`gpt-5.4-mini`)
- **Testing:** pytest, pytest-django
- **Docs:** drf-spectacular (Swagger / Redoc)
- **Infra:** Docker, Docker Compose, Gunicorn
- **Config:** python-decouple (environment-based settings)
## Features
 
**Book catalog**
Public, searchable catalog of books (title, author, description, year, total pages). Anyone can browse and search; only staff/admin accounts can add, edit, or remove books, keeping the catalog authoritative. Supports filtering by author/year, text search across title/author/description, and ordering by year, title, or date added.
 
**Personal shelf**
Registered users can add any book to their own shelf and track it through three states — *want to read*, *reading*, *finished* — along with current page progress. Progress is validated against the book's actual page count, and marking a book "finished" automatically timestamps completion.
 
**Reviews**
Once a book is marked finished on a user's shelf, they can leave a review with a 1–5 rating. Reviews are tied to a specific shelf entry, so you can only review books you've actually read, and only your own.
 
**Authentication**
JWT-based registration and login. Ownership is enforced end-to-end: users can only see and modify their own shelf entries and reviews.
 
**AI Reading Assistant**
A conversational endpoint that answers questions about the catalog — recommendations, comparisons, "is this book for me" — grounded in real catalog data rather than the model's general knowledge (see below).
 
**API documentation**
Auto-generated, interactive OpenAPI schema via drf-spectacular (Swagger UI and Redoc).
 
**Dockerized**
Full local dev and deployment setup via Docker Compose (app + PostgreSQL), with migrations running automatically on startup.
 
## AI Reading Assistant
 
**Endpoint:** `POST /assistant/ask/`
**Access:** public (no authentication required), rate-limited to 5 requests/minute per IP to control API cost and prevent abuse.
 
### How it works
 
1. The client sends a `question`, optionally scoped to a specific book via `book_id`.
2. If `book_id` is provided, the API fetches that book from the database and grounds the assistant's answer in its title, author, publication year, and description. If the book doesn't exist, the API returns `404`.
3. If `book_id` is omitted, the API searches the catalog for books matching keywords in the question (title/description) and falls back to a small random sample of the catalog if nothing matches — this guarantees the assistant always has real catalog data to work with instead of inventing books.
4. The assembled context (question + book data) is sent to OpenAI's `gpt-5.4-mini` model, and the generated answer is returned to the client.
In a real frontend integration, `book_id` is meant to be supplied automatically by the client (e.g. the book detail page the user is currently viewing), not typed by the end user — the user only ever types natural-language questions.
 
### Request
 
```json
POST /assistant/ask/
Content-Type: application/json
 
{
  "question": "Who would enjoy this book?",
  "book_id": 2
}
```
 
`book_id` is optional — omit it for general recommendations (e.g. "What's a good detective novel?").
 
### Response
 
Success (`200 OK`):
```json
{ "answer": "..." }
```
 
Validation error (`400`) — missing/invalid `question`.
 
Book not found (`404`):
```json
{ "error": "Книгу з таким id не знайдено" }
```
 
AI service unavailable (`503`):
```json
{ "error": "AI-сервіс тимчасово недоступний" }
```
 
### Configuration
 
Requires an OpenAI API key set as an environment variable:
```
OPENAI_API_KEY=sk-...
```
Get one at [platform.openai.com](https://platform.openai.com/api-keys). API usage is billed separately from a ChatGPT subscription — a small prepaid balance ($5+) covers extensive testing given the low per-request cost of `gpt-5.4-mini`.
 
## Getting started
 
### Prerequisites
 
- Docker and Docker Compose
- An OpenAI API key (for the AI assistant feature)
### Setup
 
1. Clone the repository:
```
   git clone https://github.com/katabrovkova952-blip/first_with_django.git
   cd first_with_django
```
 
2. Copy the example environment file and fill in your own values:
```
   cp .env.example .env
```
   Required variables include `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, database credentials (`DB_NAME`, `DB_USER`, `DB_PASSWORD`), and `OPENAI_API_KEY`.
 
3. Build and start the containers:
```
   docker-compose up --build
```
   Migrations run automatically on startup.
 
4. Create an admin user (needed to access `/admin/` and manage the book catalog):
```
   docker-compose exec bookshelf python manage.py createsuperuser
```
 
The API will be available at `http://localhost:8000/`.
 
### Running tests
 
```
docker-compose exec bookshelf pytest
```
 
## API overview
 
| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/api/register/` | POST | Public | Create a new user account |
| `/api/token/` | POST | Public | Obtain JWT access/refresh tokens |
| `/api/token/refresh/` | POST | Public | Refresh an access token |
| `/api/books/` | GET | Public | List/search/filter the catalog |
| `/api/books/` | POST | Staff only | Add a new book |
| `/api/books/<id>/` | GET | Public | Retrieve a book |
| `/api/books/<id>/` | PUT/PATCH/DELETE | Staff only | Update or remove a book |
| `/api/shelf/` | GET/POST | Owner | View or add books to your shelf |
| `/api/shelf/<id>/` | GET/PUT/PATCH/DELETE | Owner | Update reading status/progress, or remove |
| `/api/review/` | GET/POST | Owner | View or create reviews for your finished books |
| `/api/review/<id>/` | GET/PUT/PATCH/DELETE | Owner | Update or remove your review |
| `/assistant/ask/` | POST | Public (rate-limited) | Ask the AI reading assistant a question |
| `/api/schema/` | GET | Public | Raw OpenAPI schema |
| `/api/docs/` | GET | Public | Interactive Swagger UI |
| `/api/redoc/` | GET | Public | Redoc API documentation |
 
## Project structure
 
```
├── config/          # Project settings, root URLs
├── books/           # Book catalog, shelf, reviews, registration
├── assistant/        # AI reading assistant app
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── requirements.txt
```