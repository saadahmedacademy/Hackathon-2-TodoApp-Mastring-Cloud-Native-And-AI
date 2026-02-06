# Frontend Web Application

This is the frontend web application for the Progressive Todo Application, built with Next.js, React, and Tailwind CSS. It provides a user interface for authentication (signup, signin) and managing user-specific todo lists by consuming the backend REST APIs.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Development Server](#running-the-development-server)
  - [Building for Production](#building-for-production)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## Features

- User Registration and Login
- View, Create, Update, Delete Todo Items
- Mark Todo Items as Complete/Incomplete
- Responsive Interface for various screen sizes
- Secure Session Management with JWT tokens

## Tech Stack

- **Framework:** Next.js 16+ (App Router)
- **UI Library:** React 18+
- **Styling:** Tailwind CSS
- **Language:** TypeScript
- **HTTP Client:** Fetch API (or Axios if preferred)

## Prerequisites

Before you begin, ensure you have the following installed:

-   Node.js (v18.x or later)
-   npm (v9.x or later) or Yarn (v1.x or later)

## Getting Started

Follow these steps to set up and run the frontend application locally.

### Installation

1.  Navigate to the `phase-2/frontend` directory:
    ```bash
    cd phase-2/frontend
    ```
2.  Install the dependencies:
    ```bash
    npm install
    # or
    yarn install
    ```

### Environment Variables

Create a `.env.local` file in the `phase-2/frontend` directory (at the same level as `package.json`) and add the following environment variables. These are crucial for the application to communicate with the backend API.

```
# .env.local
NEXT_PUBLIC_BACKEND_API_BASE_URL=http://localhost:8000 # Replace with your backend API URL
```

Make sure to replace `http://localhost:8000` with the actual URL of your running backend API.

### Running the Development Server

1.  Start the development server:
    ```bash
    npm run dev
    # or
    yarn dev
    ```
2.  Open your browser and visit `http://localhost:3000` (or the port specified in your terminal) to see the application.

### Building for Production

1.  Generate a production build:
    ```bash
    npm run build
    # or
    yarn build
    ```
2.  Start the production server:
    ```bash
    npm run start
    # or
    yarn start
    ```

## API Endpoints

This frontend application consumes the REST API provided by the backend (located in `phase-2/src/api`). Ensure the backend is running and accessible at the `NEXT_PUBLIC_BACKEND_API_BASE_URL` specified in your `.env.local` file.

Key API interactions include:
- User registration and login
- Fetching, creating, updating, and deleting todo items

## Project Structure

The project follows the Next.js App Router structure:

```
frontend/
├── app/                  # Next.js App Router structure
│   ├── (auth)/           # Public routes (auth flow: signup, signin)
│   ├── dashboard/        # Protected routes (todo management)
│   ├── globals.css       # Global styles
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Root page
├── components/           # Reusable UI components (auth, todos, ui, layout)
├── lib/                  # Utilities and helper functions (auth, api, utils)
├── hooks/                # Custom React hooks (useAuth, useTodos)
├── types/                # TypeScript type definitions
├── public/               # Static assets
└── tests/                # Test files
```