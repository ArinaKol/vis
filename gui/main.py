import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import csv

def read_relation_triples(file_path):
    print("read relation triples:", file_path)
    if file_path is None:
        return set(), set(), set()
    triples = set()
    entities, relations = set(), set()
    file = open(file_path, 'r', encoding='utf8')
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 3
        h = params[0].strip()
        r = params[1].strip()
        t = params[2].strip()
        triples.add((h, r, t))
        entities.add(h)
        entities.add(t)
        relations.add(r)
    return triples, entities, relations

def find_rel(gr, v_1, v_2):
    i = 0
    j = 0
    ij = -1
    for n in gr.nodes():
        wt = gr.nodes[n]['title']
        ij = ij + 1
        if wt == v_1:
            v11 = gr.nodes[n]['id']
            i = 1
        if wt == v_2:
            v22 = gr.nodes[n]['id']
            j = 1
        if j == 1 and i == 1:
            return 1, v11, v22
    #if i == 0:
    #    v11 = ij+1
    #    if j == 0:
    #        v22=ij+2
    #        return 0, v11, v22
    #    return 3, v11, v22
    #elif j == 0:
    #    v22 = ij+1
    #    return 2, v11, v22
    return 0, 0, 0


G = nx.Graph()
with open('RDGCN_EN_RU_15K_V1_xlnet.csv', encoding="utf8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
       G.add_node(int(row['ent1_id']), id=int(row['ent1_id']), id2=int(row['ent2_id']), pos=(float(row['x']), float(row['y'])), color = 'darkblue' if row['lang'] == 'en' else 'crimson', lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'], x=(float(row['x'])), y=float(row['y']))
pos_=nx.get_node_attributes(G, 'pos')
pos=dict()
for p in pos_:
    p1=np.array([pos_[p][0],pos_[p][1]])
    pos[p]=p1

rel_triples_1, _, _ = read_relation_triples('rel_triples_1')
for triplet in rel_triples_1:
    v1 = triplet[0][28:]
    v2 = triplet[2][28:]
    r = triplet[1][28:]
    k, w1, w2 = find_rel(G, v1, v2)
    if k == 1:
    #    G.add_node(w1, id=w1, id2=0,pos=(float(row['x']), float(row['y'])), color='darkblue' if row['lang'] == 'en' else 'crimson',lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'],x=(float(row['x'])), y=float(row['y']))
    #    G.add_node(w2, id=w2, id2=0,pos=(float(row['x']), float(row['y'])), color='darkblue' if row['lang'] == 'en' else 'crimson',lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'],x=(float(row['x'])), y=float(row['y']))
        G.add_edge(w1, w2, rel=r)
rel_triples_1, _, _ = read_relation_triples('rel_triples_2')
for triplet in rel_triples_1:
    v1 = triplet[0][28:]
    v2 = triplet[2][28:]
    r = triplet[1][28:]
    k, w1, w2 = find_rel(G, v1, v2)
    if k == 1:
    #    G.add_node(w1, id=w1, id2=0,pos=(float(row['x']), float(row['y'])), color='darkblue' if row['lang'] == 'en' else 'crimson',lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'],x=(float(row['x'])), y=float(row['y']))
    #    G.add_node(w2, id=w2, id2=0,pos=(float(row['x']), float(row['y'])), color='darkblue' if row['lang'] == 'en' else 'crimson',lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'],x=(float(row['x'])), y=float(row['y']))
        G.add_edge(w1, w2, rel=r)

fig, ax = plt.subplots()
#pos = nx.spring_layout(G)
color_map = []
nn=nx.get_node_attributes(G, 'color')
for node in nn:
    color_map.append(str(nn[node]))
nx.draw_networkx_nodes(G, node_color = color_map, pos=pos, ax=ax)
edges = nx.draw_networkx_edges(G, pos=pos, ax=ax)
nodes = nx.draw_networkx_nodes(G, node_color = color_map, pos=pos, ax=ax)

annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)
idx_to_node_dict = {}
for idx, node in enumerate(G.nodes):
    idx_to_node_dict[idx] = node

def update_annot(ind):
    node_idx = ind["ind"][0]
    node = idx_to_node_dict[node_idx]
    xy = pos[node]
    annot.xy = xy
    node_attr = {'node': node}
    node_attr.update(G.nodes[node])
    text = '\n'.join(f'{k}: {v}' for k, v in node_attr.items())
    annot.set_text(text)

def update_annot1(ind):
    edge = list(G.edges)[ind["ind"][0]]
    xy = (pos[edge[0]] + pos[edge[1]]) / 2
    annot.xy = xy
    node_attr = {'edge': edge}
    node_attr.update(G.edges[edge])
    text1 = '\n'.join(f'{k}: {v}' for k, v in node_attr.items())
    annot.set_text(text1)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = nodes.contains(event)
        cont1, ind1 = edges.contains(event)
        if cont or cont1:
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            if cont1:
                update_annot1(ind1)
                annot.set_visible(True)
                fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()