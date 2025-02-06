# Semantic Search AI
#note - chatgpt wrote this code, I edited it
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from flask import Flask, jsonify, request, render_template
from scraper import get_blogposts_as_json # this is scraper.py not an external module
# start flask app
app = Flask(__name__)
# Load the model
model = SentenceTransformer('sentence-transformers/all-MPNet-base-v2')

# Load the blogposts TODO store the blogposts in a file and load from there, no need to scrape every time, scrape if last modified was not today
blogposts = get_blogposts_as_json()
blogTitles = [post['title'] for post in blogposts]

#Create embeddings
#embeddings = model.encode(blogTitles, convert_to_numpy=True)

def encode(post, titleWeight=1): # Encode post including title and text
    textSentences = post['text'].split('\n')
    titleSentence = post['title']
    titleEmbedding = model.encode([titleSentence], convert_to_numpy=True)
    textEmbeddings = model.encode(textSentences, convert_to_numpy=True)
    textMean = np.mean(textEmbeddings, axis=0)
    sentenceEmbedding = np.mean([textMean, titleEmbedding[0]], axis=0)

    return sentenceEmbedding

embeddings = np.array([encode(post) for post in blogposts])

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
    results = [{**blogposts[i], 'similarity': float(distances[0][j])} for j, i in enumerate(indices[0])]
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

    #for index in range(len(result)):
    #    result[index] = (result[index][0], float(result[index][1]), result[index][2])
    #print("RESULT: "+str(result))
    return jsonify({"result": result})

if __name__ == "__main__": # if this is the file that is running, and not a module
    print("server running!")
    app.run(host='0.0.0.0', port=5000)

