from fastapi import FastAPI, HTTPException
from typing import List, Optional
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

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

class Product(BaseModel):
    id: int
    brand: str
    price: Optional[str]
    original_price: Optional[str]
    delivery_price: Optional[str]
    ratings: Optional[str]
    ratings_num: Optional[str]
    ratings_link: Optional[str]
    link: Optional[str]
    image_link: Optional[str]

@app.get("/products", response_model=List[Product])
def get_products(search: Optional[str] = None, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        base_query = "SELECT id, brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link FROM watch_data"
        filters = []
        params = []

        if search:
            filters.append("brand ILIKE %s")
            params.append(f"%{search}%")

        if filters:
            base_query += " WHERE " + " AND ".join(filters)

        base_query += " ORDER BY id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(base_query, params)
        products = cursor.fetchall()
        connection.close()

        if not products:
            raise HTTPException(status_code=404, detail="No products found.")

        return [
            Product(
                id=product[0],
                brand=product[1],
                price=product[2],
                original_price=product[3],
                delivery_price=product[4],
                ratings=product[5],
                ratings_num=product[6],
                ratings_link=product[7],
                link=product[8],
                image_link=product[9],
            )
            for product in products
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/top", response_model=List[Product])
def get_top_products():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT id, brand, price, original_price, delivery_price, ratings, ratings_num, ratings_link, link, image_link
            FROM watch_data
            WHERE ratings IS NOT NULL
            ORDER BY ratings_num DESC, ratings DESC
            LIMIT 5
        """
        cursor.execute(query)
        top_products = cursor.fetchall()
        connection.close()

        return [
            Product(
                id=product[0],
                brand=product[1],
                price=product[2],
                original_price=product[3],
                delivery_price=product[4],
                ratings=product[5],
                ratings_num=product[6],
                ratings_link=product[7],
                link=product[8],
                image_link=product[9],
            )
            for product in top_products
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}/reviews")
def get_product_reviews(product_id: int, page: int = 1, limit: int = 10):
    raise HTTPException(status_code=404, detail="Reviews are not available for this product.")
