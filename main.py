from QavaninCrawler import QavaninCrawler
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from db import DB
from embedding import Embedding
from utils import cosine_similarity

# Loading environment variables from .env file
load_dotenv()

# Initialize Embedding model
embedding = Embedding()

# # Create database
db = DB(embedding)

# # craete crawler
# crawler = QavaninCrawler(db)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Crawling before server is starting
#     crawler.start()
#     yield    
#     # Close connection to database
#     db.close_connection()


# app = FastAPI(lifespan=lifespan)
app = FastAPI()


@app.get("/search")
def read_root(q: str = None):
    # get embeddings
    query_embedding = embedding.get_embedding(q)
    scores = {}
    for (id, text, text_embedding) in db.fetch_all():
        score = cosine_similarity(text_embedding.squeeze(), query_embedding.squeeze())
        scores[f"https://qavanin.ir/Law/TreeText/?IDS={id}"] = score

    sorted_scores = dict(sorted(scores.items(), key=lambda item: -item[1]))
    return {"results": sorted_scores}

