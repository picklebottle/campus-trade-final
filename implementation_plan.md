# Implementation Plan: Campus Trade (P2P Campus Marketplace)

Build **Campus Trade**, a peer-to-peer marketplace for college campuses where students buy and sell textbooks, electronics, cycles, calculators, bags, and hostel essentials from verified students nearby.

The application follows the PRD specifications with a high-fidelity static single-page frontend (HTML5/CSS3/Vanilla JS), a robust FastAPI backend (SQLAlchemy ORM, SQLite, Pydantic v2, JWT auth, PBKDF2 password hashing), pre-seeded demo data, and full responsive design matching the Linear/Vercel/Apple design aesthetic.

---

## User Review Required

> [!NOTE]
> - **Portability**: The frontend is a static SPA served directly by FastAPI (or any static server) with an in-memory client-side router (`#/`, `#/marketplace`, `#/item/:id`, `#/sell`, `#/messages`, `#/profile`, `#/dashboard`). It communicates with the FastAPI REST API, with fallback mock data if running standalone.
> - **Python Environment**: We will install `sqlalchemy`, `passlib`, `python-jose[cryptography]`, and `python-multipart` into the local Python environment.

---

## Proposed Changes

### Backend Architecture (`app/`)

#### [NEW] `requirements.txt`
Dependencies matching PRD Section 5:
- `fastapi==0.115.0`
- `uvicorn[standard]==0.30.6`
- `sqlalchemy==2.0.35`
- `pydantic==2.9.2`
- `python-jose[cryptography]==3.3.0`
- `passlib[pbkdf2]==1.7.4`
- `python-multipart==0.0.9`

#### [NEW] `app/config.py`
Settings including `SECRET_KEY`, `DATABASE_URL` (defaults to `sqlite:///./campus_trait.db`), `ACCESS_TOKEN_EXPIRE_MINUTES`, and `UPLOAD_DIR`.

#### [NEW] `app/database.py`
SQLAlchemy engine with SQLite connection handling (`check_same_thread=False`), sessionmaker, and declarative base.

#### [NEW] `app/models.py`
Full ORM models matching PRD Section 8:
- `User`: `id`, `name`, `email`, `hashed_password`, `college`, `department`, `year`, `rating` (default 5.0), `profile_views` (default 0), `created_at`
- `Item`: `id`, `title`, `description`, `price`, `category`, `condition` (`Like new`, `Good condition`, `Fair condition`), `status` (`active`, `sold`, `draft`), `seller_id` (FK), `created_at`, `sold_at`
- `ItemImage`: `id`, `item_id` (FK), `url`, `position`
- `WishlistEntry`: `id`, `user_id` (FK), `item_id` (FK), `created_at`, `UniqueConstraint("user_id", "item_id")`
- `Conversation`: `id`, `item_id` (FK nullable), `buyer_id` (FK), `seller_id` (FK), `created_at`
- `Message`: `id`, `conversation_id` (FK), `sender_id` (FK), `text`, `is_read` (default False), `created_at`

#### [NEW] `app/schemas.py`
Pydantic v2 request/response schemas for:
- User registration, login, token, user profile, dashboard stats
- Item creation (with `image_urls` accepting base64 data URIs or paths), update, item detail, item list query
- Wishlist response & toggle
- Conversation summary, detail thread with messages, message create
- Category metadata

#### [NEW] `app/auth.py`
Security utilities:
- PBKDF2 SHA-256 password hashing & verification
- JWT creation and decoding
- FastAPI dependencies: `get_current_user` (required) and `get_optional_user` (optional)

#### [NEW] `app/routers/`
- `auth.py`:
  - `POST /api/auth/register`
  - `POST /api/auth/login` (supports OAuth2 password request form and JSON body)
  - `GET /api/auth/me`
- `items.py`:
  - `GET /api/items` (query filters: `search`, `category`, `sort` [recent, low, high], `status`, `mine`, `limit`, `offset`)
  - `GET /api/items/{id}`
  - `POST /api/items` (handles base64 image decoding to disk/static files)
  - `PATCH /api/items/{id}` (seller only: title, price, description, status)
  - `DELETE /api/items/{id}` (seller only)
  - `GET /api/items/meta/categories`
- `wishlist.py`:
  - `GET /api/wishlist`
  - `POST /api/wishlist/{item_id}`
  - `DELETE /api/wishlist/{item_id}`
  - `POST /api/wishlist/{item_id}/toggle`
- `conversations.py`:
  - `GET /api/conversations` (with unread counts, latest message, item snippet)
  - `POST /api/conversations` (start conversation about item)
  - `GET /api/conversations/{id}` (thread + automatically marks incoming messages as read)
  - `POST /api/conversations/{id}/messages` (send message)
- `users.py`:
  - `GET /api/users/me/dashboard` (active, sold, draft counts, rating, views incremented)
  - `GET /api/users/{id}` (public profile)
- `health.py`:
  - `GET /api/health`

#### [NEW] `app/main.py`
FastAPI app mounting `/static` for assets, `/uploads` for user-uploaded images, configuring CORS, registering all routers, and serving `static/index.html` at root.

#### [NEW] `seed.py`
Comprehensive seed script generating:
- Demo users (e.g., Alex Rivera - 3rd Year CS, Priya Sharma - 2nd Year EE, Marcus Chen - 4th Year Mech, Sarah Lin - 1st Year Design)
- 12+ realistic items across Books, Electronics, Calculators, Cycles, Bags, Hostel Essentials with realistic college pricing, multiple images, and conditions
- Sample conversations and message threads
- Pre-populated wishlist items

---

### Frontend Single-Page App (`static/`)

#### [NEW] `static/index.html`
- SEO meta tags, Title: "Campus Trade — Your Campus. Your Marketplace."
- Google Fonts: Plus Jakarta Sans & Inter
- Responsive viewport with safe-area insets
- App container with sticky header, main content host `#app`, desktop footer, and mobile bottom navigation bar (`< 768px`)
- Toast container for feedback notifications

#### [NEW] `static/css/style.css`
- Design system tokens (PRD Section 10):
  - Light theme: `--bg: #FAF9F7`, `--bg-elevated: #FFFFFF`, `--surface: #F4F3F0`, `--border: #E7E5E0`, `--border-strong: #D9D6D0`, `--text: #15161A`, `--text-dim: #6B6D78`, `--text-faint: #9A9BA5`, `--accent: #4F46E5`, `--accent-hover: #4338CA`
  - Dark theme: `--bg: #0B0B0D`, `--bg-elevated: #131317`, `--surface: #17181C`, `--border: #242529`, `--border-strong: #31323A`, `--text: #F2F2F4`, `--text-dim: #9EA0AA`, `--text-faint: #6B6D77`, `--accent: #8683FF`, `--accent-hover: #9A97FF`
- Components & layouts:
  - Sticky header with glassmorphism on scroll (`backdrop-filter: blur(12px)`)
  - Staggered entrance keyframes (`fadeUp`)
  - Full-bleed campus photo strip with CSS mask gradient (`linear-gradient(to bottom, black 55%, transparent 100%)`)
  - Category cards with hover lift & icon tint
  - Item cards with image zoom on hover, condition badge, price tag, and wishlist heart with bounce animation
  - Marketplace preview device frame
  - Search bar, category filter pills, sort select, skeleton shimmer loaders, empty states
  - Product detail gallery with thumbnail selection and smooth fade
  - 4-step Sell wizard with step indicators, drag-and-drop dropzone, image previews with hover remove, chip selectors, draft indicator, and review step
  - Two-pane messages layout (collapsible on mobile), unread dot, pinned item card, chat bubbles
  - Profile & Dashboard with animated stat cards and instant tab switching
  - Mobile bottom navigation (< 768px) with elevated center "Sell" action
  - Full `prefers-reduced-motion: reduce` overrides

#### [NEW] `static/js/app.js`
- **Router**: Hash-based router (`#/`, `#/marketplace`, `#/item/:id`, `#/sell`, `#/messages`, `#/profile`, `#/dashboard`) with scroll-to-top and route-change hooks
- **API Client**: REST client connecting to FastAPI backend with bearer token auth and automatic fallback
- **State Store**: Reactive in-memory state for current user, active item, conversations, wishlist set, active filters
- **Views**:
  - `renderHome()`: Staggered hero, campus photo strip, category grid, fresh 4 listings, device mockup preview, closing CTA
  - `renderMarketplace()`: Live search filter, category pills, sort dropdown, skeleton loading state, live result counter, empty state, responsive grid
  - `renderItemDetail(id)`: Multi-image gallery with active thumbnail switcher, seller info card, response-time badge, "Chat with Seller" action, wishlist toggle
  - `renderSellWizard()`: 4-step state machine (Photos -> Details -> Price/Condition -> Review), file upload + drag-and-drop handler with base64 encoding, validation, live publish
  - `renderMessages(conversationId)`: Two-pane layout, conversation list with unread markers, active thread with pinned item reference, auto-scroll, message send
  - `renderProfile()`: Stats row, Listings / Sold / Wishlist tabs with distinct empty states
  - `renderDashboard()`: 3 staggered metric cards (Active / Sold / Drafts), active listings grid, quick create shortcut
- **UI Enhancements**:
  - Theme toggle (light/dark) with persistence and smooth transition
  - Global toast notification manager
  - Wishlist toggle handler with bounce micro-animation

#### [NEW] Assets & Images
- High quality college/campus assets and item photography (calculators, textbooks, road bike, MacBook, tech bag, desk lamp)
- Inline SVG icons across the app

---

### Deployment & Config

#### [NEW] `Dockerfile`
`python:3.12-slim` container build with SQLite directory creation, requirements install, and uvicorn CMD.

#### [NEW] `.env.example`
Configuration template with `SECRET_KEY`, `DATABASE_URL`, and `PORT`.

#### [NEW] `README.md`
Complete documentation for running locally, seeding, running with Docker, and architectural details.

---

## Verification Plan

### Automated Verification
1. **Dependency check**: Install and verify all required packages in the Python environment.
2. **Database & Seed test**: Run `seed.py` to create SQLite tables and populate demo data; verify records count for users, items, images, conversations, messages, and wishlist entries.
3. **API endpoint tests**: Run an API smoke test script executing requests against:
   - `GET /api/health`
   - `POST /api/auth/login` (retrieve JWT token)
   - `GET /api/items` (verify search, category, sort params)
   - `POST /api/items` (create test item)
   - `POST /api/wishlist/{item_id}/toggle` (test wishlist toggle)
   - `GET /api/conversations` and `POST /api/conversations/{id}/messages` (test chat thread)
   - `GET /api/users/me/dashboard` (test seller dashboard metrics)

### Interactive Browser Verification (via Browser Subagent)
1. **Home Page (`#/`)**:
   - Check hero layout visibility above fold, staggered animations, campus photo strip gradient fade, category hover states, fresh listings, and marketplace preview mockup.
2. **Marketplace (`#/marketplace`)**:
   - Test search query filtering, category pill selection, sorting (price low->high, high->low, recent), skeleton loading state, and empty state search.
3. **Product Detail (`#/item/:id`)**:
   - Test thumbnail switching in gallery, condition badges, seller card info, wishlist heart click animation, and "Chat with Seller" navigation.
4. **Sell Wizard (`#/sell`)**:
   - Complete 4-step wizard: upload photo -> enter title & category -> select price & condition chip -> review summary -> publish item. Verify item appears in marketplace.
5. **Messages (`#/messages`)**:
   - Open conversation, verify pinned listing reference card, send a new message, verify instant bubble append and auto-scroll.
6. **Profile (`#/profile`) & Dashboard (`#/dashboard`)**:
   - Test tab switching (Listings / Sold / Wishlist) and stat cards.
7. **Theme Toggle**:
   - Switch between light and dark theme, verifying CSS custom property updates and smooth transition.
8. **Mobile Viewport Test**:
   - Resize to 390px (mobile) to verify bottom navigation bar, collapsed chat view, and 2-column marketplace grid.
