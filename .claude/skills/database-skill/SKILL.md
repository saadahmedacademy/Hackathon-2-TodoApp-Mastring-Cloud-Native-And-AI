---
name: database-skill
description: Design relational schemas, create tables, and manage safe database migrations.
---

# Database Skill

## Instructions

1. **Schema Design**
   - Model entities based on domain requirements
   - Define clear primary keys and foreign keys
   - Normalize data while avoiding over-engineering
   - Explicitly define nullable vs non-nullable fields

2. **Table Creation**
   - Create tables with meaningful names
   - Use appropriate data types for each column
   - Add indexes for frequently queried fields
   - Enforce constraints to prevent invalid states

3. **Migrations**
   - Version all schema changes
   - Ensure migrations are idempotent or reversible
   - Avoid destructive changes without a safe path
   - Document intent of each migration clearly

4. **Relationships**
   - Define one-to-many and many-to-many relationships explicitly
   - Enforce referential integrity at the database level
   - Use cascading rules carefully and intentionally

--------------------------------------------------
BEST PRACTICES
--------------------------------------------------

- Treat the database as a source of truth
- Enforce constraints in the schema, not only in code
- Prefer explicit schemas over implicit behavior
- Keep migrations small and incremental
- Design schemas to evolve safely over time

--------------------------------------------------
COMMON PITFALLS TO AVOID
--------------------------------------------------

- Missing foreign keys or constraints
- Overuse of nullable columns
- Breaking changes without migrations
- Storing derived or duplicated data unnecessarily
- Relying solely on application-level validation

--------------------------------------------------
EXAMPLE WORKFLOW (CONCEPTUAL)
--------------------------------------------------

Design:
Domain Model → Relational Schema → Constraints & Indexes

Change:
Schema Update → Migration → Review → Apply

--------------------------------------------------
SUCCESS CRITERIA
--------------------------------------------------

- Tables accurately reflect domain intent
- Data integrity is enforced by the database
- Migrations are safe, reviewable, and reversible
- Schema supports future feature expansion
- Database layer remains stable across phases

