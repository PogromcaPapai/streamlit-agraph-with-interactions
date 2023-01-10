import os
import csv
import json

from operator import itemgetter
import streamlit.components.v1 as components
import streamlit as st

from streamlit_agraph import data
from streamlit_agraph.config import Config
from streamlit_agraph.triple import Triple
from streamlit_agraph.node import Node
from streamlit_agraph.edge import Edge
from streamlit_agraph.triplestore import TripleStore

_RELEASE = False

if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _agraph = components.declare_component("agraph", path=build_dir)
else:
    _agraph = components.declare_component(
        "agraph",
        url="http://localhost:3001",
    )

@st.cache
def get_context(nodes, edges, config):
    nodes_data = [ node.to_dict() for node in nodes]
    edges_data = [ edge.to_dict() for edge in edges]
    config_json = json.dumps(config.__dict__)
    data = { "nodes": nodes_data, "edges": edges_data}
    data_json = json.dumps(data)
    return {"data":data_json, "config":config_json}
 
def agraph(nodes, edges, config, **kwargs):
    ons = {i.removeprefix("on").lower():j for i,j in kwargs.items() if i.startswith("on")}
    
    component_value = _agraph(**get_context(nodes, edges, config))
    if component_value is not None and component_value.get('is_event'):
        return ons.get(component_value['type'].lower(), lambda x: None)(component_value['event'])
    return component_value

hierarchical = {
      "enabled":False,
      "levelSeparation": 150,
      "nodeSpacing": 100,
      "treeSpacing": 200,
      "blockShifting": True,
      "edgeMinimization": True,
      "parentCentralization": True,
      "direction": 'UD',        # UD, DU, LR, RL
      "sortMethod": 'hubsize',  # hubsize, directed
      "shakeTowards": 'leaves'  # roots, leaves
    }


if not _RELEASE:
    st.title("Streamlit Agraph 2.0")
    import networkx as nx
    G = nx.karate_club_graph()

    # Create the equivalent Node and Edge lists
    nodes = [Node(id=i, label=str(i)) for i in range(len(G.nodes))]
    edges = [Edge(source=i, target=j, type="CURVE_SMOOTH") for (i,j) in G.edges]
    config = Config(width=750, height=750) # layout={"hierarchical":True} directed=True #
    container = st.container()
    container.write("This is inside the container")
    return_value = agraph(nodes, edges, config=config, onSelectNode=lambda _: container.write('test'))
    # ^ i think the solution might be to replace this object with something that can be called
    # maybe a class with __eq__ for types?
    # st.write(return_value)
