import json

# Global task list
tasks = []


# -------------------- FILE HANDLING --------------------

def load_tasks():
    global tasks
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except:
        tasks = []


def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)


# -------------------- CORE FEATURES --------------------

def add_task():
    name = input("Enter task: ")
    priority = input("Enter priority (High/Medium/Low): ")

    task = {
        "name": name,
        "priority": priority,
        "done": False
    }

    tasks.append(task)

    save_tasks()   # 👈 VERY IMPORTANT LINE

    print("✅ Task added!")
    


def view_tasks():
    if not tasks:
        print("❌ No tasks available")
        return

    print("\n📋 Your Tasks:")
    for i, task in enumerate(tasks):
        status = "✅ Done" if task["done"] else "⏳ Pending"
        print(f"{i+1}. {task['name']} | {task['priority']} | {status}")


def delete_task():
    view_tasks()
    try:
        task_no = int(input("Enter task number to delete: "))
        if 0 < task_no <= len(tasks):
            removed = tasks.pop(task_no - 1)
            save_tasks()
            print(f"🗑️ Deleted: {removed['name']}")
        else:
            print("❌ Invalid number")
    except:
        print("❌ Please enter a valid number")


def mark_done():
    view_tasks()
    try:
        task_no = int(input("Enter task number to mark as done: "))
        if 0 < task_no <= len(tasks):
            tasks[task_no - 1]["done"] = True
            save_tasks()
            print("✅ Task marked as done!")
        else:
            print("❌ Invalid number")
    except:
        print("❌ Please enter a valid number")


def search_task():
    keyword = input("Enter keyword to search: ").lower()
    found = False

    for i, task in enumerate(tasks):
        if keyword in task["name"].lower():
            status = "Done" if task["done"] else "Pending"
            print(f"{i+1}. {task['name']} | {task['priority']} | {status}")
            found = True

    if not found:
        print("❌ No matching tasks found")


def sort_tasks():
    if not tasks:
        print("❌ No tasks to sort")
        return

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: priority_order.get(x["priority"], 4))

    print("🔄 Tasks sorted by priority!")
    save_tasks()

def edit_task():
    view_tasks()
    try:
        task_no = int(input("Enter task number to edit: "))
        if 0 < task_no <= len(tasks):
            new_name = input("Enter new task name: ")
            new_priority = input("Enter new priority (High/Medium/Low): ")

            tasks[task_no - 1]["name"] = new_name
            tasks[task_no - 1]["priority"] = new_priority

            save_tasks()
            print("✏️ Task updated!")
        else:
            print("❌ Invalid number")
    except:
        print("❌ Please enter a valid number")

# -------------------- MAIN PROGRAM --------------------

def main():
    load_tasks()

    while True:
        print("\n====== SMART TASK MANAGER ======")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Mark Task as Done")
        print("5. Search Task")
        print("6. Sort by Priority")
        print("7. Edit Task")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            mark_done()
        elif choice == "5":
            search_task()
        elif choice == "6":
            sort_tasks()
        elif choice == "7":
            edit_task()
        elif choice == "8":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice")


# Run program
if __name__ == "__main__":
    main()