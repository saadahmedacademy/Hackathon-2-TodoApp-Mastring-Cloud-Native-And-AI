#!/usr/bin/env python3
"""
Main CLI application for the console todo application.
"""
import sys
import os
# Add the project root to the Python path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.todo_service import TodoService


def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("Console Todo Application")
    print("="*50)
    print("1. Add Todo")
    print("2. View Todos")
    print("3. Update Todo")
    print("4. Mark Complete")
    print("5. Mark Incomplete")
    print("6. Delete Todo")
    print("7. Exit")
    print("-"*50)


def get_user_choice():
    """Get and validate user menu choice."""
    try:
        choice = input("Enter your choice (1-7): ").strip()
        return int(choice)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 7.")
        return None


def add_todo(service: TodoService):
    """Handle adding a new todo item."""
    print("\n--- Add New Todo ---")
    title = input("Enter title: ").strip()

    if not title:
        print("Error: Title is required and cannot be empty.")
        return

    description = input("Enter description (optional, press Enter to skip): ").strip()
    if not description:
        description = None

    try:
        todo = service.add_todo(title, description)
        print(f"Successfully added todo: '{todo.title}' with ID {todo.id}")
    except ValueError as e:
        print(f"Error: {e}")


def view_todos(service: TodoService):
    """Handle viewing all todo items."""
    print("\n--- All Todos ---")
    todos = service.get_all_todos()

    if not todos:
        print("No todos found.")
        return

    for todo in todos:
        status = "✓" if todo.completed else "○"
        print(f"[{status}] {todo.id}. {todo.title}")

        if todo.description:
            print(f"    Description: {todo.description}")
        print()


def update_todo(service: TodoService):
    """Handle updating an existing todo item."""
    print("\n--- Update Todo ---")

    try:
        todo_id = int(input("Enter ID of todo to update: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    # Check if todo exists
    existing_todo = service.find_todo_by_id(todo_id)
    if not existing_todo:
        print(f"Error: Todo with ID {todo_id} not found.")
        return

    print(f"Updating todo: {existing_todo.title}")

    new_title = input(f"Enter new title (current: '{existing_todo.title}', press Enter to keep current): ").strip()
    if not new_title:
        new_title = None  # Keep existing title

    new_description = input(f"Enter new description (current: '{existing_todo.description or 'None'}', press Enter to keep current): ").strip()
    if new_description == "":
        new_description = existing_todo.description  # Keep existing description if empty input provided
    elif not new_description:  # If input was just whitespace
        new_description = None  # Set to None if empty

    try:
        if service.update_todo(todo_id, new_title, new_description):
            print(f"Successfully updated todo with ID {todo_id}")
        else:
            print(f"Failed to update todo with ID {todo_id}")
    except ValueError as e:
        print(f"Error: {e}")


def mark_complete(service: TodoService):
    """Handle marking a todo as complete."""
    print("\n--- Mark Todo Complete ---")

    try:
        todo_id = int(input("Enter ID of todo to mark complete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if service.mark_complete(todo_id):
        print(f"Successfully marked todo with ID {todo_id} as complete")
    else:
        print(f"Error: Todo with ID {todo_id} not found")


def mark_incomplete(service: TodoService):
    """Handle marking a todo as incomplete."""
    print("\n--- Mark Todo Incomplete ---")

    try:
        todo_id = int(input("Enter ID of todo to mark incomplete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if service.mark_incomplete(todo_id):
        print(f"Successfully marked todo with ID {todo_id} as incomplete")
    else:
        print(f"Error: Todo with ID {todo_id} not found")


def delete_todo(service: TodoService):
    """Handle deleting a todo item."""
    print("\n--- Delete Todo ---")

    try:
        todo_id = int(input("Enter ID of todo to delete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    if service.delete_todo(todo_id):
        print(f"Successfully deleted todo with ID {todo_id}")
    else:
        print(f"Error: Todo with ID {todo_id} not found")


def main():
    """Main application loop."""
    service = TodoService()
    print("Welcome to the Console Todo Application!")

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            add_todo(service)
        elif choice == 2:
            view_todos(service)
        elif choice == 3:
            update_todo(service)
        elif choice == 4:
            mark_complete(service)
        elif choice == 5:
            mark_incomplete(service)
        elif choice == 6:
            delete_todo(service)
        elif choice == 7:
            print("\nThank you for using the Console Todo Application!")
            print("Goodbye!")
            break
        else:
            if choice is not None:  # Only show error if input was valid number but not in range
                print("Invalid choice. Please enter a number between 1 and 7.")

        # Pause to let user see results before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()