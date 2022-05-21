seed_url = ['https://food.trueid.net/']
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import unquote 
import os,codecs
# import networkx as nx
# import matplotlib.pyplot as plt

import mimetypes
mimetypes.init()

headers = {
    'User-Agent': 'team123_bot',
    'From': 'wipawas.t@ku.th'
    }

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

# pagerank
# root_url = "https://www.ryoiireview.com/"
# g=nx.Graph()
# g.add_node(root_url)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def storeFile(url,raw_html):
  path = "C:/Users/User/Documents/webir/html_tid"
  abs_file = path
  os.makedirs(path, 0o755, exist_ok=True)
  splited_url = unquote(url).split('/')
  splited_url = [ele for ele in splited_url if ele.strip()]
  for name in splited_url:
    #if len(splited_url) > 2:
        if name != "https:":
            if name == splited_url[-1]:
                abs_file = path + '/' + name + '.html'
            else:
                path = path + '/' + name
                os.makedirs(path, 0o755, exist_ok=True)

  f = codecs.open(abs_file, 'w', 'utf-8')
  f.write(raw_html)
  f.close()

def delOtherDomain(url): 
    exception = 'https://food.trueid.net/'
    if exception in url:
        return True     
    return False

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    
    try:
          response = requests.get(url,headers = headers,timeout=5).content
          soup = BeautifulSoup(response, "html.parser")
    #       types = response.headers['Content-Type']
          for a_tag in soup.findAll("a"):
              href = a_tag.attrs.get("href")
              # if '.jpg' not in href and '.png' not in href: 
              if href == "" or href is None:
                  # href empty tag
                  continue
              # in the URL if it's relative (not absolute link)
              href = urljoin(url, href)
              parsed_href = urlparse(href)
              # remove URL GET parameters, URL fragments, etc.
              href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
              if delOtherDomain(href):
                if not is_valid(href):
                    # not a valid URL
                    continue
                if href in internal_urls:
                      # already in the set
                    continue
                mimestart = mimetypes.guess_type(href)[0]
                if mimestart != None:
                    mimestart = mimestart.split('/')[0]
                    print(mimestart)
                if domain_name not in href:
                      # external link
                      # (j[-3:]=='htm') or (j[-4:] =='html') or (j[-3:]=='php')
                    if href not in external_urls and mimestart not in ['audio', 'video', 'image']:
                          print(f"External link: {href}")
                          external_urls.add(href)
                          storeFile(href,str(soup))
                    continue
                if mimestart not in ['audio', 'video', 'image']:
                    print(f"Internal link: {href}")
                    storeFile(href,str(soup))
                    urls.add(href)
                    internal_urls.add(href)
    except HTTPError as http_err:
          print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
          print(f'Other error occurred: {err}')  # Python 3.6
    return urls

# number of urls visited so far will be stored here
total_urls_visited = 0

# root_url = "https://www.ryoiireview.com/"
# g=nx.Graph()
# g.add_node(root_url)
count = 0
def crawl(url, max_urls=10000):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print("[+] Total URLs:" + str(total_urls_visited))
    print(f"Crawling: {url}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        if delOtherDomain(link):
#             g.add_node(link)
#             g.add_edge(url,link)
            crawl(link, max_urls=max_urls)
    
if __name__ == "__main__":
    for link in seed_url:
      crawl(link)
      print("[+] Total Internal links:", len(internal_urls))
      print("[+] Total External links:", len(external_urls))
      print("[+] Total URLs:", len(external_urls) + len(internal_urls))
      # print("[+] Total crawled URLs:", max_urls)
#     pagerank = nx.pagerank_numpy(g, alpha=0.85, personalization=None,  weight='weight', dangling=None)
