# Data Model: Phase-II Backend

## Entity: TodoItem

### Fields
- **id**: Integer (Primary Key, Auto-increment)
- **user_id**: String (Foreign Key, Required) - Links to user who owns the todo
- **title**: String (Required, Max length: 255)
- **description**: String (Optional, Max length: 1000)
- **completed**: Boolean (Default: false)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated, Updates on modification)

### Relationships
- Belongs to one User (identified by user_id)

### Validation Rules
- Title must not be empty or null
- Title must be between 1-255 characters
- Description can be null or up to 1000 characters
- Completed defaults to false
- Both timestamps are automatically managed

## Entity: User (Reference)

### Fields
- **user_id**: String (Primary Key, Required) - Provided by authentication system

## State Transitions
- **Incomplete** (default) → **Complete** (via mark_complete endpoint)
- **Complete** → **Incomplete** (via update endpoint with completed=false)

## Database Considerations (Neon PostgreSQL)
- Index on (user_id) for efficient user-based queries
- Index on (user_id, completed) for filtered queries
- Foreign key constraint on user_id (if user table exists)
- Proper escaping and parameterized queries to prevent SQL injection