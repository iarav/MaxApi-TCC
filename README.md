# MaxApi-TCC
My Python API for the MAX TCC project

## Description
This is the project API, structured in Python. It has the necessary endpoints that will be used in the web system and all the chatbot logic.
To use it, it requires a configured PostgreSQL database called `max_chatbot`.

## Commands:
- Run this command only the first time to create a virtual environment in Python:<br>
`python -m venv venv` 
- Run this command every time to activate the Python environment:<br>
    - On Windows:<br>
  `venv\Scripts\activate`
    - On Unix or macOS:<br>
  `source venv/bin/activate`
- Run the following command to install all the requirements:
  `pip install -r requirements.txt` 
- Run this command to execute the API (Before this, follow Configuring Database steps):<br>
`uvicorn api.main:app --reload` 

### Install this dependencies if `pip install -r requirements.txt` does not work, run:
- pip install python-dotenv
- pip install uvicorn
- pip install fastapi
- pip install sqlalchemy
- pip install psycopg2
- pip install spacy
- python -m spacy download pt_core_news_sm

## Configuring Database:
1. Create a PostgreSQL database called `max_chatbot`.
2. Run the database script which is in the folder (`api\db\db_script`).
3. Create the .env file configuring the variable `DATABASE_URL` in the format: 
`postgresql://USER:PASSWORD@localhost:PORT_NUMBER/DB_NAME`

## Environment versions (venv):
- Python 3.11.4