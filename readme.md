1. Clone the repository
   git clone (repository link)
   cd taskmanager

2. Create & activate virtual environment (optional)
   python -m venv venv
   venv\Scripts\activate

3. Install required packages
   pip install -r requirements.txt

4. Run migrations
   python manage.py migrate

5. Create superuser
   python manage.py createsuperuser

6. Start the server
   python manage.py runserver

Visit the app:
http://127.0.0.1:8000/

All screenshots are:

### Login Page

![Login](taskmanager/media/Images/login.png)

### Register

![Register](taskmanager/media/Images/register.png)

### Create Task

![Create Task](taskmanager/media/Images/createtask.png)

### update Task

![update Task](taskmanager/media/Images/updatetask.png)

### Task list

![Task list](taskmanager/media/Images/tasklist.png)

### Task details

![Task details](taskmanager/media/Images/taskdetails.png)

### user profile

![user profile](taskmanager/media/Images/userprofile.png)

### Delete confirmation

![Delete confirmation](taskmanager/media/Images/deleteconfirmation.png)
