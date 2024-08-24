from QavaninCrawler import QavaninCrawler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv


# Loading environment variables from .env file
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Crawling before server is starting
    crawler = QavaninCrawler(3)
    crawler.start()
    yield    


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"hello": "world"}

