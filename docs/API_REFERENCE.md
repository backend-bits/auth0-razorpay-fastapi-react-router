# API Reference

This document provides detailed information about the Fullstack SAAS Template API endpoints, integrated with Auth0 authentication and Razorpay payments.

## 🔐 Authentication Overview

This template uses **Auth0** for authentication and **JWT tokens** for API authorization.

### Auth0 Integration Details
- **Token Type**: JWT (JSON Web Tokens)
- **Algorithm**: RS256 (RSA Signature)
- **Issuer**: `https://your-tenant.auth0.com/`
- **Audience**: Your API identifier (e.g., `https://api.yourapp.com`)

**📖 Auth0 API Documentation**: [Auth0 Authentication API](https://auth0.com/docs/api/authentication)

### JWT Token Structure
```json
{
  "iss": "https://your-tenant.auth0.com/",
  "sub": "auth0|123456789",
  "aud": "https://api.yourapp.com",
  "iat": 1640995200,
  "exp": 1641081600,
  "scope": "openid profile email",
  "permissions": ["read:users", "create:users"]
}
```

## 💳 Payment Overview

This template uses **Razorpay** for payment processing and subscription management.

### Razorpay Integration Details
- **Supported Currencies**: INR (primary), USD, EUR, GBP
- **Payment Methods**: Cards, UPI, Net Banking, Wallets
- **Webhook Signature**: HMAC-SHA256
- **Settlement**: T+1 for domestic payments

**📖 Razorpay API Documentation**: [Razorpay Payment API](https://razorpay.com/docs/api/)

### Supported Payment Flow
1. **Order Creation** → 2. **Payment** → 3. **Verification** → 4. **Subscription Activation**

## Authentication Endpoints

### POST `/api/auth/login`
Auth0 handles authentication - this endpoint is not directly called.

### GET `/api/profile`
Get current user profile information.

**Authentication:** Required (JWT token)

**Response:**
```json
{
  "user": {
    "auth0_id": "auth0|123456",
    "email": "user@example.com",
    "name": "John Doe",
    "subscription_tier": "pro",
    "is_paid": true
  },
  "message": "Profile retrieved successfully"
}
```

### GET `/api/dashboard`
Get user dashboard data including usage statistics.

**Authentication:** Required (JWT token)

**Response:**
```json
{
  "user": { ... },
  "dashboard": {
    "subscription_tier": "pro",
    "is_paid": true,
    "usage_stats": {
      "requests_today": 150,
      "requests_month": 2500
    }
  }
}
```

## Payment Endpoints

### POST `/api/payments/create-order`
Create a new payment order for subscription.

**Authentication:** Required (JWT token)

**Request Body:**
```json
{
  "plan_type": "plan_pro_monthly",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "success": true,
  "order": {
    "order_id": "order_xyz123",
    "amount": 29900,
    "currency": "INR",
    "key_id": "rzp_test_xxx",
    "plan_type": "plan_pro_monthly",
    "plan_name": "Pro Plan",
    "tier": "pro"
  }
}
```

### POST `/api/payments/verify`
Verify payment after successful completion.

**Authentication:** Required (JWT token)

**Request Body:**
```json
{
  "razorpay_payment_id": "pay_xxx",
  "razorpay_order_id": "order_xxx",
  "razorpay_signature": "signature_xxx"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "tier": "pro"
}
```

## Premium Content Endpoints

### GET `/api/premium/content`
Access premium content (requires Pro subscription).

**Authentication:** Required (JWT token + Pro subscription)

**Response:**
```json
{
  "content": "This is premium content!",
  "user_tier": "pro",
  "access_granted": true
}
```

### GET `/api/analytics/usage`
Get detailed usage analytics (requires at least Starter subscription).

**Authentication:** Required (JWT token + Starter+ subscription)

**Response:**
```json
{
  "analytics": {
    "total_requests": 1250,
    "requests_this_month": 450,
    "subscription_tier": "pro",
    "plan_limits": {
      "requests_per_day": -1,
      "tokens_per_day": -1,
      "requests_per_month": 2000,
      "tokens_per_month": 2000000
    }
  }
}
```

## Auth0 Action Endpoints

### POST `/api/analytics/signup`
Called by Auth0 Actions on user registration.

**Authentication:** Service token required

### POST `/api/analytics/login`
Called by Auth0 Actions on user login.

**Authentication:** Service token required

### POST `/api/security/events`
Log security events from Auth0 Actions.

**Authentication:** Service token required

## Webhook Endpoints

### POST `/webhooks/razorpay`
Razorpay webhook for payment events.

**Authentication:** Razorpay signature verification

**Supported Events:**
- `subscription.activated`
- `subscription.charged`
- `subscription.cancelled`
- `payment.captured`
- `payment.failed`

## Error Responses

All endpoints return standardized error responses:

```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### Common HTTP Status Codes
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized (invalid/missing token)
- `402` - Payment Required (subscription needed)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## Rate Limiting

API endpoints are protected by rate limiting:
- General endpoints: 100 requests per minute
- Payment endpoints: 10 requests per minute
- Auth endpoints: 5 requests per minute

## CORS

The API allows requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)
- Production domains (configure in CORS settings)

## Authentication Flow

1. **Frontend** calls Auth0 for authentication
2. **Auth0** returns JWT token
3. **Frontend** includes token in `Authorization: Bearer <token>` header
4. **Backend** verifies token using Auth0 JWKS
5. **Backend** checks subscription tier for premium endpoints
6. **Response** returned based on authentication and authorization

## Auth0 Management APIs

### User Management
```javascript
// Get user profile
GET https://your-tenant.auth0.com/api/v2/users/{user_id}

// Update user metadata
PATCH https://your-tenant.auth0.com/api/v2/users/{user_id}
{
  "user_metadata": {
    "subscription_tier": "pro",
    "preferences": { "theme": "dark" }
  }
}

// Get user roles
GET https://your-tenant.auth0.com/api/v2/users/{user_id}/roles
```

### Application Management
```javascript
// Get application details
GET https://your-tenant.auth0.com/api/v2/clients/{client_id}

// Update application settings
PATCH https://your-tenant.auth0.com/api/v2/clients/{client_id}
{
  "callbacks": ["https://yourdomain.com/callback"],
  "allowed_origins": ["https://yourdomain.com"]
}
```

**📖 Auth0 Management API**: [Auth0 Management API Reference](https://auth0.com/docs/api/management/v2)

## Razorpay Payment APIs

### Orders API
```javascript
// Create order
POST https://api.razorpay.com/v1/orders
{
  "amount": 29900,
  "currency": "INR",
  "receipt": "order_rcptid_11",
  "notes": {
    "user_id": "user_123",
    "plan_type": "pro_monthly"
  }
}

// Fetch order
GET https://api.razorpay.com/v1/orders/{order_id}
```

### Payments API
```javascript
// Fetch payment details
GET https://api.razorpay.com/v1/payments/{payment_id}

// Capture payment (for manual capture)
POST https://api.razorpay.com/v1/payments/{payment_id}/capture
{
  "amount": 29900,
  "currency": "INR"
}

// Create refund
POST https://api.razorpay.com/v1/payments/{payment_id}/refund
{
  "amount": 5000,
  "notes": {
    "reason": "Customer request"
  }
}
```

### Subscriptions API
```javascript
// Create subscription
POST https://api.razorpay.com/v1/subscriptions
{
  "plan_id": "plan_pro_monthly",
  "customer_id": "cust_123",
  "total_count": 12,
  "start_at": 1640995200
}

// Cancel subscription
POST https://api.razorpay.com/v1/subscriptions/{subscription_id}/cancel

// Fetch subscription details
GET https://api.razorpay.com/v1/subscriptions/{subscription_id}
```

**📖 Razorpay API Reference**: [Razorpay API Documentation](https://razorpay.com/docs/api/)

## Webhook Specifications

### Auth0 Webhooks
Auth0 sends events to your configured webhook URLs:

```json
{
  "type": "user.created",
  "data": {
    "user": {
      "user_id": "auth0|123456",
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

### Razorpay Webhooks
Razorpay sends payment events with HMAC signatures:

```json
{
  "event": "payment.captured",
  "data": {
    "payment": {
      "id": "pay_123456789",
      "amount": 29900,
      "currency": "INR",
      "status": "captured",
      "order_id": "order_123456789"
    }
  }
}
```

**Webhook Signature Verification:**
```javascript
const crypto = require('crypto');
const expectedSignature = crypto
  .createHmac('sha256', webhookSecret)
  .update(JSON.stringify(payload))
  .digest('hex');
```

## Testing

Use the following test tokens for development:

### Auth0 Test Users
Create test users in Auth0 Dashboard under "User Management" → "Users"

### Razorpay Test Mode
Use test API keys and test cards:
- Success: `4111 1111 1111 1111`
- Failure: `4000 0000 0000 0002`
- Insufficient funds: `4000 0000 0000 0002`
- UPI Success: `success@razorpay`
- UPI Failure: `failure@razorpay`