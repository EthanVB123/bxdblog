# bxdblog
Semantic search for the businessxdesign.com.au blog

Note: scraper.py is very scrappy and not to be ran - it was just used to scrape the blog titles and links which are in BlogTitlesAndLinks.txt. No further use required, unless more blog posts are added. More maintainable solution is planned, but low priority.

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
