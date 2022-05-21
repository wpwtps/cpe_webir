from glob import escape
import os, codecs
from unittest import skip

dir_name = 'C:\\Users\\User\Documents\\webir\\html'
#dir_name = 'D:\\html_aj'
url_file = 'urllist.txt'
protocol = 'http://'

# Get the list of all files in directory tree at given path
list_of_urls = []
for (dir_path, dir_names, filenames) in os.walk(dir_name):
    dir_path = dir_path[len(dir_name)+1:]
    list_of_urls += [protocol + os.path.join(dir_path, file).replace('\\', '/') for file in filenames]

#print('list_of_urls',list_of_urls)
# Print the URLs
f = codecs.open(url_file, 'w', 'utf-8')
for url in list_of_urls:
    try: 
        f.write(url + '\n')
        print(url)
    except:
        continue
f.close()


import codecs

def read_file(file):
    f = codecs.open(file, 'r', 'utf-8')
    raw_html = f.read()
    f.close()
    return raw_html

def link_parser(raw_html):
    urls = [];
    pattern_start = '<a href="';  pattern_end = '"'
    index = 0;  length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            link = raw_html[start:end]
            if len(link) > 0:
                if link not in urls:
                    urls.append(link)
            index = end
        else:
            break
    return urls

from urllib.parse import urljoin

def url_normalization(base_url, link):
    return urljoin(base_url, link)

wg_file = 'webgraph_all2.txt'
f = codecs.open(wg_file, 'w', 'utf-8')

webgraph = []

print("len(list_of_urls)", len(list_of_urls))

count = 0
for url in list_of_urls:
    count +=1 
    try:
        print(url)
    except: 
        pass
    file = os.path.join(dir_name, url.replace(protocol, ''))
    raw_html = read_file(file)
    #print("raw_html", raw_html)
    links = link_parser(raw_html)
    outlinkIDs = []
    for link in links:
        #print("raw_html", raw_html)
        #print("linkkkkkk", link)
        #print("urlllllll", url)
        outlink = url_normalization(url, link)
        #print("outlinkkk", outlink)
        out_start = outlink.find('//')
        outlink = outlink[out_start+2:-1]
        outlink = "http://" + outlink
        selement = str(list_of_urls).find(outlink)
        eelement = str(list_of_urls).find("'", selement,-1)
        outlink = str(list_of_urls)[selement:eelement]
        #print("outlinkkk2", outlink)
        try:
            # print("outlinkkk", outlink)
            outlinkIDs.append(list_of_urls.index(outlink))
        except ValueError as error:
            pass; #print(error)

    # Make a unique and sorted list
    outlinkIDs = list(set(outlinkIDs))
    outlinkIDs.sort()

    outlinkIDs_str = ','.join(map(str, outlinkIDs))
    print("outlinkIDs",outlinkIDs)
    if outlinkIDs_str == '':
        outlinkIDs_str = '-'
    f.write(outlinkIDs_str + '\n')
    print(' -->', outlinkIDs_str)

    webgraph.append(outlinkIDs)
    print("count", count)

    #if input('next: ') == 'n':
    #    break
f.close()


import codecs

def pagerank(webgraph):
    nodes   = len(webgraph)
    print('webgraph',len(webgraph))

    pr_prev = [1/nodes] * nodes
    print('pr_prev',pr_prev)
    pr_curr = [0] * nodes
    print('pr_curr',len(pr_curr))
    alpha   = 0.85
    epsilon = 0.0000000001

    round = 0
    while True:
        round += 1
        
        # Reset scores to zero
        pr_curr = [0] * nodes

        # Compute PageRank
        for id in range(nodes):
            outlinks = webgraph[id]
            outdegree = len(outlinks)
            print("outlink", outlinks)
            for link in outlinks:
                pr_curr[link] += pr_prev[id]/outdegree

        # Solve the rank leak problem
        leak = 1 - sum(pr_curr)
        for id in range(nodes):
            pr_curr[id] += leak/nodes

        # Solve the rank sink problem
        for id in range(nodes):
            pr_curr[id] = (alpha*pr_curr[id]) + ((1-alpha)*(1/nodes))

        # Check error
        error = 0
        for id in range(nodes):
            error += abs(pr_curr[id] - pr_prev[id])
        if error < epsilon:
            return pr_curr

        #print(pr_curr)
        print(f'round {round:>3} -> sum = {sum(pr_curr)}, error = {error}')
    
        pr_prev = pr_curr

## ---- main program ----
pr_score_file = 'page_scores2.txt'
full_path = os.path.join('C:\\Users\\User\\Documents\\webir\\test', 'page_scores_all2.txt')

pr_scores = pagerank(webgraph)

f = codecs.open(full_path, 'w', 'utf-8')
nodes = len(webgraph)
print("nodes",nodes)
for id in range(nodes):
    f.write(list_of_urls[id] + ',' + str(pr_scores[id]) + '\n')
f.close()
# print("list_of_urls",list_of_urls)
