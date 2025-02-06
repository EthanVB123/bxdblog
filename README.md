# bxdblog
Semantic search for the businessxdesign.com.au blog



## Usage
You need the following:
Python 3.10+
The following python packages:
- sentence_transformers
- faiss-cpu
- flask
- numpy

Use the following command to run the server:
```
python semanticSearch.py  
```
The server will run on port 5000. It is currently configured to run on all interfaces, so it will be accessible from any device on the same network, but not from the internet.

If more blog posts are added, simply restart the server to redo the web scraping and embedding. Currently, server takes a while (~20 seconds) to restart, even if no new blog posts are added, working on that!
