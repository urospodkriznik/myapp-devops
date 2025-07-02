import os
from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.db import get_db
from app.models import User, Item, RoleEnum
from app.schemas import UserCreate, ItemCreate, UserLogin, TokenResponse
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response as StarletteResponse
from starlette.middleware.base import BaseHTTPMiddleware
from alembic.config import Config
from alembic import command
from app.auth import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from fastapi.security import OAuth2PasswordBearer
from app.dependencies import get_current_user, require_role
from loguru import logger
import time
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests")

# Configure Loguru for structured logging
logger.remove()
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
    level="INFO"
)
logger.add(
    lambda msg: print(msg, end=""),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(
            "Request started",
            extra={
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")
            }
        )
        
        try:
            response = await call_next(request)
            
            # Log response
            process_time = time.time() - start_time
            logger.info(
                "Request completed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": round(process_time, 4)
                }
            )
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "process_time": round(process_time, 4)
                }
            )
            raise

def create_app():
    app = FastAPI(
        title="MyApp API",
        description="A secure FastAPI application with monitoring and logging",
        version="1.0.0",
        docs_url="/docs" if os.getenv("ENVIRONMENT", "development") == "development" else None,
        redoc_url="/redoc" if os.getenv("ENVIRONMENT", "development") == "development" else None
    )

    # Add security middleware
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(LoggingMiddleware)
    
    # Add trusted host middleware for production
    if os.getenv("ENVIRONMENT") == "production":
        app.add_middleware(
            TrustedHostMiddleware, 
            allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
        )
        # Only enable HTTPS redirect in production
        if os.getenv("FORCE_HTTPS", "false").lower() == "true":
            app.add_middleware(HTTPSRedirectMiddleware)

    # @app.on_event("startup")
    # def run_migrations():
    #     try:
    #         logger.info("Starting application migrations...")
    #         config = Config("alembic.ini")
    #         command.upgrade(config, "head")
    #         logger.info("Migrations completed successfully")
    #     except Exception as e:
    #         logger.error(f"Migration failed: {e}")
    #         raise

    # Enhanced CORS configuration
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count"],
    )

    @app.middleware("http")
    async def count_requests(request, call_next):
        REQUEST_COUNT.inc()
        return await call_next(request)

    @app.get("/metrics")
    def metrics():
        data = generate_latest()
        return StarletteResponse(content=data, media_type=CONTENT_TYPE_LATEST)

    @app.post("/login", response_model=TokenResponse)
    async def login(
        user: UserLogin,
        session: AsyncSession = Depends(get_db),
        response: Response = None,
    ):
        logger.info(f"Login attempt for user: {user.email}")
        
        result = await session.execute(select(User).where(User.email == user.email))
        db_user = result.scalar_one_or_none()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            logger.warning(f"Failed login attempt for user: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token({"sub": str(db_user.id)})
        refresh_token = create_refresh_token({"sub": str(db_user.id)})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=os.getenv("ENVIRONMENT") == "production",
            samesite="lax",
            path="/refresh",
        )
        
        logger.info(f"Successful login for user: {user.email}")
        return {"access_token": access_token}

    @app.get("/refresh", response_model=TokenResponse)
    async def refresh_token(refresh_token: str = Cookie(None)):
        if not refresh_token:
            logger.warning("Refresh attempt without token")
            raise HTTPException(401, "Missing refresh token")

        user_id = decode_token(refresh_token)
        if not user_id:
            logger.warning("Invalid refresh token provided")
            raise HTTPException(401, "Invalid refresh token")

        new_access_token = create_access_token({"sub": user_id})
        logger.info(f"Token refreshed for user: {user_id}")
        return {"access_token": new_access_token}

    @app.post("/logout")
    async def logout(response: Response, current_user: User = Depends(get_current_user)):
        response.delete_cookie("refresh_token", path="/refresh")
        logger.info(f"User logged out: {current_user.email}")
        return {"ok": True}

    @app.get("/users", dependencies=[Depends(require_role(RoleEnum.ADMIN))])
    async def read_users(session: AsyncSession = Depends(get_db)):
        logger.info("Admin user list requested")
        result = await session.execute(select(User))
        users = result.scalars().all()
        return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

    @app.post("/register")
    async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
        logger.info(f"Registration attempt for user: {user.email}")
        
        result = await session.execute(select(User).where(User.email == user.email))
        if result.scalar_one_or_none():
            logger.warning(f"Registration failed - email already exists: {user.email}")
            raise HTTPException(400, detail="Email already registered")
        
        new_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role,
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        logger.info(f"User registered successfully: {user.email}")
        return {"id": new_user.id, "name": new_user.name, "email": new_user.email}

    @app.get("/me")
    async def get_me(current_user: User = Depends(get_current_user)):
        return {"id": current_user.id, "name": current_user.name, "email": current_user.email, "role": current_user.role.value}

    @app.delete("/users/{user_id}")
    async def delete_user(
        user_id: int, 
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(require_role(RoleEnum.ADMIN))
    ):
        logger.info(f"User deletion requested by admin {current_user.email} for user ID: {user_id}")
        
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            logger.warning(f"User deletion failed - user not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        await session.delete(user)
        await session.commit()
        
        logger.info(f"User deleted successfully: {user.email}")
        return {"ok": True}

    @app.get("/items")
    async def get_items(session: AsyncSession = Depends(get_db)):
        result = await session.execute(select(Item))
        items = result.scalars().all()
        return [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
            }
            for item in items
        ]

    @app.post("/items")
    async def create_item(
        item: ItemCreate, 
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        logger.info(f"Item creation requested by user: {current_user.email}")
        
        new_item = Item(name=item.name, description=item.description, price=item.price)
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)
        
        logger.info(f"Item created successfully: {new_item.name}")
        return {
            "id": new_item.id,
            "name": new_item.name,
            "description": new_item.description,
            "price": new_item.price,
        }

    @app.delete("/items/{item_id}")
    async def delete_item(
        item_id: int, 
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        logger.info(f"Item deletion requested by user {current_user.email} for item ID: {item_id}")
        
        result = await session.execute(select(Item).where(Item.id == item_id))
        item = result.scalar_one_or_none()
        if item is None:
            logger.warning(f"Item deletion failed - item not found: {item_id}")
            raise HTTPException(status_code=404, detail="Item not found")
        
        await session.delete(item)
        await session.commit()
        
        logger.info(f"Item deleted successfully: {item.name}")
        return {"ok": True}

    @app.get("/healthz")
    def health_check():
        return {"ok": True, "timestamp": time.time()}

    return app


app = create_app()