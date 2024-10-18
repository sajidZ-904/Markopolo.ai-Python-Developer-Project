from transformers import pipeline
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database configuration from .env
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def retrieve_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "SELECT brand, price, ratings, link FROM watch_data"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return []

def generate_response(query_text):
    data = retrieve_data()
    if not data:
        return "No data available to answer your query."

    # Use the data as context to answer the question using a pipeline
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    context = "\n".join([f"Brand: {item[0]}, Price: {item[1]}, Ratings: {item[2]}, Link: {item[3]}" for item in data])

    response = qa_pipeline(question=query_text, context=context)
    return response["answer"]

if __name__ == "__main__":
    user_query = input("Ask a question about watches: ")
    print(generate_response(user_query))
