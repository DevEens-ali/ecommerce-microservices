# 🛒 E-Commerce Microservices Backend

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
```

### Architecture Principles

- Independent microservices
- Database-per-service pattern
- API Gateway as a single client entry point
- HTTP-based service-to-service communication
- JWT-based authentication
- Environment-based configuration
- Independent deployment of services

---

## ✨ Features

### 🔐 Authentication Service

- User registration
- User login
- Password hashing with bcrypt
- JWT token generation
- Protected `/auth/me` endpoint
- Duplicate email validation
- Authentication middleware

### 📦 Product Service

- Create products
- Get all products
- Get product by ID
- Update products
- Delete products
- Pydantic input validation
- Product quantity/stock management

### 🛒 Order Service

- Create orders
- Get authenticated user's orders
- Get order by ID
- Update order status
- Delete orders
- JWT-protected endpoints
- Product existence validation
- Stock availability validation
- Automatic total price calculation
- Product Service communication through HTTP

### 🚪 API Gateway

Routes client requests to the appropriate service:

```text
/auth/*       → Auth Service
/products/*   → Product Service
/orders/*     → Order Service
```

The client can use the Gateway instead of communicating directly with every service.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST APIs and microservices |
| SQLAlchemy | ORM and database operations |
| MySQL | Relational database |
| Aiven | Cloud MySQL hosting |
| Pydantic | Request/response validation |
| JWT / PyJWT | Authentication |
| bcrypt | Password hashing |
| HTTPX | Service-to-service communication |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |
| Vercel | Cloud deployment |
| Swagger / OpenAPI | API documentation |

---

## 📁 Project Structure

```text
ecommerce-microservices/
│
├── api-gateway/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── vercel.json
│
├── auth-service/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       └── auth.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── vercel.json
│
├── product-service/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       └── products.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── vercel.json
│
├── order-service/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── routers/
│   │       └── orders.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── vercel.json
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🔄 Service Communication

The Order Service communicates with the Product Service before creating an order.

```text
Client
  │
  ▼
API Gateway
  │
  ▼
Order Service
  │
  │ HTTP Request
  ▼
Product Service
  │
  ▼
Product Database
```

### Order Creation Flow

1. Client sends product ID and quantity.
2. Order Service validates the JWT.
3. Order Service requests the product from Product Service.
4. Product Service returns product information.
5. Order Service checks product stock.
6. Order Service calculates the total price.
7. Order is stored in `order_db`.

The Order Service does **not** directly access the Product Service database.

---

## 🔐 Authentication Flow

```text
Register
   │
   ▼
Auth Service
   │
   ▼
User stored in auth_db
   │
   ▼
Login
   │
   ▼
JWT Access Token
   │
   ▼
Authorization: Bearer <token>
   │
   ▼
Protected Endpoint
```

The JWT contains the authenticated user's identity and is validated by protected services.

---

## 🗄️ Database Architecture

Each service has its own database.

```text
Auth Service
    └── auth_db
         └── users

Product Service
    └── product_db
         └── products

Order Service
    └── order_db
         └── orders
```

This follows the **Database-per-Service** microservices pattern.

There are no direct cross-service database relationships. Services communicate through APIs instead.

---

## 🔑 Environment Variables

Sensitive configuration is stored in environment variables instead of source code.

### Auth Service

```env
DATABASE_URL=your_auth_database_url
SECRET_KEY=your_secret_key
```

### Product Service

```env
DATABASE_URL=your_product_database_url
```

### Order Service

```env
DATABASE_URL=your_order_database_url
SECRET_KEY=your_secret_key
PRODUCT_SERVICE_URL=your_product_service_url
```

### API Gateway

```env
AUTH_SERVICE_URL=your_auth_service_url
PRODUCT_SERVICE_URL=your_product_service_url
ORDER_SERVICE_URL=your_order_service_url
```

> ⚠️ Never commit real database passwords, JWT secrets, API keys, or other credentials to GitHub.

---

## 🧪 API Endpoints

### Authentication

```text
POST /auth/register
POST /auth/login
GET  /auth/me
```

### Products

```text
POST   /products/
GET    /products/
GET    /products/{product_id}
PUT    /products/{product_id}
DELETE /products/{product_id}
```

### Orders

```text
POST   /orders/
GET    /orders/
GET    /orders/{order_id}
PUT    /orders/{order_id}
DELETE /orders/{order_id}
```

---

## 📚 Swagger Documentation

Each service provides interactive OpenAPI/Swagger documentation.

### API Gateway

https://ecommerce-microservices-a4zs.vercel.app/docs

### Auth Service

https://auth-service-ebon.vercel.app/docs

### Product Service

https://product-service-sandy.vercel.app/docs

### Order Service

https://order-service-ilqjj49dq-none-705d.vercel.app/docs

---

## 🐳 Docker

The project includes Dockerfiles for each service and a Docker Compose configuration for running the microservices architecture locally.

### Clone the repository

```bash
git clone https://github.com/DevEens-ali/ecommerce-microservices.git
cd ecommerce-microservices
```

### Start the project

```bash
docker-compose up --build
```

### Local Services

```text
API Gateway  → http://localhost:8000
Auth Service → http://localhost:8001
Product      → http://localhost:8002
Order        → http://localhost:8003
```

### Stop containers

```bash
docker-compose down
```

---

## 🔧 Local Development

Each service can also be run independently.

### Auth Service

```bash
cd auth-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

### Product Service

```bash
cd product-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

### Order Service

```bash
cd order-service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

### API Gateway

```bash
cd api-gateway
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## 🎯 Project Goals

This project was developed to gain practical experience with:

- Microservices architecture
- REST API development
- API Gateway patterns
- Service-to-service communication
- Database-per-service architecture
- JWT authentication
- Password hashing
- Input validation
- Docker containerization
- Docker Compose
- Cloud database integration
- Environment-based configuration
- Cloud deployment
- API testing and debugging

---

## 🧠 What I Learned

During development, I learned how to:

- Design independent backend services.
- Separate authentication, products, and orders into individual services.
- Implement JWT-based authentication.
- Hash and verify user passwords securely.
- Connect individual services to separate MySQL databases.
- Communicate between microservices using HTTPX.
- Build an API Gateway for centralized routing.
- Manage production environment variables.
- Deploy multiple FastAPI services independently.
- Debug cloud deployment issues.
- Resolve missing production dependencies.
- Structure a backend project for scalability and maintainability.

---

## ⚠️ Challenges Faced

### Database Configuration

Configuring independent database connections for each microservice required separate connection strings and database configurations.

### Service-to-Service Communication

The Order Service needed product information without directly accessing the Product database. This was handled through HTTP communication with the Product Service.

### JWT Authentication

JWT authentication had to be implemented and validated for protected endpoints such as order operations.

### Environment Variables

Local development used localhost service URLs, while production required deployed service URLs. Environment variables were used to manage this difference.

### Vercel Deployment

Each FastAPI service required its own Vercel configuration and deployment setup.

### Dependency Issue

During Order Service deployment, the application initially failed because the `PyJWT` dependency was not available in the deployment environment. Adding the dependency to `requirements.txt` resolved the runtime import error.

### Docker

Docker and Docker Compose were configured as part of the project architecture. Local container testing also involved troubleshooting Docker environment and image-storage issues.

---

## 🚀 Future Improvements

Possible future improvements include:

- Redis caching
- Centralized logging
- Health-check endpoints
- Rate limiting
- API versioning
- Async database operations
- Message broker integration
- Background jobs
- Kubernetes deployment
- CI/CD pipeline
- Dedicated Inventory Service
- Payment Service
- Notification Service
- Monitoring and observability

---

## 👨‍💻 Author

### Anees Ali

Software Engineering Student  
Backend / Full Stack Developer

- GitHub: https://github.com/DevEens-ali
- LinkedIn: https://linkedin.com/in/anees-ali-201633286

---

## 📄 License

This project was developed for educational and internship purposes.
