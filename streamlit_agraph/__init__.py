from functools import cache
import os
import csv
import json

from operator import itemgetter
from typing import Any, Callable, NewType
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

Event = NewType("Event", dict[str, Any])
class Graph(object):
    
    @st.cache
    @staticmethod
    def _get_context(nodes, edges, config):
        nodes_data = [ node.to_dict() for node in nodes]
        edges_data = [ edge.to_dict() for edge in edges]
        config_json = json.dumps(config.__dict__)
        data = { "nodes": nodes_data, "edges": edges_data}
        data_json = json.dumps(data)
        return {"data":data_json, "config":config_json}
    
    def __new__(cls, nodes, edges, config):
        component_value = _agraph(**cls._get_context(nodes, edges, config))
        if component_value is not None and component_value.get('is_event', False):
            new = super().__new__(cls)
            new.nodes = nodes
            new.edges = edges
            new.config = config
            new.type_ = component_value.get('type')
            new.event = component_value.get('event')
            return new
        else:
            component_value.on = lambda x, y: None
            return component_value
        
    def on(self, event_type: str, function: Callable[[Event, list[Node], list[Edge], Config], Any]) -> Any:
        if event_type != None and event_type == self.type_:
            return function(self.event, self.nodes, self.edges, self.config)

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
    graph = Graph(nodes, edges, config)
    graph.on('selectNode', 
            lambda _1,_2,_3,_4: st.write("it works")
        )
    
