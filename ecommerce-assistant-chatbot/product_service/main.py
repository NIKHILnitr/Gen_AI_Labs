from fastapi import FastAPI, Query
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize FastAPI app
app = FastAPI(title="Product Service")

# Load product data on startup
print("Loading product data and computing embeddings...")
df_products = pd.read_csv("Product_Information_Dataset.csv")

# Fill NaNs in description or title to empty strings to avoid issues
df_products['title'] = df_products['title'].fillna('')
df_products['description'] = df_products['description'].fillna('')

# Combine title and description for embedding; this is the text corpus
documents = (df_products['title'] + '. ' + df_products['description']).tolist()

# Load a pre-trained sentence transformer model for embedding (downloaded at build/runtime)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings for all products (this may take a few seconds for 5000 items)
embeddings = model.encode(documents, convert_to_tensor=False)

@app.get("/search")
async def search_products(
    q: str = Query(None, description="Search query string"),
    category: str = Query(None, description="Filter by product category"),
    min_price: float = Query(None, description="Minimum price filter"),
    max_price: float = Query(None, description="Maximum price filter"),
    limit: int = Query(5, description="Number of top results to return")
):
    """
    Search products by query with optional filters. Uses vector similarity for RAG.
    """
    # Start with all products
    mask = np.array([True] * len(df_products))

    # Apply category filter if provided (case-insensitive match on categories field)
    if category:
        mask &= df_products['categories'].str.contains(category, case=False, na=False)

    # Apply price filters if provided
    if min_price is not None:
        mask &= df_products['price'] >= min_price
    if max_price is not None:
        mask &= df_products['price'] <= max_price

    # If a query string is provided, perform vector similarity search (RAG)
    if q:
        # Compute embedding for the query
        query_embedding = model.encode(q)
        # Compute cosine similarities between query and all product embeddings
        sims = cosine_similarity([query_embedding], embeddings)[0]
        # Mask out products that do not meet filter criteria
        sims = np.where(mask, sims, -np.inf)
        # Get indices of top-N similar products
        top_indices = sims.argsort()[::-1][:limit]
        # Retrieve the corresponding product rows
        results_df = df_products.iloc[top_indices]
    else:
        # No query provided: just filter and return first 'limit' products
        results_df = df_products[mask].head(limit)

    # Select fields to return in the response
    result_fields = ['title', 'price', 'average_rating', 'rating_number', 'store', 'categories', 'description']
    results = results_df[result_fields].to_dict(orient='records')
    return {"results": results}
