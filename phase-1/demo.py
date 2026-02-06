#!/usr/bin/env python3
"""
Demo script to showcase the Console Todo Application functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.services.todo_service import TodoService

def demo():
    print("🎯 Console Todo Application Demo")
    print("="*40)

    # Create service instance
    service = TodoService()

    print("\n1. Adding todos...")
    todo1 = service.add_todo("Buy groceries", "Milk, bread, eggs")
    print(f"   Added: {todo1.title}")

    todo2 = service.add_todo("Walk the dog")
    print(f"   Added: {todo2.title}")

    todo3 = service.add_todo("Finish project", "Complete the implementation")
    print(f"   Added: {todo3.title}")

    print(f"\n2. Current todos ({len(service.get_all_todos())} total)...")
    for todo in service.get_all_todos():
        status = "✓" if todo.completed else "○"
        desc = f" - {todo.description}" if todo.description else ""
        print(f"   [{status}] {todo.id}. {todo.title}{desc}")

    print(f"\n3. Updating todo #{todo2.id}...")
    service.update_todo(todo2.id, "Walk the dog in the park", "Don't forget the leash")
    updated_todo = service.find_todo_by_id(todo2.id)
    print(f"   Updated: {updated_todo.title}")

    print(f"\n4. Marking todo #{todo1.id} as complete...")
    service.mark_complete(todo1.id)
    completed_todo = service.find_todo_by_id(todo1.id)
    print(f"   Marked as {'complete' if completed_todo.completed else 'incomplete'}")

    print(f"\n5. Current todos after updates...")
    for todo in service.get_all_todos():
        status = "✓" if todo.completed else "○"
        desc = f" - {todo.description}" if todo.description else ""
        print(f"   [{status}] {todo.id}. {todo.title}{desc}")

    print(f"\n6. Deleting todo #{todo3.id}...")
    service.delete_todo(todo3.id)
    print(f"   Deleted todo with ID {todo3.id}")

    print(f"\n7. Final todos...")
    todos = service.get_all_todos()
    if todos:
        for todo in todos:
            status = "✓" if todo.completed else "○"
            print(f"   [{status}] {todo.id}. {todo.title}")
    else:
        print("   No todos remaining")

    print(f"\n✅ Demo completed! {len(todos)} todos remaining in the list.")

if __name__ == "__main__":
    demo()