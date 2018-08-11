#coding: utf-8
import requests
import json
import collections
import itertools
import networkx as nx
from networkx.readwrite import json_graph
import matplotlib as mpl
mpl.use('Agg')
#%matplotlib inline
import matplotlib.pyplot as plt

class TagNetwork():
    def __init__(self):
        return
    def get_tags(self):
        #記事取得
        params = {"page":1, "per_page":100}
        items = []
        for i in range(5):
            print("fetching... page " + str(i + 1))
            params["page"] = i + 1
            res = requests.get("https://qiita.com/api/v2/items", params=params)
            #print(res)
            items.extend(json.loads(res.text))
        self.tags_list = []
        for item in items:
            tags = [tag["name"] for tag in item["tags"]]
            self.tags_list.append(tags)
        self.tag_count = collections.Counter(itertools.chain.from_iterable(self.tags_list)).most_common(50)

    def make_network(self):
        #ネットワーク図の作成
        G = nx.Graph()
        G.add_nodes_from([(tag, {"count":count}) for tag, count in self.tag_count])
        for tags in self.tags_list:
            for tag0, tag1 in itertools.combinations(tags, 2):
                if not G.has_node(tag0) or not G.has_node(tag1):
                    continue
                if G.has_edge(tag0, tag1):
                    G[tag0][tag1]["weight"] += 1
                else:
                    G.add_edge(tag0, tag1, weight=1)

        self.G = G####

        #画像として保存
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

    def make_json(self):
        self.network_json = json_graph.node_link_data(self.G)

if __name__ == "__main__":
    n = TagNetwork()
    n.get_tags()
    n.make_network()
