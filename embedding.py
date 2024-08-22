from transformers import AutoTokenizer, AutoModel
import torch


def get_embeddings(text: str):

    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    text = "This is an example sentence"
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)

    sentence_embedding = outputs.last_hidden_state.mean(dim=1)
    sentence_embedding_np = sentence_embedding.numpy()

    print("Sentence Embedding", sentence_embedding_np)
    return sentence_embedding_np