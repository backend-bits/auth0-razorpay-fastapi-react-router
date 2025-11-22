# Deployment Guide

This guide covers deploying the Fullstack SAAS Template to production environments.

## Backend Deployment

### Option 1: Vercel (Recommended)

1. **Connect Repository:**
   ```bash
   # Install Vercel CLI
   npm i -g vercel

   # Login to Vercel
   vercel login

   # Deploy from backend directory
   cd backend
   vercel --prod
   ```

2. **Environment Variables:**
   Set these in Vercel dashboard or using CLI:
   ```bash
   vercel env add AUTH0_DOMAIN
   vercel env add AUTH0_API_AUDIENCE
   vercel env add AUTH0_CLIENT_ID
   vercel env add AUTH0_CLIENT_SECRET
   vercel env add SERVICE_TOKEN
   vercel env add RAZORPAY_KEY_ID
   vercel env add RAZORPAY_KEY_SECRET
   vercel env add RAZORPAY_WEBHOOK_SECRET
   ```

3. **Vercel Configuration:**
   Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "main.py"
       }
     ]
   }
   ```

### Option 2: Railway

1. **Connect Repository:**
   - Go to Railway.app
   - Connect GitHub repository
   - Select the backend folder

2. **Environment Variables:**
   Set in Railway dashboard under "Variables"

3. **Database:**
   - Add PostgreSQL plugin
   - Update DATABASE_URL

### Option 3: DigitalOcean App Platform

1. **Create App:**
   - Connect GitHub repository
   - Set source directory to `backend`

2. **Environment Variables:**
   Configure in App settings

3. **Database:**
   - Add managed PostgreSQL database
   - Configure connection string

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Deploy Frontend:**
   ```bash
   cd frontend
   vercel --prod
   ```

2. **Environment Variables:**
   ```bash
   vercel env add VITE_AUTH0_DOMAIN
   vercel env add VITE_AUTH0_CLIENT_ID
   vercel env add VITE_AUTH0_AUDIENCE
   vercel env add VITE_API_BASE_URL
   ```

### Option 2: Netlify

1. **Connect Repository:**
   - Go to Netlify dashboard
   - Connect GitHub repository
   - Set build command: `npm run build`
   - Set publish directory: `dist`

2. **Environment Variables:**
   Set in Netlify dashboard under "Site settings" → "Environment variables"

## Database Setup

### Supabase (Recommended)

1. **Create Project:**
   - Go to supabase.com
   - Create new project

2. **Database Schema:**
   Run the following SQL in Supabase SQL Editor:
   ```sql
   -- Users table
   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     auth0_id VARCHAR(255) UNIQUE NOT NULL,
     email VARCHAR(255) UNIQUE,
     name VARCHAR(255),
     subscription_tier VARCHAR(50) DEFAULT 'free',
     is_paid BOOLEAN DEFAULT FALSE,
     is_active BOOLEAN DEFAULT TRUE,
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );

   -- Subscriptions table
   CREATE TABLE subscriptions (
     id SERIAL PRIMARY KEY,
     user_id INTEGER REFERENCES users(id),
     subscription_id VARCHAR(255),
     tier VARCHAR(50),
     status VARCHAR(50),
     valid_until TIMESTAMP,
     last_charged TIMESTAMP,
     created_at TIMESTAMP DEFAULT NOW()
   );

   -- Security events table
   CREATE TABLE security_events (
     id SERIAL PRIMARY KEY,
     user_id INTEGER REFERENCES users(id),
     event_type VARCHAR(100),
     ip_address INET,
     user_agent TEXT,
     metadata JSONB,
     timestamp TIMESTAMP DEFAULT NOW()
   );
   ```

3. **Environment Variables:**
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_key
   ```

### Alternative: PlanetScale

1. **Create Database:**
   - Go to planetscale.com
   - Create new database

2. **Schema Migration:**
   Use PlanetScale CLI or dashboard to create tables

## Redis Setup

### Redis Cloud (Recommended)

1. **Create Redis Instance:**
   - Go to redis.com/cloud
   - Create free tier instance

2. **Environment Variable:**
   ```
   REDIS_URL=redis://username:password@host:port
   ```

### Alternative: Upstash

1. **Create Database:**
   - Go to upstash.com
   - Create Redis database

2. **Connection String:**
   Use the provided connection string

## Auth0 Production Setup

1. **Update Application Settings:**
   - Change callback URLs to production domain
   - Update logout URLs
   - Update allowed origins

2. **Create Production API:**
   - Duplicate your API settings
   - Update audience to production URL

3. **Environment Variables:**
   Update all Auth0 variables to production values

## Razorpay Production Setup

1. **Complete KYC:**
   - Upload documents in Razorpay dashboard
   - Wait for verification

2. **Generate Live Keys:**
   - Switch to live mode
   - Generate live API keys

3. **Update Webhooks:**
   - Change webhook URL to production domain
   - Ensure HTTPS certificate is valid

4. **Environment Variables:**
   Update to live Razorpay credentials

## Domain Configuration

### Custom Domain Setup

1. **Frontend Domain:**
   - Configure DNS to point to Vercel/Netlify
   - Update Auth0 allowed origins

2. **Backend Domain:**
   - Configure DNS to point to your backend host
   - Update CORS origins in FastAPI

3. **SSL Certificates:**
   - Automatic with Vercel/Netlify
   - Manual configuration for other providers

## Auth0 Production Management

### Production Application Setup
1. **Create Production Application**:
   - Go to [Auth0 Dashboard](https://manage.auth0.com)
   - Create new "Regular Web Application"
   - Configure production domains and URLs

2. **Production API Configuration**:
   - Create production API with proper audience
   - Set appropriate token expiration times
   - Configure production permissions

3. **Domain Configuration**:
   - Use custom domain if available
   - Configure SSL certificates
   - Update DNS settings

### Auth0 Security Best Practices
- **Rotate Secrets**: Regularly rotate client secrets
- **Monitor Logs**: Set up alerts for suspicious activities
- **Configure MFA**: Enable Multi-Factor Authentication
- **Rate Limiting**: Implement appropriate rate limits

**📖 Official Auth0 Production Guide**: [Auth0 Production Checklist](https://auth0.com/docs/deploy/checklist)

## Razorpay Production Management

### Production Account Setup
1. **Complete KYC Verification**:
   - Submit all required documents
   - Wait for approval (typically 1-2 business days)
   - Enable live mode

2. **Live API Keys**:
   - Generate live key pair from dashboard
   - Update environment variables
   - Test thoroughly before going live

3. **Production Webhooks**:
   - Update webhook URLs to production domain
   - Ensure HTTPS certificates are valid
   - Test webhook delivery

### Razorpay Compliance & Security
- **PCI DSS Compliance**: Razorpay handles PCI compliance
- **Data Encryption**: All payment data is encrypted
- **Fraud Detection**: Enable Razorpay's fraud detection
- **Chargeback Management**: Set up chargeback notification alerts

**📖 Official Razorpay Production Guide**: [Razorpay Go Live Checklist](https://razorpay.com/docs/payment-gateway/go-live/)

### Payment Method Configuration
```javascript
// Production payment options
const options = {
  key: 'rzp_live_your_key_id',
  amount: 29900,
  currency: 'INR',
  name: 'Your SAAS App',
  description: 'Pro Plan Subscription',
  order_id: orderId,
  handler: function (response) {
    // Handle successful payment
    verifyPayment(response);
  },
  prefill: {
    name: customer.name,
    email: customer.email,
    contact: customer.phone
  },
  theme: {
    color: '#3399cc'
  }
};
```

## Environment Variables Summary

### Backend (.env) - Production
```env
# Auth0 Production
AUTH0_DOMAIN=your-prod-tenant.auth0.com
AUTH0_API_AUDIENCE=https://api.yourdomain.com
AUTH0_CLIENT_ID=your-prod-client-id
AUTH0_CLIENT_SECRET=your-prod-client-secret
SERVICE_TOKEN=secure-random-prod-token

# Razorpay Production
RAZORPAY_KEY_ID=rzp_live_your_live_key_id
RAZORPAY_KEY_SECRET=your_live_secret
RAZORPAY_WEBHOOK_SECRET=your_live_webhook_secret

# Database Production
SUPABASE_URL=https://your-prod-project.supabase.co
SUPABASE_ANON_KEY=your-prod-anon-key
SUPABASE_SERVICE_KEY=your-prod-service-key

# Redis Production
REDIS_URL=redis://username:password@your-redis-host:6379

# App Settings
FRONTEND_URL=https://yourdomain.com
ENVIRONMENT=production
```

### Frontend (.env.production) - Production
```env
VITE_AUTH0_DOMAIN=your-prod-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-prod-client-id
VITE_AUTH0_AUDIENCE=https://api.yourdomain.com
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_ENVIRONMENT=production
```

### Frontend (.env.local)
```env
VITE_AUTH0_DOMAIN=your-tenant.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_AUTH0_AUDIENCE=https://api.yourdomain.com
VITE_API_BASE_URL=https://api.yourdomain.com
```

## Monitoring & Analytics

### Backend Monitoring
- **Sentry:** Error tracking
- **DataDog:** Application monitoring
- **Prometheus:** Metrics collection

### Frontend Monitoring
- **Vercel Analytics:** Built-in analytics
- **Google Analytics:** User behavior tracking
- **Sentry:** Error tracking

### Database Monitoring
- **Supabase Dashboard:** Built-in monitoring
- **DataDog Database Monitoring:** Advanced metrics

## Security Checklist

- [ ] HTTPS enabled on all domains
- [ ] Environment variables not committed to git
- [ ] API keys rotated regularly
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation in place
- [ ] Authentication required for sensitive endpoints
- [ ] Webhook signatures verified
- [ ] Database backups configured

## Performance Optimization

### Backend
- Enable Redis caching
- Use connection pooling
- Implement rate limiting
- Optimize database queries
- Use async/await properly

### Frontend
- Enable code splitting
- Optimize images
- Use CDN for static assets
- Implement lazy loading
- Enable compression

## Backup Strategy

### Database Backups
- **Supabase:** Automatic daily backups
- **PlanetScale:** Point-in-time recovery
- **Manual:** Regular pg_dump exports

### Code Backups
- Git repository as source of truth
- Regular releases/tags
- Documentation versioning

## Troubleshooting

### Common Issues

1. **CORS Errors:**
   - Check allowed origins in FastAPI CORS settings
   - Verify Auth0 application origins

2. **Authentication Failures:**
   - Verify Auth0 domain and audience
   - Check JWT token expiration
   - Validate client credentials

3. **Payment Issues:**
   - Confirm Razorpay live credentials
   - Check webhook URL accessibility
   - Verify webhook signature

4. **Database Connection:**
   - Check connection string format
   - Verify firewall rules
   - Confirm credentials

### Logs & Debugging

- **Backend:** Check Vercel/Railway logs
- **Frontend:** Browser developer tools
- **Database:** Supabase dashboard
- **Auth0:** Auth0 dashboard logs
- **Razorpay:** Razorpay dashboard

## Cost Optimization

### Hosting Costs
- **Vercel:** Generous free tier, pay per usage
- **Supabase:** Free tier for small projects
- **Redis Cloud:** Free tier available

### Scaling Considerations
- Monitor usage patterns
- Implement caching strategies
- Use CDN for static assets
- Optimize database queries

## Support

- [Auth0 Documentation](https://auth0.com/docs)
- [Razorpay Documentation](https://razorpay.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Router Documentation](https://reactrouter.com)
- [Vercel Documentation](https://vercel.com/docs)