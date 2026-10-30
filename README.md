# Campus Trade 🎓

> **"Your Campus. Your Marketplace."**
> A fast, trusted, peer-to-peer marketplace designed specifically for college campuses.

---

## ⚡ Overview

Campus Trade replaces scattered WhatsApp groups and bulletin boards with a single, ultra-fast, mobile-friendly marketplace where verified college students buy and sell textbooks, calculators, electronics, bicycles, backpacks, and hostel essentials from students nearby.

Visually inspired by Linear, Vercel, Notion, and Apple, Campus Trade delivers a modern consumer experience with zero clutter, instant search and filtering, live in-app chat with pinned listing cards, a 4-step streamlined sell wizard, and dark/light mode.

---

## 🛠 Tech Stack

### Frontend
- **Architecture**: Static Single-Page Application (SPA) with zero build step
- **Styling**: Vanilla CSS3 with CSS custom properties for full Light & Dark mode
- **Router**: Client-side hash router (`#/`, `#/marketplace`, `#/item/:id`, `#/sell`, `#/messages`, `#/profile`, `#/dashboard`)
- **Typography**: Google Fonts (*Plus Jakarta Sans* for display/headings, *Inter* for body/UI)
- **Icons**: Hand-crafted inline SVGs (no external icon font dependency)
- **Motion**: CSS transitions/keyframes, micro-interactions, `prefers-reduced-motion` compliance

### Backend
- **Framework**: FastAPI (Python 3.12 / 3.11)
- **Server**: Uvicorn (ASGI)
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic v2
- **Auth**: JWT tokens via `python-jose` with PBKDF2 SHA-256 password hashing
- **Database**: SQLite (file-based) by default, easily swappable to Postgres/MySQL via `DATABASE_URL`
- **File Uploads**: Base64 decoding directly to `/uploads` static file storage

---

## 🚀 Quick Start

### 1. Local Python Setup

```bash
# Clone or navigate to the directory
cd campus_trade_final

# Install dependencies
pip install -r requirements.txt

# Seed the database with demo users, realistic items, and sample conversations
python seed.py

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

Open your browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

### 2. Docker Setup

```bash
# Build Docker image (pinned to python:3.12-slim per PRD)
docker build -t campus-trade .

# Run container
docker run -p 8000:8000 campus-trade
```

### 3. Deploy from GitHub

For a Docker-based deployment using the repository's `backend` folder, set the
host's root/build directory to `backend` and use `backend/Dockerfile` (or
`Dockerfile` if the host resolves it relative to that directory). Set a strong
`SECRET_KEY` in the host's environment. Use a managed database and persistent
storage for `uploads/` if the host does not retain container files between
deploys. See [`backend/README.md`](backend/README.md) for details.

---

## 👤 Demo Credentials

The database comes pre-seeded with 4 verified campus student accounts:

| Name | Email | Password | Role / Department |
| :--- | :--- | :--- | :--- |
| **Alex Rivera** (Active Demo User) | `alex@campus.edu` | `password123` | 3rd Year • Computer Science |
| **Priya Sharma** | `priya@campus.edu` | `password123` | 2nd Year • Electrical Engg |
| **Marcus Vance** | `marcus@campus.edu` | `password123` | 4th Year • Mechanical Engg |
| **Sarah Jenkins** | `sarah@campus.edu` | `password123` | 1st Year • Product Design |

---

## 🗺 Information Architecture & Routes

| Route | View | Description |
| :--- | :--- | :--- |
| `#/` | **Home** | Staggered hero, full-bleed campus photo strip with gradient fade, category grid, fresh listings, device preview mockup, CTA banner |
| `#/marketplace` | **Marketplace** | Real-time search, category filter pills, sort controls, skeleton loader, responsive 4→2 column grid |
| `#/item/:id` | **Item Detail** | Image gallery with thumbnail switcher, price, condition badge, seller card, **"Chat with Seller"** primary CTA, wishlist toggle |
| `#/sell` | **Sell Wizard** | 4-step wizard: Photos (drag-and-drop / browse) → Details → Price & Condition chips → Review & Live Publish |
| `#/messages` | **Messages** | Two-pane chat, unread indicator, pinned listing reference card, auto-scroll, instant bubble sending |
| `#/profile` | **Profile** | User details, statistics, and instant tab switching between Listings, Sold, and Wishlist items |
| `#/dashboard` | **Seller Dashboard** | 3 animated metric cards (Active, Sold, Drafts), active listings grid, quick create button |

---

## 🔌 API Contract Reference

| Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | No | Create student account, returns JWT |
| `POST` | `/api/auth/login` | No | OAuth2 password flow, returns JWT |
| `GET` | `/api/auth/me` | Yes | Get authenticated user profile |
| `GET` | `/api/items` | Optional | Search, filter, and sort campus items |
| `GET` | `/api/items/{id}` | Optional | Get item details with seller & images |
| `POST` | `/api/items` | Yes | Create item listing (supports base64 image data URIs) |
| `PATCH` | `/api/items/{id}` | Yes (Owner) | Edit item or mark as sold |
| `DELETE` | `/api/items/{id}` | Yes (Owner) | Delete item listing |
| `GET` | `/api/items/meta/categories` | No | Fixed category list |
| `GET` | `/api/wishlist` | Yes | Get saved wishlist items |
| `POST` | `/api/wishlist/{item_id}/toggle`| Yes | Toggle item in wishlist with bounce animation |
| `GET` | `/api/conversations` | Yes | List conversations with unread counts |
| `POST` | `/api/conversations` | Yes | Start a conversation regarding an item |
| `GET` | `/api/conversations/{id}` | Yes | Full conversation thread (marks unread as read) |
| `POST` | `/api/conversations/{id}/messages` | Yes | Send chat message |
| `GET` | `/api/users/me/dashboard` | Yes | Active/sold/draft counts, rating, views |
| `GET` | `/api/health` | No | Health check |

---

## 🎨 Design System

- **Light Mode Colors**: `--bg: #FAF9F7`, `--bg-elevated: #FFFFFF`, `--accent: #4F46E5`, `--border: #E7E5E0`
- **Dark Mode Colors**: `--bg: #0B0B0D`, `--bg-elevated: #131317`, `--accent: #8683FF`, `--border: #242529`
- **Typography**: Display: *Plus Jakarta Sans* (600–800), Body/UI: *Inter* (400–700)
- **Border Radius**: 10–14px (controls/cards), 20–26px (banners/panels)
- **Responsive**: Full mobile layout (< 768px) with bottom navigation bar and collapsed single-view chat
