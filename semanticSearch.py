# Semantic Search AI
#note - chatgpt wrote this code, I edited it
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from flask import Flask, jsonify, request, render_template

# start flask app
app = Flask(__name__)
# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

datafile = "blogTitlesAndLinks.txt" #note this is hand-cleaned

blogPosts = {} # title : url
with open(datafile, "r") as blogs:
    text = blogs.read().splitlines()
    for i in range(0, len(text), 2):
        blogPosts[text[i]] = text[i+1]
blogTitles = list(blogPosts)

#Create embeddings
embeddings = model.encode(blogTitles, convert_to_numpy=True)

# Save embeddings to disk (optional)
np.save("blog_embeddings.npy", embeddings)

# Initialize FAISS index
dimension = embeddings.shape[1]  # Embedding size
index = faiss.IndexFlatL2(dimension) #creates index - flat means brute force search, L2 = Euclidean distance
index.add(embeddings)

# Save index to disk (optional)
faiss.write_index(index, "faiss_index")

# Search functionality
def search(query, top_k=len(blogTitles)):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [(blogTitles[i], distances[0][j], blogPosts[blogTitles[i]]) for j, i in enumerate(indices[0])]
    return results

# Example search
query = "manage work life balance"
results = search(query)
print("Search Results:", results)


# Load the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Used by frontend to call search
@app.route('/callSearch', methods=['GET'])
def callSearch():
    query = request.args.get("query","No Query")
    result = search(query)

    for index in range(len(result)):
        result[index] = (result[index][0], float(result[index][1]), result[index][2])
    #print("RESULT: "+str(result))
    return jsonify({"result": result})

if __name__ == "__main__": # if this is the file that is running, and not a module
    print("server running!")
    app.run(host='0.0.0.0', port=5000)

