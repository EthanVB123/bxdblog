import requests
from bs4 import BeautifulSoup
import time
import re
import json
target_url = "https://www.businessxdesign.com.au/blog"
post_prefix = "https://www.businessxdesign.com.au/"

class BlogPost:
    def __init__(self, title, text, image_url, url):
        self.title = title
        self.text = text
        self.image_url = image_url
        self.url = url

    def __str__(self):
        return f"Title: {self.title}\nText Length: {len(self.text)}\nImage URL: {self.image_url}\nURL: {self.url}"


def read_site(url, printText=False, log=False):
    if log:
        print(f"Reading from {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching {url}: {e}")
        return "ERROR"

    if printText:
        print(response.text)
    return response.text

    
#print(len(blogposts))
#print(blogposts[0])
def getBlogposts():
    """Returns a list of BlogPost objects for every blog post"""
    blogposts_list = []
    
    html = read_site(target_url)
    soup = BeautifulSoup(html, "html.parser")
    blogpost_links = soup.find_all("a", href=re.compile("^/post/.*"))
    href_values = [link.get('href') for link in blogpost_links if link.get('href')]
    href_values = list(set(href_values))  # Remove duplicates

    for post in href_values:
        url = post_prefix + post
        #print(f"Reading from {url}")
        soup = BeautifulSoup(read_site(url), "html.parser")
        
        blog_image = soup.find("div", class_="blog-image-wrapper").find("img")
        
        blogposts_list.append(BlogPost(
            soup.h2.text.encode("latin1").decode("utf-8"),
            soup.find("div", class_="rich-text").get_text(separator="\n").encode("latin1").decode("utf-8"),
            blog_image["src"],
            url
        ))
        
    return blogposts_list

def areBlogpostsUpToDate():
    """Returns True if the number of blog posts is up to date, False otherwise"""
    html = read_site(target_url)
    soup = BeautifulSoup(html, "html.parser")
    blogpost_links = soup.find_all("a", href=re.compile("^/post/.*"))
    href_values = [link.get('href') for link in blogpost_links if link.get('href')]
    href_values = list(set(href_values))
    return len(href_values) == len(json.load(open('blogposts.json')))





def get_blogposts_as_json():
    posts = getBlogposts()
    with open('blogposts.json', 'w', encoding='utf-8') as f:
        json.dump([post.__dict__ for post in posts], f, indent=4)
    return [post.__dict__ for post in posts]

#print(get_blogposts_as_json())
