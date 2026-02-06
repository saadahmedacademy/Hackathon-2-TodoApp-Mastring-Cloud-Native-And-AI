# Quickstart Guide: Frontend Web Application

## Prerequisites
- Node.js 18+ installed
- Access to backend API endpoints
- JWT authentication system operational

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

3. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

4. **Configure environment variables**
   Create `.env.local` file with:
   ```
   NEXT_PUBLIC_API_BASE_URL=<backend-api-base-url>
   ```

5. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

6. **Open the application**
   Visit `http://localhost:3000` in your browser

## Key Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests

## Project Structure Overview
- `app/` - Next.js App Router pages and layouts
- `components/` - Reusable UI components
- `lib/` - Utility functions and API clients
- `hooks/` - Custom React hooks
- `types/` - TypeScript type definitions

## Authentication Flow
1. Unauthenticated users directed to `/signup` or `/signin`
2. Upon successful authentication, JWT stored in browser
3. Protected routes in `/dashboard` require valid JWT
4. Token automatically attached to API requests

## API Integration
- All API calls go through centralized `lib/api.ts` client
- Authorization headers automatically added to requests
- Error handling and loading states managed globally