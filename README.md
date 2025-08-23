#Installation
1. Clone the Repository
git clone https://github.com/sameer9860/Lead-Management-System

2.cd lead-management-system(if you are in another dir)

3. Set Up Virtual Environment
python -m venv env

4.\env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux

5. Install Dependencies
pip install -r requirements.txt

7. Apply Migrations
python manage.py migrate

9. Create a Superuser (Admin)
python manage.py createsuperuser
Follow the prompts to set up the admin account.

10. Run the Development Server
python manage.py runserver
Access the application at http://127.0.0.1:8000.
