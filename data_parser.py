import json
import torch
from transformers import AutoModel, AutoTokenizer
from tqdm.auto import tqdm
import numpy as np


with open('/home/ql2004/projects/rate-prof-ai/jsondata/data1.json', 'r') as file:
    reviews = json.load(file)

chunks = []
for i in range(1,10):
    review = reviews[i]
    if review is None:
        print("skipping review at index {i}")
        continue
    professor = reviews[i]['prof_name']
    classes = reviews[i]['classes']
    quality = reviews[i]['quality']
    difficulty = reviews[i]['difficulty']
    text = "Professor: " + str(professor) + ", Classes: " + str(classes) + " Quality: " + str(quality) + " difficulty: " + str(difficulty)
    chunks.append(text)

device = "cuda" if torch.cuda.is_available() else "cpu" 

model_id = "intfloat/e5-base-v2"

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModel.from_pretrained(model_id).to(device)
model.eval()

def embed(docs: list[str]) -> list[list[float]]:
    docs = [f"passage: {d}" for d in docs]
    # tokenize
    tokens = tokenizer(
        docs, padding=True, max_length=512, truncation=True, return_tensors="pt"
    ).to(device)
    with torch.no_grad():
        # process with model for token-level embeddings
        out = model(**tokens)
        # mask padding tokens
        last_hidden = out.last_hidden_state.masked_fill(
            ~tokens["attention_mask"][..., None].bool(), 0.0
        )
        # create mean pooled embeddings
        doc_embeds = last_hidden.sum(dim=1) / \
            tokens["attention_mask"].sum(dim=1)[..., None]
    return doc_embeds.cpu().numpy()

# Embed data in batches
batch_size = 256
all_embeddings = []

for i in tqdm(range(0, len(chunks), batch_size)):
    i_end = min(len(chunks), i+batch_size)
    chunk_batch = chunks[i:i_end]
    # embed current batch
    embed_batch = embed(chunk_batch)
    all_embeddings.append(embed_batch)

all_embeddings = np.concatenate(all_embeddings, axis=0)

np.save('/home/ql2004/projects/rate-prof-ai/embeddings.npy', all_embeddings)

print(f"Embeddings shape: {all_embeddings.shape}")















