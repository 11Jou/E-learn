# E-Learn
An online educational platform that allows every instructor to send invitations to their 
students to access their courses, whether they are live or recorded, and to take the 
exams for each lesson. It also enables the instructor to monitor their students' 
performance.

### Installation
1. Create virtual environment:

   ```bash
   python -m venv env
   cd env
   scripts\activate
   pip install django
   django-admin startproject project
   cd project

2. Clone the repository:

    ```bash
    git clone https://github.com/11Jou/E-learn.git
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

The project will be accessible at [http://localhost:8000/](http://localhost:8000/).
