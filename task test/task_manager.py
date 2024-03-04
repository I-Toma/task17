'''
----- Task Manager Program -----
This program serves as a task manager
'''
# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise
# the program will look in your root directory for the text files.

# ===== Importing libraries ===== #

import os
from datetime import datetime, date


TASKS_FILE = "tasks.txt"
USERS_FILE = "user.txt"
DATETIME_STRING_FORMAT = "%Y-%m-%d"

'''
According to PEP 8, there should be two blank lines 
between top-level functions and classes.
Comments are ignored when considering blank lines between functions.
I checked the spacing MULTIPLE times and all of the functions seem to have
two blank lines between them, so i'm not sure why this comment,
in the  review was added:
(There should 2 blank lines before and after the definition of a function.)
'''

def create_tasks():
    '''
    Creates a new task file if it doesn't exist.
    '''
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w"):
            pass

    with open(TASKS_FILE, 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []

    for t_str in task_data:
        curr_t = {}

        # Split by semicolon and manually add each component
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime \
            (task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime \
            (task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    return task_list


def reg_user(username_password):
    '''
    Register a new user by taking input for username and password.
    Check for duplicate usernames before adding a new user.
    Args:
        username_password (dict): Dictionary containing
        the existing username-password pairs.
    '''
    # Add a new user to the user.txt file
    # Request input of a new username
    new_username = input("New Username: ").lower()
    if new_username in username_password.keys():
        print("Username already exists. Please choose a different username.")
        return

    # Request input of a new password
    new_password = input("New Password: ")

    # Request input of the password confirmation
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password match
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password

        # If no user.txt file, write one with a default account
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, "w") as default_file:
                default_file.write("admin;password")

        # Add the new user to the user.txt file
        with open(USERS_FILE, "a") as out_file:
            out_file.write(f"{new_username};{new_password}\n")
    else:
        print("Passwords do not match")


def add_task(task_list, username_password):
    '''
    Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.
    '''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of task: ")
    task_description = input("Description of task: ")

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime \
                (task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()

    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Add the new task to the list
    task_list.append(new_task)
    with open(TASKS_FILE, "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def display_task_details(i, t):
    '''
    Display the details of a task including its title, assigned user,
    assigned date, due date, description, and completion status.
    Parameters:
    - i (int): The task index
    - t (dict): The task details
    '''
    disp_str = f"{i}. Task:          {t['title']}\n"
    disp_str += f"Assigned to:      {t['username']}\n"
    disp_str += f"Date Assigned:    {t['assigned_date'].strftime \
                                        (DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date:         {t['due_date'].strftime \
                                        (DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Description: {t['description']}\n"
    disp_str += f"Completed:        {'Yes' if t['completed'] else 'No'}\n"
    print(disp_str)


def view_all(task_list):
    '''
    Function to view all tasks in the task list.
    Args:
    - task_list: The list of tasks to be viewed
    '''
    for i, t in enumerate(task_list, start=1):
        display_task_details(i, t)


def edit_task(selected_task):
    '''
    Edit the selected task in terms of username and due date.
    Args:
    - selected_task: Dictionary representing the selected task
    Returns:
    - updated_task: Dictionary with updated task details
    '''
    new_username = input("Enter the new username or"
                        "press enter to keep the current username: ")
    new_due_date_str = input("Enter the new due date (YYYY-MM-DD)"
                            "or press enter to keep the current due date: ")

    updated_task = selected_task.copy()

    if new_username:
        updated_task['username'] = new_username

    if new_due_date_str:
        try:
            updated_task['due_date'] = datetime.strptime \
                (new_due_date_str, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid datetime format. Task due date not updated.")

    return updated_task


def view_mine(task_list, curr_user):
    '''
    Display tasks assigned to the current user
    and provide options to mark as complete or edit.
    Args:
        task_list (list): List representing the tasks.
        curr_user (str): Current username.
    '''
    print("My Tasks:")
    for i, t in enumerate(task_list, start=1):
        if t['username'] == curr_user:
            display_task_details(i, t)

    while True:
        print("\nOptions:")
        print("  Enter task number to view details and perform actions.")
        print("  Enter -1 to return to the main menu.")

        choice = input("Your choice: ")

        if choice == '-1':
            break

        try:
            task_index = int(choice)
            if 1 <= task_index <= len(task_list):
                selected_task = task_list[task_index - 1]
                display_task_details(task_index, selected_task)

                action = input("Choose an action (1: Mark as complete,"
                               "2: Edit, -1: Return to main menu): ")

                if action == '1':
                    if not selected_task['completed']:
                        selected_task['completed'] = True
                        print("Task marked as complete.")
                    else:
                        print("Task is already marked as complete.")
                elif action == '2':
                    if not selected_task['completed']:
                        updated_task = edit_task(selected_task)
                        task_list[task_index - 1] = updated_task
                        print("Task edited successfully.")
                    else:
                        print("Cannot edit a completed task.")
                elif action == '-1':
                    break
                else:
                    print("Invalid action. Please choose a valid action.")
            else:
                print("Invalid task number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid task number.")


def generate_reports(task_list, username_password):
    '''
    Generates reports based on the task list
    and username/password dictionary.
    Calculates various statistics including total tasks,
    completed tasks, uncompleted tasks, overdue tasks,
    and percentages of tasks for both overall and individual users.
    Parameters:
    - task_list: The list of tasks
    - username_password: The dictionary of usernames and passwords
    '''
    total_users = len(username_password)
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    uncompleted_tasks = total_tasks - completed_tasks

    # I use "editor.rulers": [79], so it looked okay to me 😅
    overdue_tasks = sum(
                        1 for task in task_list if not task['completed']
                        and task['due_date'].date() < date.today()
                        )

    # Write task overview to file
    with open("task_overview.txt", "w") as task_file:
        task_file.write("Task Overview\n")
        task_file.write("--------------\n")
        task_file.write(f"Total tasks: {total_tasks}\n")
        task_file.write(f"Completed tasks: {completed_tasks}\n")
        task_file.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        task_file.write(f"Overdue tasks: {overdue_tasks}\n")

        # Check if task list is not empty before calculating percentages
        if total_tasks != 0:
            task_file.write(f"Percentage of tasks incomplete:"
                            f"{(uncompleted_tasks / total_tasks) * 100 \
                                :.2f}%\n")
            task_file.write(f"Percentage of tasks overdue:"
                            f"{(overdue_tasks / total_tasks) * 100 \
                                :.2f}%")
        else:
            task_file.write("No tasks assigned yet!")

    # Write user overview to file
    with open("user_overview.txt", "w") as user_file:
        user_file.write("User Overview\n")
        user_file.write("--------------\n")
        user_file.write(f"Total users: {total_users}\n")
        user_file.write(f"Total tasks: {total_tasks}\n")

        # Calculate user specific task statistics
        for username in username_password.keys():
            user_tasks = [task for task in task_list
                            if task['username'] == username]

            total_user_tasks = len(user_tasks)

            completed_user_tasks = sum(1 for task in user_tasks
                                        if task['completed'])

            uncompleted_user_tasks = total_user_tasks - completed_user_tasks

            overdue_user_tasks = sum(1 for task in user_tasks
                                        if not task['completed']
                                        and task['due_date']
                                        .date() < date.today())

            user_file.write(f"\nUser: {username}\n")
            user_file.write(f"Total tasks assigned: {total_user_tasks}\n")

            # Check if task list is not empty before calculating percentages
            if total_user_tasks != 0:
                if total_user_tasks != 0:

                    user_file.write(f"Percentage of total tasks: "
                                    f"{(completed_user_tasks / total_tasks) \
                                        * 100:.2f}%\n")

                    user_file.write(f"Percentage of completed tasks: "
                                    f"{(completed_user_tasks / \
                                        total_user_tasks * 100) \
                                        if total_user_tasks != 0 \
                                        else 0:.2f}%\n")

                    user_file.write(f"Percentage of uncompleted tasks: "
                                    f"{(uncompleted_user_tasks / \
                                        total_user_tasks * 100) \
                                        if total_user_tasks != 0 \
                                        else 0:.2f}%\n")

                    user_file.write(f"Percentage of overdue tasks: "
                                    f"{(overdue_user_tasks / \
                                        total_user_tasks) * 100 \
                                        if total_user_tasks != 0 \
                                        else 0:.2f}%")
            else:
                user_file.write("No tasks assigned yet!")
            user_file.write("\n")


def display_statistics():
    '''Display statistics of the tasks and users.'''
    # Read the contents of the task_overview.txt and display it
    with open("task_overview.txt", "r") as task_file:
        task_overview = task_file.read()
        print("\n")
        print(task_overview)
        print("----------------------------------------")

    # Read the contents of the user_overview.txt and display it
    with open("user_overview.txt", "r") as user_file:
        user_overview = user_file.read()
        print("\n")
        print(user_overview)
        print("----------------------------------------\n")


def main():
    '''Main function for user authentication and task management.'''
    username_password = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as user_file:
            user_data = user_file.read().split("\n")

        for user in user_data:
            if ";" in user:
                try:
                    username, password = user.rstrip().split(';')
                    username_password[username] = password
                except ValueError:
                    print()

    # Initialise an empty task list if tasks.txt doesn't exist
    task_list = create_tasks()

    logged_in = False

    # User authentication loop
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")

        # Validate user credentials
        if curr_user not in username_password:
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    # Main menu loop
    while True:
        print()
        menu = input('''Select one of the following Options below:
    r -  Registering a user
    a -  Adding a task
    va - View all tasks
    vm - View my task
    gr - Generate reports
    ds - Display statistics
    e -  Exit
    : ''').lower()

        # Depending on user choice perform the corresponding action
        if menu == 'r' and curr_user == 'admin':
            reg_user(username_password)
        elif menu == 'a':
            add_task(task_list, username_password)
        elif menu == 'va':
            view_all(task_list)
        elif menu == 'vm':
            view_mine(task_list, curr_user)
        elif menu == 'gr':
            generate_reports(task_list, username_password)
            print("Reports generated successfully.")
        elif menu == 'ds' and curr_user == 'admin':
            display_statistics()
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("Wrong choice or not admin, Please Try again")

if __name__ == "__main__":
    main()
