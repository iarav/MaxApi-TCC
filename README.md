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
- Run this command to execute the API:<br>
`uvicorn api.main:app --reload` 

## Configuring Database:
1. Create a PostgreSQL database called `max_chatbot`.
2. Run the database script which is in the folder (`api\db\db_script`).
3. Create the .env file configuring the variable `DATABASE_URL` in the format: 
`postgresql://USER:PASSWORD@localhost:PORT_NUMBER/DB_NAME`

## Environment versions (venv):
- Python 3.7.4

### Installing dependencies
- pip install uvicorn   
- pip install fastapi   
- pip install sqlalchemy
- pip install psycopg2

### Packages
If there is any problem when executing the API, you can check the installed dependencies with the command `pip list`.<br>
The necessary packages are:

| Package             | Version |
|---------------------|---------|
| annotated-types     | 0.5.0   |
| anyio               | 3.7.1   |
| click               | 8.1.7   |
| colorama            | 0.4.6   |
| exceptiongroup      | 1.2.2   |
| fastapi             | 0.103.2 |
| greenlet            | 3.0.3   |
| h11                 | 0.14.0  |
| idna                | 3.7     |
| importlib-metadata  | 6.7.0   |
| pip                 | 19.0.3  |
| psycopg2-binary     | 2.9.9   |
| pydantic            | 2.5.3   |
| pydantic-core       | 2.14.6  |
| setuptools          | 40.8.0  |
| sniffio             | 1.3.1   |
| SQLAlchemy          | 2.0.32  |
| typing-extensions   | 4.7.1   |
| starlette           | 0.27.0  |
| uvicorn             | 0.22.0  |
| zipp                | 3.15.0  |