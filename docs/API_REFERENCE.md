# API Reference

This document provides detailed information about the Fullstack SAAS Template API endpoints.

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

## Testing

Use the following test tokens for development:

### Auth0 Test Users
Create test users in Auth0 Dashboard under "User Management" → "Users"

### Razorpay Test Mode
Use test API keys and test cards:
- Success: `4111 1111 1111 1111`
- Failure: `4000 0000 0000 0002`
- UPI Success: `success@razorpay`