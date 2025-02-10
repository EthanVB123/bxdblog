# Semantic Search AI
#note - chatgpt wrote this code, I edited it
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from flask import Flask, jsonify, request, render_template
from scraper import get_blogposts_as_json, areBlogpostsUpToDate # this is scraper.py not an external module
import json
import os
import time
# start flask app
app = Flask(__name__)
# Load the model
# model = SentenceTransformer('sentence-transformers/all-MPNet-base-v2') old model
model = SentenceTransformer('BAAI/bge-large-en-v1.5')


# Load the blogposts TODO store the blogposts in a file and load from there, no need to scrape every time, scrape if last modified was not today

blogposts = [] # placeholder so that the code runs, is defined later right before app.run

#if not os.path.exists('blogposts.json') or os.path.getmtime('blogposts.json') < time.time() - 86400:
#    blogposts = get_blogposts_as_json()
#else:
#    with open('blogposts.json', 'r', encoding='utf-8') as f:

#        blogposts = json.load(f)
    
def files_up_to_date():
    if not os.path.exists('blogposts.json') or os.path.getmtime('blogposts.json') < time.time() - 86400:
        print("blogposts.json is more than 1 day old")
        return False
    elif not os.path.exists('blog_embeddings.npy') or os.path.getmtime('blog_embeddings.npy') < time.time() - 86400:
        print("blog_embeddings.npy is more than 1 day old")
        return False
    elif not os.path.exists('faiss_index') or os.path.getmtime('faiss_index') < time.time() - 86400:
        print("faiss_index is more than 1 day old")
        return False
    elif not areBlogpostsUpToDate():
        print("blogposts are not up to date")
        return False
    else:
        return True




# Reloads blogposts, embeddings and index - to be called on startup if blogposts.json more than 12 hours old, or if query is made and there are new blogposts
def load_embeddings():
    # Scrape blogposts from the blog
    blogposts = get_blogposts_as_json()

    # Create embeddings for blogposts and save them to blog_embeddings.npy  
    embeddings = np.array([encode(post) for post in blogposts])
    np.save("blog_embeddings.npy", embeddings)

    # Create FAISS index to allow for efficient search and save it to faiss_index
    index = faiss.IndexFlatIP(embeddings.shape[1]) #brute force search by Euclidean distance is sufficient considering the small number of blogposts
    index.add(embeddings)
    faiss.write_index(index, "faiss_index")

    return blogposts, embeddings, index


def encode(post): # Encode post including title and text, with title having the same weight as all the text combined
    textSentences = post['text'].split('\n')
    titleSentence = post['title']
    titleEmbedding = model.encode([titleSentence], batch_size=8, convert_to_numpy=True) # batch size 8 is required on my machine with only 4GB VRAM
    textEmbeddings = model.encode(textSentences, batch_size=8, convert_to_numpy=True)
    textMean = np.mean(textEmbeddings, axis=0)
    k = 0.3  # Weight for title embedding
    sentenceEmbedding = (textMean + k * titleEmbedding[0]) / (1 + k)
    return sentenceEmbedding

# Search functionality, query is the (string) search query, top_k is the number of results to return (default is all)
def search(query, top_k=0): # top_k = 0 means all results
    query_embedding = model.encode([query], convert_to_numpy=True)
    if top_k <= 0 or top_k > len(blogposts):
        top_k = len(blogposts)
    else:
        top_k = int(top_k) #just in case - it must always be an integer
    print(f"Document embeddings dimension: {embeddings.shape[1]}")
    print(f"Query embedding dimension: {query_embedding.shape[0]}")
    distances, indices = index.search(query_embedding, top_k)
    results = [{**blogposts[i], 'similarity': float(distances[0][j])} for j, i in enumerate(indices[0])]
    return results



# Load the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Used by frontend to call search
@app.route('/callSearch', methods=['GET'])
def callSearch():
    # the following if block checks if the files are up to date and updates, hence eliminating the need to restart the server upon new blogposts
    # however, takes ~0.5s per query, so if you don't think it is worth it, remove it
    if not files_up_to_date():
        print("Files are not up to date")
        blogposts, embeddings, index = load_embeddings()
    query = request.args.get("query","No Query")
    result = search(query)
    return jsonify({"result": result})


if __name__ == "__main__": # if this is the file that is running, and not a module
    print("server running!")
    if files_up_to_date():
        print("Files are up to date")
        blogposts = json.load(open('blogposts.json'))
        embeddings = np.load('blog_embeddings.npy')
        index = faiss.read_index('faiss_index')
    else:
        print("Loading files")
        blogposts, embeddings, index = load_embeddings() # currently runs every restart, should be called only if blogposts.json is more than 12 hours old, or if query is made and there are new blogposts
    #print("Blogposts: "+str(blogposts))
    #print("Blogposts Length: "+str(len(blogposts)))
    app.run(host='0.0.0.0', port=5000)


