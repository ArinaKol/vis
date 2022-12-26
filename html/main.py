import networkx as nx
import json
from networkx.readwrite import json_graph
from pyvis.network import Network
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import csv

from bokeh.plotting import figure, from_networkx, show
from bokeh.io import output_file, show
from bokeh.models import (BoxSelectTool, Circle, EdgesAndLinkedNodes, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool)
from bokeh.models import (BoxZoomTool, Circle, HoverTool,
                          MultiLine, Plot, Range1d, ResetTool)
from bokeh.palettes import Spectral4
from bokeh.plotting import from_networkx
from bokeh.io import output_file, show
from bokeh.models import CustomJSTransform, LabelSet
from bokeh.transform import transform


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



###
G = nx.Graph()
with open('RDGCN_EN_RU_15K_V1_xlnet.csv', encoding="utf8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
       G.add_node(int(row['ent1_id']), id=int(row['ent1_id']), id2=int(row['ent2_id']), pos=(float(row['x']), float(row['y'])), color = 'darkblue' if row['lang'] == 'en' else 'crimson', lang=row['lang'], title=row['ent1'] if row['lang'] == 'en' else row['ent2'], type=row['type'], x=(float(row['x'])), y=float(row['y']))
pos=nx.get_node_attributes(G, 'pos')


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



# Form screens
HOVER_TOOLTIPS = [("id", "@id"), ("title", "@title"), ("type", "@type"), ("lang", "@lang"), ("x,y", "@pos")]
plot = figure(height=720, width=1580, tooltips = HOVER_TOOLTIPS, tools="pan,wheel_zoom,tap,save,reset", active_scroll='wheel_zoom', x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))

plot.add_tools(TapTool(), BoxSelectTool())


network_graph = from_networkx(G, pos)
network_graph.node_renderer.selection_glyph = Circle(size=15, fill_color='color')
network_graph.node_renderer.glyph = Circle(size=15, fill_color='color', line_alpha=0.2)


network_graph.edge_renderer.glyph = MultiLine(line_color="#dbdbdb", line_alpha=0.8, line_width=5)
network_graph.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=5)
network_graph.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=5)

network_graph.selection_policy = NodesAndLinkedEdges()
network_graph.inspection_policy = NodesAndLinkedEdges()

plot.renderers.append(network_graph)

source = network_graph.edge_renderer.data_source

source.data['names'] = ["%d-%d" % (x, y) for (x,y) in zip(source.data['start'], source.data['end'])]

# create a transform that can extract and average the actual x,y positions
code = """
    const result = new Float64Array(xs.length)
    const coords = provider.get_edge_coordinates(source)[%s]
    for (let i = 0; i < xs.length; i++) {
        result[i] = (coords[i][0] + coords[i][1])/2
    }
    return result
"""
xcoord = CustomJSTransform(v_func=code % "0", args=dict(provider=network_graph.layout_provider, source=source))
ycoord = CustomJSTransform(v_func=code % "1", args=dict(provider=network_graph.layout_provider, source=source))

# Use the transforms to supply coords to a LabelSet
labels = LabelSet(x=transform('start', xcoord),
                  y=transform('start', ycoord),
                  text='rel', text_font_size="10px",
                  x_offset=5, y_offset=5,
                  source=source)

plot.add_layout(labels)

show(plot)