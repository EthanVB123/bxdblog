# Semantic Search AI
#note - chatgpt wrote this code, I edited it
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS # this will be removed later - allows requests from frontend, as they are different sources atm
print("start of code")
# start flask app
app = Flask(__name__)
CORS(app) # *** REMOVE FOR PRODUCTION THIS IS A SECURITY RISK *** (it makes ddos really easy)
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

# Create flask route
@app.route('/callSearch', methods=['GET'])
def callSearch():
    query = request.args.get("query","No Query")
    result = search(query)

    for index in range(len(result)):
        result[index] = (result[index][0], float(result[index][1]), result[index][2])
    #print("RESULT: "+str(result))
    return jsonify({"result": result})

##if __name__ == "__main__": # if this is the file that is running, and not a module
##    print("server running!")
##    app.run(debug=True)

