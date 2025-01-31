import requests
from bs4 import BeautifulSoup
import time
import re
target_url = "https://www.businessxdesign.com.au/blog"
post_prefix = "https://www.businessxdesign.com.au/"
def read_site(url, printText=False, log=False):
    if log:
        print(f"Reading from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return "ERROR"

    if printText:
        print(response.text)
    return response.text

html = read_site(target_url)

soup = BeautifulSoup(html, "html.parser")
blogpost_links = soup.find_all("a", href=re.compile("^/post/.*"))
href_values = [link.get('href') for link in blogpost_links if link.get('href')]
href_values = list(set(href_values)) # to remove duplicates

# at this point, href_values stores a link to every blog post

#href_values_test = href_values[:2] #as not to overload the system

# following finds all blog post names
for post in href_values:
    url = post_prefix + post
    soup = BeautifulSoup(read_site(url), "html.parser")
    #print(soup.get_text())

    
    print(soup.h2.string.replace("â","'")) #the titles
    print(url) #the links

    #image_elements = soup.find_all('img', class_ = "image-cover")
    #image_urls = [img['src'] for img in image_elements]
    #print(image_urls)
    #print(soup.img["src"])
    
