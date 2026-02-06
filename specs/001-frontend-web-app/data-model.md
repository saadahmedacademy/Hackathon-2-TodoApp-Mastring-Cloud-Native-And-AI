# Frontend Data Model: Todo Application

## User Entity
- **Fields**: id (string), email (string), createdAt (timestamp)
- **Relationships**: owns many Todos
- **Validation**: email must be valid format
- **State Transitions**: authenticated/unauthenticated

## Todo Entity
- **Fields**: id (string), title (string), description (optional string), completed (boolean), userId (string), createdAt (timestamp), updatedAt (timestamp)
- **Relationships**: belongs to User
- **Validation**: title must be non-empty, length limits for description
- **State Transitions**: incomplete → complete, complete → incomplete

## Authentication State
- **Fields**: isAuthenticated (boolean), user (User object or null), token (JWT string or null), isLoading (boolean)
- **Validation**: token must be present when isAuthenticated is true
- **State Transitions**: unauthenticated → authenticating → authenticated/failed

## API Response Models
### TodoResponse
- **Fields**: data (Todo object or Todo[]), error (optional Error object), status (number)

### AuthResponse
- **Fields**: data (User object), token (JWT string), error (optional Error object), status (number)

### ErrorResponse
- **Fields**: message (string), code (string), details (optional object)

## UI State Models
### TodoFormState
- **Fields**: title (string), description (string), errors (object), isSubmitting (boolean)

### TodoListState
- **Fields**: todos (Todo[]), filter (string), isLoading (boolean), error (string or null)