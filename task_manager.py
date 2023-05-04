# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
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
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


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
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
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

# FUNCTION CALLED TO REGISTER USER
def reg_user():        
    while True:
        new_username = input("New Username: ")
        if new_username not in username_password.keys():
            new_password = input("New Password: ")

            # - Request input of password confirmation.
            confirm_password = input("Confirm Password: ")

            # - Check if the new password and confirmed password are the same.
            if new_password == confirm_password:
                # - If they are the same, add them to the user.txt file,
                print("New user added")
                username_password[new_username] = new_password
                
                with open("user.txt", "w") as out_file:
                    user_data = []
                    for k in username_password:
                        user_data.append(f"{k};{username_password[k]}")
                    out_file.write("\n".join(user_data))
                    break

            # - Otherwise you present a relevant message.
            else:
                print("Passwords do no match")
        else:    
            print("This username already exists in our database.\nPlease select a different username.")
            continue

# FUNCTION CALLED TO ADD TASK
def add_task():
    while True:
        '''Allow a user to add a new task to task.txt file
                Prompt a user for the following: 
                    - A username of the person whom the task is assigned to,
                    - A title of a task,
                    - A description of the task and 
                    - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
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

        task_list.append(new_task)
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
                print()
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break

# FUNCTION CALLED TO VIEW ALL TASKS
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
            format of Output 2 presented in the task pdf (i.e. includes spacing
            and labelling) 
        '''
    disp_str = f"\nALL TASKS: \n\n"
    for t in task_list:
        disp_str += f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Completed: \t {t['completed']}\n"
        disp_str += f"Task Description: \n {t['description']}\n\n\n"
        print(disp_str)

# FUNCTION CALLED TO VIEW MY TASK (contains other functions in it!)
def view_mine():
    '''Reads the urr_user's tasks from task.txt file and prints to the console (i.e. includes spacing
        and numbering for reference)
        Each task is saved into an array of dictionaries (Key is number of task)
        A list of task numbers is created (to later cross reference for selection)
    '''
    task_number = 1
    my_tasks = {}
    my_tasks_list = []
    disp_str = f"\nLIST OF {curr_user.upper()}'S TASKS:\n"
    for t in task_list:
        if t['username'] == curr_user:
            disp_str += f"Task {task_number}: \n"
            disp_str += f"\t\tTask: \t\t {t['title']}\n"
            disp_str += f"\t\tAssigned to: \t {t['username']}\n"
            disp_str += f"\t\tDate Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\t\tDue Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"\t\tCompleted: \t {t['completed']}\n"
            disp_str += f"\t\tTask Description: \n\t\t{t['description']}\n\n"
            my_tasks[task_number] = t
            my_tasks_list.append(t)
            task_number+=1
    print(disp_str)

    
    '''
    User selects task they would like to view and edit. Reads the task from my_tasks{} dictionary, and prints to the console 
        (Format includes spacing and labelling)
    '''
    print("\nPlease enter task number to edit details or mark as completed.")
    while True:
        try:
            selection=int(input("Or enter -1 to go back to menu\n"))
            if selection == -1:
                menu()
            elif selection not in my_tasks.keys():
                print("Invalid task number. Try again")
            else:
                t = my_tasks[selection]      
                disp_str += f"\nYOU SELECTED TASK {task_number}\n\n"
                disp_str += f"\t\tTask: \t\t {t['title']}\n"
                disp_str += f"\t\tAssigned to: \t {t['username']}\n"
                disp_str += f"\t\tDate Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"\t\tDue Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"\t\tTask Description: \n\t\t{t['description']}\n"
                print(disp_str)
                view_mine_options(t)
                break
        except ValueError:
            print("No valid integer! Please try again ...")
    
def view_mine_options(t):
    while True:

        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        # depending on menu selection: complete_task(), edit_task(), or loop.
        print()
        menu = input('''Select one of the following Options below:
e - Edit task
c - Mark task as completed
t - Go back to task list
''').lower()
        if menu == 't':
            view_mine()
        elif menu == 'm':
            break
        elif t['completed']== True:
            print("\nError: Unable to edit or complete a completed tasks.\nEnter t to go back to task list.")
        elif menu == 'e':
            edit_task(t)
            break
        elif menu == 'c':
            complete_task(t)
            break
        else:
            print("Invalid selection. Please try again")
        
      
# FUNCTION CALLED TO EDIT ONE OF MY TASKS
def edit_task(t):  
    while True:
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        # depending on menu selection: edit task_username or due_date 
        print()
        menu = input('''Select one of the following fields to edit:
u - Username of the person asigned to the task
d - Due date of the task
''').lower()
        if menu == 'u':
            # Prompt user to enter new username assigned to task.
            # If username doesn't exist = Error
            # If correct = updated task_list and re-writes it to tasks.txt
            while True:
                task_username = input("Name of new person assigned to this task: ")
                if task_username not in username_password.keys():
                    print("User does not exist. Please enter a valid username")
                    continue
                else:
                    t['username'] = task_username
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
                            print()
                        task_file.write("\n".join(task_list_to_write))
                    print("Task successfully updated.")
                    break
            break
        elif menu == 'd':
            # Prompt user to enter new due_date assigned to task.
            # If correct = updated task_list and re-writes it to tasks.txt
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                    t['due_date'] = due_date_time
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
                            print()
                        task_file.write("\n".join(task_list_to_write))
                    print("Task successfully updated. ")
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            break
        else:
            print("Invalid selection. Please try again")

# FUNCTION CALLED TO MARK ONE OF MY TASKS AS COMPLETED
def complete_task(t):
    t['completed'] = True
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
            print()
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully updated to COMPLETED = True.")

# FUNCTION CALLED TO GENERATE REPORTS TO task_overview.txt and user_overview.txt
def generate_reports():
    print()
    # Calculate values for task_overview.txt:
    # total_tasks
    total_tasks = len(task_list)
    # completed_tasks
    completed_tasks = 0
    for t in task_list:
        if t['completed'] == True:
            completed_tasks +=1
    # uncompleted_tasks
    uncompleted_tasks = total_tasks - completed_tasks
    
    # uncompleted_overdue_tasks
    uncompleted_overdue_tasks = 0
    date_today = datetime.today()

    for t in task_list:
        due_date = t['due_date']
        overdue = date_today > due_date
        if overdue and t['completed'] == False:
            uncompleted_overdue_tasks +=1
    # % incomplete tasks
    percentage_incomplete = uncompleted_tasks * 100 / total_tasks 

    # % overdue tasks
    percentage_overdue = uncompleted_overdue_tasks * 100 / total_tasks
    str_gr = "\nGENERATED TASK REPORTS: "
    str_gr +=(f"\nTotal tasks:                {total_tasks}")
    str_gr +=(f"\nCompleted tasks:            {completed_tasks}")
    str_gr +=(f"\nUncompleted tasks:          {uncompleted_tasks}")
    str_gr +=(f"\nUncompleted overdue tasks:  {uncompleted_overdue_tasks}")
    str_gr +=(f"\n% Incomplete tasks:         {percentage_incomplete}%")
    str_gr +=(f"\n% Overdue tasks:            {percentage_overdue}%")
    str_gr +=(f"\n\n--------------------------------------------------\n")

    

    # open task_overview.txt and write reports 
    with open("task_overview.txt", "w") as task_overview_file:
            print()
            task_overview_file.write(str_gr)
            print("Reports successfully added to task_overview.txt!\n")


    # Calculate values for user_overview.txt:
    # Total users
    total_users = len(username_password)
    # For each user: 
    users = list(username_password.keys())
    str_user_breakdown = ""

    for user in users:
        u_total_tasks = 0
        u_total_tasks_completed = 0
        u_uncompleted_overdue_tasks = 0
        
        for t in task_list:
            # Total tasks asigned to user, tasks completed and uncomplete overdue tasks:
            if t['username'] == user:
                u_total_tasks+=1
                if t['completed'] == True:
                    u_total_tasks_completed += 1
                    due_date = t['due_date']
                    overdue = date_today > due_date
                    if overdue:
                        u_uncompleted_overdue_tasks +=1
               
        # % of total tasks asigned to user
        u_percentage_total_tasks = u_total_tasks * 100 / total_tasks
        # % of tasks completed, pending, and overdue pending
        if u_total_tasks == 0:
            u_percentage_completed_tasks = 0
            u_percentage_pending_tasks = 0
            u_uncompleted_overdue_tasks = 0
        else:
            u_percentage_completed_tasks = u_total_tasks_completed * 100 / u_total_tasks
            u_percentage_pending_tasks = 100 - u_percentage_completed_tasks
            u_percentage_uncompleted_overdue_tasks = u_uncompleted_overdue_tasks * 100 / u_total_tasks

        str_user_breakdown += f'''{user}'s task reports:
Tasks assigned:                           {u_total_tasks}
% of total tasks assigned to user:        {u_percentage_total_tasks}%
% of their completed tasks:               {u_percentage_completed_tasks}%
% of their pending tasks:                 {u_percentage_pending_tasks}%
% of their overdue tasks:                 {u_percentage_uncompleted_overdue_tasks}%

\n\n'''
    str_u = "\nGENERATED USER REPORTS: "
    str_u +=(f"\nTotal users:                             {total_users}")
    str_u +=(f"\nTotal tasks:                             {total_tasks}")
    str_u +=(f"\n\n--------------------------------------------------\n")
    str_u +=(f"\nUSER BREAKDOWN REPORTS:\n{str_user_breakdown}")


    # open user_overview.txt and write reports 
    with open("user_overview.txt", "w") as user_overview_file:
            print()
            user_overview_file.write(str_u)
            print("Reports successfully added to user_overview.txt!\n")

# FUNCTION CALLED TO DISPLAY GENERATE REPORTS TO CONSOLE
def display_statistics():
    '''If the user is an admin they can display statistics about number of users
                and tasks.'''
    if not os.path.exists("task_overview.txt") :
        generate_reports()
        with open("task_overview.txt", 'r') as to_file:
            to_data = to_file.read()
            print("\n\n--------------------------------------------------")
            print(to_data)
    else: 
        with open("task_overview.txt", 'r') as to_file:
            to_data = to_file.read()
            print("\n\n--------------------------------------------------")
            print(to_data)

    if not os.path.exists("user_overview.txt"):
        generate_reports()   
        with open("user_overview.txt", 'r') as uo_file:
            uo_data = uo_file.read()
            print(uo_data)
    else: 
        with open("user_overview.txt", 'r') as uo_file:
            uo_data = uo_file.read()
            print(uo_data)



def menu():
    while True:
        # presenting the menu to the user and 
        # making sure that the user input is converted to lower case.
        print()
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
''').lower()

        if menu == 'r':
            reg_user()
        elif menu == 'a':
            add_task()
        elif menu == 'va':
            view_all()
        elif menu == 'vm':
            view_mine()
        elif menu == 'gr':
            generate_reports()
        elif menu == 'ds' and curr_user == 'admin': 
            display_statistics()
        elif menu == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("Invalid selection. Please try again")

menu()