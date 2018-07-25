#coding: utf-8
import requests
import json
import collections
import itertools
import networkx as nx
import matplotlib as mpl
mpl.use('Agg')
#%matplotlib inline
import matplotlib.pyplot as plt

class TagNetwork():
    def __init__(self):
        return
    def get_tags(self):
        pass
    def make_network(self):
        params = {"page":1, "per_page":100}
        items = []
        for i in range(5):
            print("fetching... page " + str(i + 1))
            params["page"] = i + 1
            res = requests.get("https://qiita.com/api/v2/items", params=params)
            #print(res)
            items.extend(json.loads(res.text))
        tags_list = []
        for item in items:
            tags = [tag["name"] for tag in item["tags"]]
            tags_list.append(tags)
        tag_count = collections.Counter(itertools.chain.from_iterable(tags_list)).most_common(50)
        G = nx.Graph()
        G.add_nodes_from([(tag, {"count":count}) for tag, count in tag_count])
        for tags in tags_list:
            for tag0, tag1 in itertools.combinations(tags, 2):
                if not G.has_node(tag0) or not G.has_node(tag1):
                    continue
                if G.has_edge(tag0, tag1):
                    G[tag0][tag1]["weight"] += 1
                else:
                    G.add_edge(tag0, tag1, weight=1)
        plt.figure(figsize=(13,13))
        pos = nx.spring_layout(G, k=1.5)

        node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)]
        nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=node_size, font_weight="bold", font_family='IPAexGothic')
        nx.draw_networkx_labels(G, pos, fontsize=14, font_family='IPAexGothic')

        edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)]
        nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color='r', width=edge_width)

        plt.axis('off')
        plt.savefig("./static/pic/tagnet.png")
        plt.show()
        plt.close()
if __name__ == "__main__":
    n = TagNetwork()
    n.make_network()
