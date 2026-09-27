from pathlib import Path

readme = r"""# 🛒 E-Commerce Microservices Backend

A scalable **microservices-based e-commerce backend** built with **FastAPI, MySQL, SQLAlchemy, JWT Authentication, API Gateway, Docker, Docker Compose, Aiven, and Vercel**.

The project separates authentication, products, and orders into independent services. Each service owns its own database and communicates with other services through APIs.

---

## 🚀 Live Deployment

### API Gateway
https://ecommerce-microservices-a4zs.vercel.app/docs

### Auth Service
https://auth-service-ebon.vercel.app/docs

### Product Service
https://product-service-sandy.vercel.app/docs

### Order Service
https://order-service-ilqjj49dq-none-705d.vercel.app/docs

---

## 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │      API Gateway        │
                    │        FastAPI          │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
      ┌──────────────┐  ┌───────────────┐ ┌──────────────┐
      │ Auth Service │  │Product Service│ │ Order Service│
      │    :8001     │  │    :8002      │ │    :8003    │
      └──────┬───────┘  └──────┬────────┘ └──────┬───────┘
             │                  │                  │
             ▼                  ▼                  ▼
        ┌─────────┐        ┌───────────┐      ┌──────────┐
        │ auth_db │        │ product_db│      │ order_db │
        └─────────┘        └───────────┘      └──────────┘
