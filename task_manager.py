# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATE_STRING_FORMAT = "%Y-%m-%d"
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# Load tasks from tasks.txt
task_list = []
with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = [t.strip() for t in t_str.split(";")]
    if len(task_components) < 6:
        print(f"Skipping invalid task: {task_components}")
        continue
    try:
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATE_STRING_FORMAT).date()
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATE_STRING_FORMAT).date()
        curr_t['completed'] = True if task_components[5] == "Yes" else False
    except ValueError:
        print(f"Skipping task with invalid date format: {task_components}")
        continue

    task_list.append(curr_t)

# Write updated tasks to file
with open("tasks.txt", "w") as task_file:
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


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().splitlines()

# Convert to a dictionary
username_password = {}
for line in user_data:
    username, password = line.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
    
    # Creating a function for registering a new user
    def reg_user(username_password):
        # Request input of a new username
        new_username = input("New Username: ")

        # Request input of a new password
        new_password = input("New Password: ")

        # Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # If they are the same, check if the username already exists in the user.txt file.
            with open("user.txt", "r") as in_file:
                for line in in_file:
                    username, password = line.split(";")
                    if username == new_username:
                        print("Username already exists. Please try a different username.")
                        new_username = input("New Username: ")
                        break

            # If the username does not exist, add it to the user.txt file.
            print("New user added")
            username_password[new_username] = new_password

            with open("user.txt", "a") as out_file:
                out_file.write(f"{new_username};{new_password}\n")

        # Otherwise you present a relevant message.
        else:
            print("Passwords do not match")

    # Check if the user input is valid.
    if menu in ("r", "a", "va", "vm", "gr", "ds", "e"):
        # If it is valid, execute the corresponding function.
        if menu == "r":
            reg_user(username_password)
        # else:
        #     print("Invalid input. Please choose a valid option.")

    #Creating a function to add a task
    def add_task():
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.'''
        global menu
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            return
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        # Read current tasks from file
        with open("tasks.txt", "r") as task_file:
            task_data = task_file.read().splitlines()

        # Convert to list of dictionaries
        task_list = []
        for line in task_data:
            task_attrs = line.split(";")
            task_dict = {
                "username": task_attrs[0],
                "title": task_attrs[1],
                "description": task_attrs[2],
                "due_date": datetime.strptime(task_attrs[3], DATETIME_STRING_FORMAT),
                "assigned_date": datetime.strptime(task_attrs[4], DATETIME_STRING_FORMAT).date(),
                "completed": True if task_attrs[5].lower() == "yes" else False
            }
            task_list.append(task_dict)

        task_list.append(new_task)

        # Write updated tasks to file
        with open("tasks.txt", "w") as task_file:
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

    if menu == "a":
        add_task()


    # Creating a function called view all tasks 
    # that is called when users type ‘va’ to view all the tasks listed in ‘tasks.txt’.
    def view_all_tasks():
        """
        Reads the tasks from tasks.txt file and prints to the console in the format specified.
        """
        with open('tasks.txt', 'r') as f:
            for line in f:
                fields = line.strip().split(';')
                task_title = fields[1]
                task_description = fields[2]
                assigned_date = fields[3]
                due_date = fields[4]
                is_completed = "Yes" if fields[5].lower() == "true" else "No"  # Change True/False to Yes/No

                print(f"Task: \t\t {task_title}")
                print(f"Assigned to: \t {fields[0]}")
                print(f"Date Assigned: \t {assigned_date}")
                print(f"Due Date: \t {due_date}")
                print(f"Task Description: \t {task_description}")
                print(f"Completed: \t {is_completed}")
                print()  # add a blank line between tasks

    # Check if the user wants to view all tasks
    # Now calling the view all function
    if menu == 'va':
        view_all_tasks()


    
    # # '''Edit a task.'''
    # def edit_task(task):
    #     print("Enter the new details for the task.")
    #     task['title'] = input("Title: ")
    #     task['description'] = input("Description: ")
    #     task['due_date'] = input("Due date (YYYY-MM-DD): ")
       
        # Creating a function called view all (vm) tasks 
        # to view all the tasks that have been assigned to them.
    
    from datetime import datetime

    def load_tasks():
        """
        Loads tasks from tasks.txt file into a list of dictionaries.

        Returns:
            A list of dictionaries representing tasks.
        """
        task_list = []
        with open('tasks.txt', 'r') as f:
            for line in f:
                fields = line.strip().split(';')
                task = {
                    'username': fields[0],
                    'title': fields[1],
                    'description': fields[2],
                    'due_date': datetime.strptime(fields[3], '%Y-%m-%d').date(),
                    'assigned_date': datetime.strptime(fields[4], '%Y-%m-%d').date(),
                    'completed': fields[5]
                }
                task_list.append(task)
        return task_list

    # This function saves all edited tasks in the view_mine function before writing them to the tasks.txt output file
    def save_tasks(task_list):
        """
        Saves the given list of tasks to the tasks.txt file.

        Args:
            task_list: A list of dictionaries representing tasks.

        Returns:
            None.
        """
        with open('tasks.txt', 'w') as f:
            for task in task_list:
                line = ';'.join([task['username'], task['title'], task['description'], str(task['due_date']), str(task['assigned_date']), str(task['completed'])]) + '\n'
                f.write(line)

    # Creating a function called view_mine()
    def view_mine(task_list, curr_user):
        """
        Prints all tasks in the given list that are assigned to the given user in a table format.
        Allows the user to select a task to mark as complete or edit, and updates the task list accordingly.

        Args:
            task_list: A list of dictionaries representing tasks.
            curr_user: The current user.

        Returns:
            None.
        """
        print("Task ID | Username | Task Title | Task Description | Due Date | Assign Date | Completed")
        for i, task in enumerate(task_list):
            if task['username'] == curr_user:
                task_id = i + 1
                if task['completed'] == "Yes":
                    completed_str = "Yes"
                else:
                    completed_str = "No"
                print(f"{task_id:<8} | {task['username']:<8} | {task['title']:<10} | {task['description']:<20} | {task['due_date'].strftime('%Y-%m-%d'):<19} | {task['assigned_date'].strftime('%Y-%m-%d'):<19} | {completed_str:<9}")

        while True:
            task_id = input("Enter Task ID to mark as complete or edit (Enter 'q' to quit): ")
            if task_id.lower() == "q":
                break
            try:
                task_index = int(task_id) - 1
                if task_index < 0 or task_index >= len(task_list):
                    raise ValueError("Invalid Task ID. Please try again.")
            except (TypeError, ValueError):
                print("Invalid Task ID. Please try again")
                continue

            task = task_list[task_index]

            if task['completed'] == "Yes":
                print("This task has already been completed and cannot be edited.")
                continue

            while True:
                action = input("Enter 'c' to mark as complete or 'e' to edit (Enter 'q' to quit): ")
                if action.lower() not in ["c", "e", "q"]:
                    print("Invalid action. Please try again.")
                    continue
                break

            if action.lower() == "q":
                break

            if action.lower() == "c":
                task['completed'] = "Yes"
                save_tasks(task_list)
                print("Task marked as complete.")

            if action.lower() == "e":
                print("Fields that can be edited: 'username', 'title', 'description', 'due_date'")
                while True:
                    field_to_edit = input("Enter field to edit (Enter 'q' to quit): ")
                    if field_to_edit.lower() == "q":
                        break
                    elif field_to_edit.lower() not in ["username", "title", "description", "due_date"]:
                        print("Invalid field. Please try again.")
                        continue
                    break

                if field_to_edit.lower() == "q":
                    break

                new_value = input(f"Enter new value for '{field_to_edit}' (leave blank to keep current value): ")
                if new_value:
                    if field_to_edit == "due_date":
                        try:
                            new_value = datetime.strptime(new_value, '%Y-%m-%d').date()
                        except (TypeError, ValueError):
                            print("Invalid date format. Due date not updated.")
                            return
                    task[field_to_edit] = new_value

                    # Ensure 'completed' field is always a string
                    task['completed'] = str(task['completed'])

                    save_tasks(task_list)
                    print("Task updated.")

                    # Re-read tasks from file into task_list
                    with open('tasks.txt', 'r') as f:
                        task_list = []
                        for line in f:
                            fields = line.strip().split(';')
                            task_list.append({
                                'username': fields[0],
                                'title': fields[1],
                                'description': fields[2],
                                'due_date': fields[3],
                                'assigned_date': fields[4],
                                'completed': fields[5]
                            })
                    break
                else:
                    print("Invalid input. Please try again.")

        with open('tasks.txt', 'r') as f:
            print(f.read())

    # Check if the user wants to view their tasks
    if menu == "vm":
        view_mine(task_list, curr_user)

    
    # function to for gr- generate reports
    def generate_reports(task_list, user_list):
        # Get the total number of tasks
        total_tasks = len(task_list)

        # Get the total number of completed tasks
        completed_tasks = 0
        for task in task_list:
            if task['completed']:
                completed_tasks += 1

        # Get the total number of uncompleted tasks
        uncompleted_tasks = total_tasks - completed_tasks

        # Get the total number of overdue tasks
        overdue_tasks = 0
        for task in task_list:
            if not task['completed'] and 'deadline' in task and task['deadline'] < datetime.now().date():
                overdue_tasks += 1

        # Calculate the percentage of tasks that are incomplete and overdue
        incomplete_percentage = (uncompleted_tasks / total_tasks) * 100
        overdue_percentage = (overdue_tasks / total_tasks) * 100

        # Write the task overview report to a file
        with open('task_overview.txt', 'w') as f:
            f.write(f'Total number of tasks: {total_tasks}\n')
            f.write(f'Total number of completed tasks: {completed_tasks}\n')
            f.write(f'Total number of uncompleted tasks: {uncompleted_tasks}\n')
            f.write(f'Total number of overdue tasks: {overdue_tasks}\n')
            f.write(f'Percentage of tasks that are incomplete: {incomplete_percentage:.2f}%\n')
            f.write(f'Percentage of tasks that are overdue: {overdue_percentage:.2f}%\n')

        # Get the total number of users
        total_users = len(user_list)

        # Write the user overview report to a file
        with open('user_overview.txt', 'w') as f:
            f.write(f'Total number of users: {total_users}\n')
            f.write(f'Total number of tasks: {total_tasks}\n')
            f.write('\n')
            for user in user_list:
                if isinstance(user, dict):
                    user_tasks = 0
                    completed_user_tasks = 0
                    overdue_user_tasks = 0
                    for task in task_list:
                        if task.get('assigned_to') == user['username']:
                            user_tasks += 1
                            if task['completed']:
                                completed_user_tasks += 1
                            elif 'deadline' in task and task['deadline'] < datetime.now().date():
                                overdue_user_tasks += 1
                    f.write(f'{user["username"]}:\n')
                    f.write(f'Total number of tasks assigned to user: {user_tasks}\n')
                    f.write(f'Percentage of total tasks assigned to user: {(user_tasks / total_tasks) * 100:.2f}%\n')
                    f.write(f'Percentage of tasks assigned to user that have been completed: {(completed_user_tasks / user_tasks) * 100:.2f}%\n')
                    f.write(f'Percentage of tasks assigned to user that must still be completed: {((user_tasks - completed_user_tasks - overdue_user_tasks) / user_tasks) * 100:.2f}%\n')
                    f.write(f'Percentage of tasks assigned to user that are overdue: {(overdue_user_tasks / user_tasks) * 100:.2f}%\n')
                    f.write('\n')
                else:
                    print(f"Invalid user: {user}")
        print("Reports generated successfully.")
    if menu == "gr":
        generate_reports(task_list, curr_user)            
    

                
    # if menu choice is to display statistics
    elif menu == 'ds' and curr_user == 'admin':
        # Check if the task and user files exist, and generate them if they don't
        if not os.path.exists('tasks.txt') or not os.path.exists('user.txt'):
            reg_user(username_password)
            add_task()


        # Read the user data from the user file
        with open('user.txt', 'r') as f:
            user_data = f.readlines()
        
        # Count the number of users and tasks
        num_users = len(user_data)
        num_tasks = 0
        for line in user_data:
            username = line.strip().split(',')[0]
            # Count the number of tasks assigned to the user
            with open('tasks.txt', 'r') as f:
                for task_line in f.readlines():
                    task = task_line.strip().split(',')
                    if task[0] == username:
                        num_tasks += 1

        # Display the statistics
        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    # else:
    #     print("You have made a wrong choice, Please Try again")