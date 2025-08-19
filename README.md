Installation
1. Clone the Repository
git clone https://github.com/sameer9860/Lead-Management-System
cd Todo-App(if you are in another dir)
2. Set Up Virtual Environment
python -m venv env
.\env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Create a Superuser (Admin)
python manage.py createsuperuser
Follow the prompts to set up the admin account.

6. Run the Development Server
python manage.py runserver
Access the application at http://127.0.0.1:8000.
