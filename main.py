from QavaninCrawler import QavaninCrawler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from db import DB
from embedding import Embedding

# Loading environment variables from .env file
load_dotenv()

# Initialize Embedding model
embedding = Embedding()

# Create database
db = DB(embedding)

# craete crawler
crawler = QavaninCrawler(db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crawling before server is starting
    crawler.start()
    yield    
    # Close connection to database
    db.close_connection()


app = FastAPI(lifespan=lifespan)


@app.get("/search")
def read_root():

    return {"hello": "world"}

