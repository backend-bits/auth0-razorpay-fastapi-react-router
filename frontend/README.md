# Fullstack Template Frontend

A modern React application with TypeScript, React Router, and Auth0 integration.

## Features

- **React 18** with TypeScript
- **React Router** for client-side routing
- **Auth0** authentication
- **Tailwind CSS** for styling
- **Payment integration** with Razorpay
- **Protected routes** and role-based access
- **Modern development** with Vite

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
Create a `.env.local` file:
```env
VITE_AUTH0_DOMAIN=your-auth0-domain.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_AUTH0_AUDIENCE=https://api.yourapp.com
VITE_API_BASE_URL=http://localhost:8000
```

3. Start the development server:
```bash
npm run dev
```

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── auth/           # Authentication components
│   ├── payments/       # Payment components
│   ├── layout/         # Layout components
│   └── ui/             # UI components
├── pages/              # Page components
│   ├── Home.tsx
│   ├── Dashboard.tsx
│   ├── Pricing.tsx
│   ├── Profile.tsx
│   └── Login.tsx
├── hooks/              # Custom hooks
├── lib/                # Utilities and API clients
├── types/              # TypeScript types
└── main.tsx           # Application entry point
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Key Components

### Authentication
- Login/logout functionality
- Protected routes
- User profile management
- Auth0 integration

### Payments
- Subscription plans display
- Razorpay checkout integration
- Payment verification
- Usage tracking

### Routing
- Public and protected routes
- Role-based access control
- Nested routing support