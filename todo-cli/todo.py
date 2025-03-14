
import click    # To create a CLI
import json     # To save and load tasks from a file
import os       # To check if the file exists

TODO_FILE = "todo.json"

#here we are writing a function to load tasks from the todo.json file
def load_tasks():
    """Load tasks from the todo.json file."""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as file:
            return json.load(file)
    return []  # If file doesn't exist, return an empty list

#here we are writing a function to save tasks to the todo.json file
def save_tasks(tasks):
    """Save tasks to the todo.json file."""
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
        
#here we are writing a function to create a group of commands
@click.group()
def cli():
    """Simple CLI for managing your Todo List"""
    pass

#here we are writing a function to add a new task
@cli.command()
@click.argument("task")
def add(task):
    """Add a new task to the todo list"""
    tasks = load_tasks()
    tasks.append({"task": task, "completed": False})
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")

#here we are writing a function to list all the tasks
@cli.command()
def list():
    """List all the tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No tasks found")
        return
    for index, task in enumerate(tasks, start=1):
        status = "✅" if task["completed"] else "❌"
        click.echo(f"{index}. {task['task']} [{status}]")
        
#here we are writing a function to mark as a completed task   
@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number -1]["completed"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed")
    else:
        click.echo(f"Invalid task number: {task_number}")
        
#here we are writing a function to delete or remove a task
@click.command()
@click.argument("task_number", type = int)
def remove(task_number):
    """Remove a task from the todo list"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number -1)
        save_tasks(tasks)
        click.echo(f"Removed task successfully: {removed_task['task']}")
    else:
        click.echo("Invalid task number")
        
        
#here we are adding all the commands in a group of commands 
cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)

#here we are running the CLI
if __name__ == "__main__":
    cli()
