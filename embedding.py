from transformers import AutoTokenizer, AutoModel
import torch
from os import getenv
import logging
import time

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)
        
DEFAULT_MODEL_NAME = getenv("MODEL_NAME")

class Embedding:
    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        logging.info(f"Embedding: Initializing the model")
        self.model_name = model_name
        while True:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModel.from_pretrained(model_name)
                break
            except Exception as e:
                logging.exception(f"Embedding: something got wrong while getting the model. trying again ...")
                time.sleep(1)

    def get_embedding(self, text: str):
        # text = "This is an example sentence"
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        sentence_embedding = outputs.last_hidden_state.mean(dim=1)
        sentence_embedding_np = sentence_embedding.numpy()

        return sentence_embedding_np
