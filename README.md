# Trading Signals SaaS Prototype 🚀

A simple SaaS prototype for stock trading signals where users can signup/login, subscribe via Stripe (₹499), and view trading signals in a React dashboard.  
Backend built with FastAPI + SQLAlchemy + Redis caching, frontend built with React (Vite).

---

## 🔥 Live URLs

- **Frontend (Vercel):** https://trading-signals-frontend.vercel.app/
- **Backend (Railway):** https://trading-signals-backend-production-adbc.up.railway.app/

---

## ✅ Features

### 1) User Authentication (JWT)
- Signup / Login using Email + Password
- JWT protected APIs
- `/auth/me` endpoint for logged-in user info

### 2) Stripe Subscription (₹499)
- Stripe Checkout Session
- Stripe Webhook: `checkout.session.completed`
- Paid users get full signals access

### 3) Signals + Redis Caching
- Mock trading signals (NIFTY / BANKNIFTY / RELIANCE etc.)
- Cached in Redis (TTL = 5 mins)
- Free users see limited signals
- Paid users see full list

### 4) React Dashboard
- Login page
- Dashboard with account info + signals table
- Subscribe button for free users
- Logout support

---

## 🧱 Tech Stack

### Backend
- FastAPI
- SQLAlchemy (SQLite locally / Postgres supported)
- Redis (caching + rate-limit + idempotency)
- Stripe (Checkout + Webhooks)

### Frontend
- React (Vite)
- Axios
- React Router

### Deployment
- Backend: Railway
- Frontend: Vercel

---

## 📌 API Endpoints

### Auth
- `POST /auth/signup`
- `POST /auth/login`
- `GET /auth/me`

### Billing
- `POST /billing/create-checkout`
- `GET /billing/status`

### Signals
- `GET /signals`

### Webhook
- `POST /webhook/stripe`

---

## 🔐 Environment Variables

### Backend (.env) (DO NOT COMMIT)
```env
DATABASE_URL=sqlite:///./app.db
JWT_SECRET=your_secret
REDIS_URL=redis://localhost:6379/0

STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

FRONTEND_URL=https://trading-signals-frontend.vercel.app


## 🧠 Architecture Diagram (Text)

User Browser (React + Vercel)
        |
        |  REST API Calls (JWT)
        v
FastAPI Backend (Railway)
        |
        |-- PostgreSQL/SQLite (User + Subscription Data)
        |
        |-- Redis Cache (Signals cache TTL 5 min)
        |-- Redis Rate-limit / Idempotency keys
        |
        |-- Stripe Checkout API (Create Session)
        |
        <--- Stripe Webhooks (checkout.session.completed)
                |
                v
        Backend updates user subscription -> Paid Access Enabled

