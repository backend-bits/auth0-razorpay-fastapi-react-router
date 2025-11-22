"""
Fullstack SAAS Template - FastAPI Backend
Main application file with Auth0 authentication and Razorpay payments
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from contextlib import asynccontextmanager

# Import our components
from auth0.dependencies import verify_token, get_current_user, require_subscription
from auth0.auth_actions import router as auth_actions_router
from razorpay.payment_manager import PaymentManager
from razorpay.webhook_handler import router as webhook_router
from razorpay.models import OrderCreate, OrderVerify

# Initialize payment manager
payment_manager = PaymentManager()

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting Fullstack SAAS Backend")
    print("✅ Auth0 integration ready")
    print("✅ Razorpay payment system ready")

    yield

    # Shutdown
    print("🛑 Shutting down Fullstack SAAS Backend")

# Create FastAPI app
app = FastAPI(
    title="Fullstack SAAS API",
    description="Complete SAAS backend with authentication and payments",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_actions_router)
app.include_router(webhook_router)

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Fullstack SAAS API",
        "version": "1.0.0",
        "docs": "/docs",
        "components": ["auth0", "razorpay"]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "auth0": "configured",
            "razorpay": "configured"
        }
    }

# Protected routes
@app.get("/api/profile")
async def get_profile(user = Depends(get_current_user)):
    """Get user profile (protected route)"""
    return {
        "user": user,
        "message": "Profile retrieved successfully"
    }

@app.get("/api/dashboard")
async def get_dashboard(user = Depends(get_current_user)):
    """Get dashboard data (protected route)"""
    return {
        "user": user,
        "dashboard": {
            "subscription_tier": user.get("subscription_tier", "free"),
            "is_paid": user.get("is_paid", False),
            "usage_stats": {
                "requests_today": 0,
                "requests_month": 0
            }
        }
    }

# Payment routes
@app.post("/api/payments/create-order")
async def create_payment_order(
    order_data: OrderCreate,
    user = Depends(get_current_user)
):
    """Create a payment order"""
    try:
        # Use user ID from token if not provided
        user_id = order_data.user_id or user.get("auth0_id")

        order = await payment_manager.create_order(
            plan_type=order_data.plan_type,
            user_id=user_id
        )

        return {
            "success": True,
            "order": order
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create order: {str(e)}"
        )

@app.post("/api/payments/verify")
async def verify_payment(
    verification: OrderVerify,
    user = Depends(get_current_user)
):
    """Verify payment after completion"""
    try:
        success = await payment_manager.verify_payment(verification)

        if success:
            return {
                "success": True,
                "message": "Payment verified successfully",
                "tier": payment_manager.get_plan_tier(verification.razorpay_order_id)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification error: {str(e)}"
        )

# Premium routes (subscription required)
@app.get("/api/premium/content")
@require_subscription("pro")
async def get_premium_content(user = Depends(get_current_user)):
    """Premium content endpoint"""
    return {
        "content": "This is premium content!",
        "user_tier": user.get("subscription_tier"),
        "access_granted": True
    }

@app.get("/api/analytics/usage")
@require_subscription("starter")
async def get_usage_analytics(user = Depends(get_current_user)):
    """Usage analytics (requires at least starter plan)"""
    return {
        "analytics": {
            "total_requests": 1250,
            "requests_this_month": 450,
            "subscription_tier": user.get("subscription_tier"),
            "plan_limits": payment_manager.get_plan_limits(user.get("subscription_tier", "free"))
        }
    }

# Admin routes (for future use)
@app.get("/api/admin/users")
async def get_users_admin(
    user = Depends(get_current_user)
    # TODO: Add admin role check
):
    """Admin endpoint to get all users"""
    # This would require admin role checking
    return {"message": "Admin endpoint - implement role checking"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )