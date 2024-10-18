# Watch Data Scraper with FastAPI

This project is a web scraping application that extracts watch data from Amazon, stores it in a PostgreSQL database, provides a RESTful API using FastAPI to interact with the data, and provides insights using RAG when user enters a question as a prompt. The application includes features such as search, filtering, sorting, and retrieving reviews for specific products.


## Features

- Web scraping of watch details, including brand, price, specifications, and user reviews from Amazon.
- Data persistence in a PostgreSQL database.
- RESTful API for accessing and manipulating watch data.
- Support for search, filter, and sort functionalities.
- Pagination for product lists and reviews.
- Prompt when user enters a question.

## Technologies Used

- Python
- FastAPI
- Selenium
- PostgreSQL
- SQLAlchemy
- dotenv
- webdriver-manager
- OpenAI
- langchain
  

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sajidZ-904/Markopolo.ai-Python-Developer-Project.git
   cd Markopolo.ai-Python-Developer-Project

2. Create a virtual environment and activate it:
   ```bash
   python -m venv virtualenv
   source virtualenv/Scripts/activate 

3. Install the required packages:
    ```bash
    pip install -r requirements.txt

4. Create a ```.env``` file in the root of your project directory and add the following variables:
   ```bash
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=watch_db
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password

### Running the application
1. Run the scraper to populate the database with watch data:
   ```bash
   python scraper.py

2. Start the FastAPI application:
   ```bash
   uvicorn main:app --reload

3. Run the RAG.py file for getting answers based on questions entered on prompt:
   ```bash
   python RAG.py

### API Endpoints

# GET ```/products```
  - **Description**: Retrieves a list of products with search, filter, and sort functionalities.
  - **Query Parameters**:
        a) ```brand```: Filter by brand.
        b) ```price_min```: Minimum price filter.
        c) ```price_max```: Maximum price filter.
        d) ```rating_min```: Minimum rating filter.
        e) ```page```: Page number for pagination.
        f) ```limit```: Number of results per page.
    
# GET ```/products/top```
  - **Description**: Returns the top products based on average rating and number of reviews.
  - **Response**: List of top products and their reviews.
    
# GET ```/products/{product_id}/reviews```
  - **Description**: Retrieves all reviews for a specific product.
  - **Path Parameter**:
    ```product_id```: ID of the product to retrieve reviews for.
  - **Query Parameters**:
      a) ```page```: Page number for pagination.
      b) ```limit```: Number of reviews per page.

After running RAG.py, enter the question as prompt and the system will provide insights based on the question entered.

### License
This project is licensed under the MIT License.
