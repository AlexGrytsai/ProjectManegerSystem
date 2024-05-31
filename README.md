

## Project Manager System

  

## Overview

The **Project Manager System** is a custom-built solution tailored specifically for  
managing tasks within an IT company environment. With a diverse team comprising  
Developers, Designers, Project Managers, and QA specialists, the task manager  
aims to streamline project development by providing a centralized platform for  
task creation, assignment, and tracking.  

[projectmanegersystem.onrender.com](projectmanegersystem.onrender.com)

You can try the service with a guest account:
**Login:** Guest
**Password:** Guest!123456
  

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

***ProjectCreateView***: Allows a supervisor to create a new project.  
![Create new project](https://previews.dropbox.com/p/thumb/ACTWBo4ijzU_mN-zdeBCdVJ3VZtLLk82cnqRqcFJLSY7hjfiA0g8e1bHC8Hbe7JHpQ1Xo_ks98EcpXxgKIjcVVGojCQjNjOkLQg1hiaX1dZnRIY0vi4iP7xeteRHJHWvED42ZTDO_yIUvMwoSEZXeJe1mVds3Yk-Vt5fxg2lLIBRRK_gt2_5kA36LlNaeHCGFX066M5xP6-CjnBqC7zqPpAp1KJyWlBZYntv1kM1Scw4m3pUJZWZGknGvmzMempQBmiA1MQCACudS6e4Jv2kiv46aQrVBa7JNctlrKBnMbjMrd-_zlO3QM7Id_WTUT4KL_8a9km5G18g7suSLpNLs46Z/p.jpeg)
***ProjectListView***: Lists all projects with task and worker counts.  
***ProjectUpdateView***: Allows a supervisor to update project details.  
![Update project](https://previews.dropbox.com/p/thumb/ACRA68Ru2Vhk1hn2WeXnYgSWH55gBJqqP77lDZUTXNN2-OnxsaPBYxxweZQldIcKrPjhgJ2LBdqayerMi5seFF1GsURfeojy0z76bi9kOiBHqZkD1DXg__ohZp1Zw-NNZIMP8aS3-PB9_nh4EppZ4qwvc9-nbHQ1nvqdhrM-9oeMOFG3rOSFryKcT1qlXy0jenL718cYS8bIhZQ_SY7oLPk-lovwHuPTZulNu0H4uivC1BQ1-A56ve5o4jfm6g6TEtSSKkAxydf8xBgNO-AaoYK4xufR2hM_MWWQmrTmnUDqpbLLQxrdxdVpMiNxPV67xxI32gtLRKeKHiQtaVAOxXZ0/p.jpeg)
***ProjectDeleteView***: Allows a supervisor to delete a project.  
***ProjectDetailView***: Displays detailed information about a project.  
***ProjectDetailTasksView***: Displays the tasks associated with a project.  
  
**Task Views**  

***TaskListView***: Lists all tasks within a project.  
***TaskCreateView***: Allows the creation of a new task within a project.  
![Create new task](https://previews.dropbox.com/p/thumb/ACSzAf-rF0Q3_ueB0IlnCFMr5ZbtXCEODhJdsscQcIFI47HXPLSpgmo093tuk8PhriyL3gakUkY2Wgur0f9BVdaTpdjmb6yUgYTB6DJ3QT5xPYI_L1jc4346PfWWfL3r09jGqP7brVM7SDWRoXW6ohGcvmpKiRetMlhCeW4-FeXQP_bkwSnK6rSVFuPbPSmAfCxPowMAal2QqmSBAOnH-cbqGYwTgNrlSGHy4lZgkGREkOIn9kmKtru_AKDwB5ABGKQM6rdB2_owIvxQHm-AL8rSMMg1bKqpkuUQlYVUHuZtbmnyEbLLzlc8g1-r7UMBfmj9SYrtnkJthOCrjtczetuu/p.jpeg)
***TaskUpdateView***: Allows updating an existing task.  
![Update task](https://previews.dropbox.com/p/thumb/ACS90InKLpzY-9OXBKuClp-wNpjuvyJT5X-TAdx_V7ds9co4ORwObL284NgV-RvMnntJLHCKGNwWRp7hJqL3F-z06ev2M0PpvrnVwHApKq4Zlq83W5nFs1Ka4XXWQYzAYL5JKAcoP3JAWrMC5kf5qgEZQaN9fUdeqdgcfWy3R7gqYOOHLru5inyN68xmcn7Me4acHgynYUGiRwiO_Njwmlr1zU4q5EX8b-YCSt525FJIHBFf34aEg_ACIlaiUmqLGOYwPoahSHRFGwwWV_cUKIaDZAfcRYRxH5F5bZ0uFaxBHkTMG9PI2Io71xsTHks09w-sDsRD3ndwZ5z9xNKSmY17/p.jpeg)
***TaskDeleteView***: Allows deleting a task.  
***TaskDetailView***: Displays detailed information about a task.  
![Task detail](https://previews.dropbox.com/p/thumb/ACQX72P64eDcFli09ESc1YvORAQpYolkGkbl3hWLHf_VbnQCcp3xZZASHZSNgL19kG23wkEgr8rGkT8JBYrfurzodySqeZvPkfyyGo1SibdHy1T0pAjRCzXBBFNmi-F2QuhdO20dv4hZWSs_LZoJw08KbfJMx6wsesF_TaSpSaZQgsV_4nXCkq_eWxAEdudcngLiZ3nj9EjoZq_IjGl7CkKQXz9XwfczK06O8T9UQ4nWJ4dFN3NLLNKNXgr_QDBQ0RUJeZ9JU_uCc-ecBJHtIHKYXH1cJE7V0S2C2BW3Y9SPzIV6HV_IiQsSF1oPj9h51TAg1TJ2FNca4-VQEsfBC6a7/p.jpeg)
  
**Comment Views**  

***CommentCreatView***: Allows creating a new comment on a task.  
***CommentUpdateView***: Allows updating a comment.  
***CommentDeleteView***: Allows deleting a comment.  
  
**Utility Functions**  

***get_project***: Retrieves a project based on the provided project ID.  
***check_responsible_worker***: Checks if the current user is a responsible worker  
for the project.  
***toggle_assign_to_task***: Toggles the assignment of the current user to a task.  
  

## Conclusion

The **Project Manager System** is designed to enhance productivity and ensure  
efficient management of tasks and projects. With its user-friendly interface  
and comprehensive features, it caters to the needs of various roles within an  
IT company, fostering better collaboration and project oversight.
