# User Guide

## Installation and Setup Instructions  

This guide provides step-by-step instructions on installing and running the student archive application built with Python, Flask, and PostgreSQL.  

### Prerequisites  
Before installing the application, ensure you have the following tools installed:  
- Python (version 3.10 or newer)  
- PostgreSQL (version 13 or newer)  
- Git  
- A compatible web browser (e.g., Chrome, Firefox, Edge)  

### Installation Steps  
1. **Clone the Repository**  
   Open a terminal and run:  
   ```bash  
   git clone <repository-url>  
   cd <repository-folder>  
   ```  

2. **Set Up a Virtual Environment**  
   Create and activate a Python virtual environment:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate   # On Windows: venv\Scripts\activate  
   ```  

3. **Install Dependencies**  
   Install the required Python packages:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Set Up the Database**  
   - Create a PostgreSQL database named `student_archive`.  
   - Update the `config.py` file with your database credentials in .env-file:  
     ```python  
     DATABASE_URL = 'postgresql://username:password@localhost/student_archive'
     SECRET_KEY = your_key
     ```  

5. **Run Database Migrations**  
   Apply the database migrations to set up tables:  
   ```bash  
   flask db upgrade  
   ```  

6. **Run the Application**  
   Start the Flask development server:  
   ```bash  
   flask run  
   ```  
   The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).  

