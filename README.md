

## Project Manager System

  

## Overview

The **Project Manager System** is a custom-built solution tailored specifically for  
managing tasks within an IT company environment. With a diverse team comprising  
Developers, Designers, Project Managers, and QA specialists, the task manager  
aims to streamline project development by providing a centralized platform for  
task creation, assignment, and tracking.  
  

## Features

Task Creation: Team members can easily create tasks directly within the  
platform, specifying details such as task description, priority, deadline, and  
associated team members.  

Task Assignment: Tasks can be assigned to individual team members or groups,  
ensuring clear accountability and responsibility distribution.  

Task Tracking: The task manager allows for real-time tracking of task progress,  
enabling team members and project managers to monitor the status of each task.  

Deadline Management: Automatic reminders and notifications help keep everyone  
informed about upcoming deadlines, ensuring tasks are completed on time.  

Task Status Updates: Team members can mark tasks as done upon completion,  
providing visibility into the progress of projects and individual tasks.  

## Requirements

Python 3.12  
Django 5.0.4  
  
## Installation

**Clone the repository:**  

    git clone https://github.com/AlexGrytsai/ProjectManegerSystem.git

    cd project-manager-system

**Create a virtual environment and activate it:**  

    python3 -m veenter code herenv venv 

    source venv/bin/activate

**Install the dependencies:**  

    pip install -r requirements.txt

**Set up the database:**  

    python manage.py makemigrations  
    python manage.py migrate

**Create a superuser:**  

    python manage.py createsuperuser 

**Run the development server:**  

    python manage.py runserver 

## Usage

Access the application by navigating to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web  
browser. Log in with the superuser credentials to access the admin interface  
and start creating projects and tasks.  
  

## Description of main Views
 
**Project Views**  
*ProjectCreateView*: Allows a supervisor to create a new project.  
*ProjectListView*: Lists all projects with task and worker counts.  
*ProjectUpdateView*: Allows a supervisor to update project details.  
*ProjectDeleteView*: Allows a supervisor to delete a project.  
*ProjectDetailView*: Displays detailed information about a project.  
*ProjectDetailTasksView*: Displays the tasks associated with a project.  
  
**Task Views**  
*TaskListView*: Lists all tasks within a project.  
*TaskCreateView*: Allows the creation of a new task within a project.  
*TaskUpdateView*: Allows updating an existing task.  
*TaskDeleteView*: Allows deleting a task.  
*TaskDetailView*: Displays detailed information about a task.  
  
**Comment Views**  
*CommentCreatView*: Allows creating a new comment on a task.  
*CommentUpdateView*: Allows updating a comment.  
*CommentDeleteView*: Allows deleting a comment.  
  
**Utility Functions**  
*get_project*: Retrieves a project based on the provided project ID.  
*check_responsible_worker*: Checks if the current user is a responsible worker  
for the project.  
*toggle_assign_to_task*: Toggles the assignment of the current user to a task.  
  

## Conclusion

The **Project Manager System** is designed to enhance productivity and ensure  
efficient management of tasks and projects. With its user-friendly interface  
and comprehensive features, it caters to the needs of various roles within an  
IT company, fostering better collaboration and project oversight.
