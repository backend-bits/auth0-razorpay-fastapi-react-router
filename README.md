# Fullstack SAAS Template

A complete fullstack SAAS application template with authentication, payments, and modern frontend/backend architecture.

## 🚀 Features

### Backend (FastAPI)
- **Auth0 Authentication**: JWT verification, user management, Auth0 Actions integration
- **Razorpay Payments**: Subscription management, webhook handling, payment verification
- **Database Integration**: Supabase with Redis caching
- **Security**: Rate limiting, CORS, input validation
- **API Documentation**: Auto-generated Swagger/OpenAPI docs

### Frontend (React + React Router)
- **Modern React**: TypeScript, hooks, context
- **React Router**: Client-side routing with protected routes
- **Auth0 Integration**: Login/logout, user management
- **Payment Integration**: Razorpay checkout, subscription management
- **UI Components**: Responsive design with Tailwind CSS
- **State Management**: React Context + custom hooks

## 📁 Project Structure

```
fullstack-template/
├── backend/                    # FastAPI backend
│   ├── auth0/                 # Auth0 authentication components
│   ├── razorpay/              # Razorpay payment components
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend setup guide
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── components/        # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom hooks
│   │   ├── lib/              # Utilities and API clients
│   │   └── types/            # TypeScript types
│   ├── package.json
│   └── README.md              # Frontend setup guide
└── docs/                      # Documentation
    ├── MODIFICATION_GUIDE.md  # How to customize templates
    ├── API_REFERENCE.md       # API documentation
    └── DEPLOYMENT.md          # Deployment instructions
```

## 🛠 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Auth0 account
- Razorpay account
- Supabase account (optional)
- Redis instance (optional)

### 1. Clone and Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Setup Frontend
```bash
cd frontend
npm install
```

### 3. Set Up Auth0 Account & Application
Follow the detailed Auth0 setup guide: [Auth0 Setup Guide](docs/MODIFICATION_GUIDE.md#auth0-setup)

**Quick Auth0 Setup Steps:**
1. **Create Account**: Go to [auth0.com](https://auth0.com) and sign up
2. **Create Application**:
   - Choose "Regular Web Application"
   - Set callback URLs: `http://localhost:5173` (dev), your production domain
   - Note: Domain, Client ID, Client Secret
3. **Create API**:
   - Identifier: `https://api.yourapp.com`
   - Signing Algorithm: RS256
4. **Configure Permissions**: Add `read:users`, `create:users`, etc.
5. **Optional - Auth0 Actions**: Set up login/logout tracking

**📖 Official Auth0 Documentation**: [Auth0 Docs](https://auth0.com/docs?tenant=dev-kosuthubha%40prod-us-5&locale=en-us)
- [Quick Start Guide](https://auth0.com/docs/quickstarts)
- [API Authorization](https://auth0.com/docs/get-started/apis)
- [Auth0 Actions](https://auth0.com/docs/actions)
- [JWT Verification](https://auth0.com/docs/secure/tokens/json-web-tokens)

### 4. Set Up Razorpay Account & Integration
Follow the detailed Razorpay setup guide: [Razorpay Setup Guide](docs/MODIFICATION_GUIDE.md#razorpay-setup)

**Quick Razorpay Setup Steps:**
1. **Create Account**: Go to [razorpay.com](https://razorpay.com) and sign up
2. **Complete KYC**: Skip for test mode, required for live mode
3. **Generate API Keys**:
   - Start with **Test Mode** for development
   - Note: Key ID (`rzp_test_xxx`) and Key Secret
4. **Set Up Webhooks**:
   - URL: `https://yourdomain.com/webhooks/razorpay`
   - Events: `subscription.activated`, `subscription.charged`, `payment.captured`
5. **Create Plans**: Set up subscription plans in Razorpay dashboard

**📖 Official Razorpay Documentation**: [Razorpay Docs](https://razorpay.com/docs/)
- [Payment Gateway Integration](https://razorpay.com/docs/payment-gateway)
- [Subscriptions API](https://razorpay.com/docs/subscriptions)
- [Webhooks Guide](https://razorpay.com/docs/webhooks)
- [Test Mode Guide](https://razorpay.com/docs/payments/test-mode)

**Test Credentials for Development:**
- **Test Cards**: `4111 1111 1111 1111` (success), `4000 0000 0000 0002` (failure)
- **Test UPI**: `success@razorpay` (success), `failure@razorpay` (failure)

### 5. Configure Environment Variables
Copy the environment files and update with your credentials:

**Backend (.env):**
```env
# Auth0 Configuration (from Auth0 Dashboard)
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_API_AUDIENCE=https://api.yourapp.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
SERVICE_TOKEN=your-secure-service-token

# Razorpay Configuration (from Razorpay Dashboard)
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Database (Optional)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-anon-key
REDIS_URL=redis://localhost:6379
```

**Frontend (.env.local):**
```env
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_AUTH0_AUDIENCE=https://api.yourapp.com
VITE_API_BASE_URL=http://localhost:8000
```

### 5. Run the Application
```bash
# Terminal 1: Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit `http://localhost:5173` to see your application!

## 🔧 Development

### Backend Development
```bash
cd backend
# Run tests
pytest

# Run with auto-reload
uvicorn main:app --reload

# View API docs
# Visit http://localhost:8000/docs
```

### Frontend Development
```bash
cd frontend
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📚 Documentation

- [Modification Guide](docs/MODIFICATION_GUIDE.md) - Customize the templates
- [API Reference](docs/API_REFERENCE.md) - Backend API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

## 🔐 Authentication Flow

1. **User Login**: Auth0 handles authentication
2. **JWT Verification**: Backend validates tokens
3. **User Sync**: User data synced to database
4. **Subscription Check**: Payment status verified
5. **Access Granted**: Protected routes accessible

## 💳 Payment Flow

1. **Plan Selection**: User chooses subscription
2. **Order Creation**: Backend creates Razorpay order
3. **Payment**: User completes payment on Razorpay
4. **Verification**: Backend verifies payment signature
5. **Subscription Update**: User subscription activated
6. **Webhook Confirmation**: Razorpay confirms via webhook

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Test with test credentials
# Use Razorpay test mode
# Use Auth0 test users
```

## 🚀 Deployment

### Backend Deployment
- **Recommended**: Vercel, Railway, or Render
- **Database**: Supabase or PlanetScale
- **Cache**: Redis Cloud or Upstash

### Frontend Deployment
- **Recommended**: Vercel, Netlify, or Cloudflare Pages
- **CDN**: Automatic with modern hosting platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- [Auth0 Documentation](https://auth0.com/docs)
- [Razorpay Documentation](https://razorpay.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Router Documentation](https://reactrouter.com)

---

Built with ❤️ using modern web technologies