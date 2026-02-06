# Quickstart Guide: Console Todo Application

## Prerequisites
- Python 3.10 or higher
- No external packages required

## Setup
1. Clone or download the repository
2. Navigate to the project directory
3. Ensure you have Python 3.10+ installed (`python --version`)

## Running the Application
Execute the main application:
```bash
python src/cli/main.py
```

## Basic Usage
Once the application starts, you'll see a menu with the following options:

1. **Add Todo**: Enter a title (and optional description) to create a new todo item
2. **View Todos**: Display all existing todo items with their ID and status
3. **Update Todo**: Modify the title or description of an existing todo by ID
4. **Mark Complete**: Mark a todo as completed by specifying its ID
5. **Delete Todo**: Remove a todo from the list by specifying its ID
6. **Exit**: Quit the application

## Example Workflow
1. Start the application: `python src/cli/main.py`
2. Select option 1 to add a new todo
3. Enter "Buy groceries" as the title
4. Select option 2 to view all todos (you'll see your new todo with ID 1)
5. Select option 4 to mark the todo as complete
6. Select option 2 again to verify the status changed

## Error Handling
- Invalid menu selections will show an error message and return to the menu
- Non-existent todo IDs will show an appropriate error message
- Empty titles will be rejected when adding/updating todos

## Session Limitations
- Data is stored in memory only and will be lost when the application exits
- No persistent storage in Phase I
- All data is cleared when the application restarts