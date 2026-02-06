# Data Model: Console Todo Application

## TodoItem Entity

### Fields
- **id**: Integer (required, auto-generated, unique)
- **title**: String (required, non-empty)
- **description**: String (optional, nullable)
- **completed**: Boolean (required, default: False)

### Validation Rules
- id: Must be a positive integer, auto-assigned sequentially
- title: Must be a non-empty string (length > 0)
- description: Can be empty or null
- completed: Must be a boolean value

### State Transitions
- Default state: completed = False
- Transition to completed: completed = True (via mark_complete operation)
- Transition to incomplete: completed = False (via mark_incomplete operation)

## TodoList Collection

### Fields
- **items**: Array/List of TodoItem entities
- **next_id**: Integer (auto-managed, starts at 1)

### Operations
- Add new item: Creates TodoItem with auto-assigned ID
- Retrieve all items: Returns entire collection
- Find by ID: Returns specific TodoItem or None if not found
- Update item: Modifies existing TodoItem properties
- Delete item: Removes TodoItem from collection
- Mark complete: Updates completed status of TodoItem

### Constraints
- All IDs must be unique within the collection
- IDs must be sequential integers starting from 1
- No duplicate IDs allowed