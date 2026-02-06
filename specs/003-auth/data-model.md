# Data Model: Authentication System

## Overview
Data model for authentication system including user accounts, tokens, and session management.

## Core Entities

### User
**Description**: User account information managed by Better Auth
**Fields**:
- id: Unique identifier (UUID/string) - Primary key
- email: User's email address - Required, unique, validated
- password_hash: Hashed password using Argon2 - Required, stored securely
- created_at: Account creation timestamp - Auto-generated
- updated_at: Last update timestamp - Auto-generated
- email_verified: Boolean indicating email verification status - Optional
- name: User's display name - Optional

**Relationships**:
- One-to-many with user's tasks (via user_id foreign key in tasks table)

### Session
**Description**: Active user sessions managed by Better Auth
**Fields**:
- id: Unique session identifier - Primary key
- user_id: Reference to user - Foreign key to User.id
- expires_at: Session expiration timestamp - Required
- created_at: Session creation timestamp - Auto-generated
- last_accessed_at: Last time session was used - Auto-generated
- device_info: Information about the device used - Optional
- ip_address: IP address of the session - Optional

### JWT Token
**Description**: JWT access and refresh tokens for authentication
**Fields**:
- token_hash: Hash of the JWT token - Primary key (for refresh tokens)
- user_id: Reference to user - Foreign key to User.id
- token_type: Type of token (access/refresh) - Required
- expires_at: Token expiration timestamp - Required
- created_at: Token creation timestamp - Auto-generated
- revoked: Boolean indicating if token was revoked - Default false

## Validation Rules

### User Validation
- Email must follow standard email format
- Password must meet strength requirements (minimum length, complexity)
- Email must be unique across all users
- Required fields cannot be null

### Session Validation
- Session must have valid user reference
- Session cannot be used after expiration
- Concurrent session limits (optional)

### Token Validation
- Tokens must have valid expiration times
- Revoked tokens cannot be used for authentication
- Refresh tokens should have longer lifespans than access tokens

## State Transitions

### User States
- Pending Verification → Active (after email verification)
- Active → Suspended (administrative action)
- Suspended → Active (after review)

### Session States
- Created → Active (first use)
- Active → Expired (after TTL)
- Active → Revoked (logout or administrative action)