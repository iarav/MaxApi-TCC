#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install python-dotenv
pip install uvicorn
pip install fastapi
pip install sqlalchemy
pip install spacy

python3 -m spacy download pt_core_news_sm

pip install psycopg2-binary

uvicorn api.main:app --reload
