from transformers import AutoTokenizer, AutoModel
import torch
from os import getenv

        
DEFAULT_MODEL_NAME = getenv("MODEL_NAME")

class Embedding:
    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def get_embedding(self, text: str):
        # text = "This is an example sentence"
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        sentence_embedding = outputs.last_hidden_state.mean(dim=1)
        sentence_embedding_np = sentence_embedding.numpy()

        print("Sentence Embedding", sentence_embedding_np)
        return sentence_embedding_np
