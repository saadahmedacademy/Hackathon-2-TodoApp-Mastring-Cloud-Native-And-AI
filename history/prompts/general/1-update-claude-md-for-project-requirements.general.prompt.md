---
id: 1
title: Update Claude MD for Project Requirements
stage: general
date: 2026-02-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-console-todo-app
user: saadahmed
command: "update claude.md file based on project requirements"
labels: [claude-md, configuration, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /home/saadahmed/hk-2-project/CLAUDE.md
tests:
---

## Prompt

Update the claude.md file based on my project requirements. In this file:

Use Auth Agent for authentication
Use Frontend Agent for frontend development (e.g., Next.js)
Use DB Agent for database design and operations
Use Backend Agent for FastAPI development
Below are my project requirements:

Basic Level Functionality
Objective: Using Claude Code and Spec-Kit Plus transform the console app into a modern multi-user web application with persistent storage.
💡Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement all 5 Basic Level features as a web application
Create RESTful API endpoints
Build responsive frontend interface
Store data in Neon Serverless PostgreSQL database
Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer
Technology
Frontend
Next.js 16+ (App Router)
Backend
Python FastAPI
ORM
SQLModel
Database
Neon Serverless PostgreSQL
Spec-Driven
Claude Code + Spec-Kit Plus
Authentication
Better Auth

Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
User logs in on Frontend → Better Auth creates a session and issues a JWT token
Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
Backend filters data → Returns only tasks belonging to that user

"""```

## Response snapshot

Updated the CLAUDE.md file to reflect the project requirements with the specified technology stack and agent assignments. Modified three sections:
1. Updated the Task context section to include information about the specialized agents (Auth, Frontend, DB, Backend)
2. Added a Technology Stack and Project Structure section with details about the layer architecture and authentication flow
3. Added a Development Approach and Requirements section with information about the Agentic Dev Stack workflow and Basic Level functionality requirements

## Outcome

- ✅ Impact: Updated CLAUDE.md to reflect project-specific requirements and technology stack
- 🧪 Tests: none
- 📁 Files: Modified /home/saadahmed/hk-2-project/CLAUDE.md to include agent assignments and project requirements
- 🔁 Next prompts: Continue with project setup and implementation
- 🧠 Reflection: Successfully updated the configuration file to guide the project development with the correct technology stack and agent assignments

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): Begin with /sp.specify to create the initial specification