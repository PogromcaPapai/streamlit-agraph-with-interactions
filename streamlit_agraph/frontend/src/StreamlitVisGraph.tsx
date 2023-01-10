import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import VisGraph from 'react-vis-graph-wrapper';


class StreamlitVisGraph extends StreamlitComponentBase {

  public render = (): ReactNode => {

    function lookup_node_id(lookup_node, mynodes){
      for (let node of mynodes){
          if (node.id === lookup_node){
              return node;
          }
    }}

    var graph = JSON.parse(this.props.args["data"]);
    
    var nodes = graph.nodes.slice();

    for (let i = 0; i < nodes.length; i++) {
      if(nodes[i].title)
        nodes[i].div = this.htmlTitle(nodes[i].title);
    }
  
    const options = JSON.parse(this.props.args["config"]);

    function handleEvent(event:any, type:string) {
      if (event.event !== undefined) event.event = undefined;
      Streamlit.setComponentValue({
        type: type,
        event: event,
        is_event: true
      });
    }

    const events = {
      // click: (ev) => {handleEvent(ev, "click")},
      // doubleClick: (ev) => {handleEvent(ev, "doubleClick")},
      // oncontext: (ev) => {handleEvent(ev, "oncontext")},
      // dragStart: (ev) => {handleEvent(ev, "dragStart")},
      // dragging: (ev) => {handleEvent(ev, "dragging")},
      // dragEnd: (ev) => {handleEvent(ev, "dragEnd")},
      // controlNodeDragging: (ev) => {handleEvent(ev, "controlNodeDragging")},
      // controlNodeDragEnd: (ev) => {handleEvent(ev, "controlNodeDragEnd")},
      // zoom: (ev) => {handleEvent(ev, "zoom")},
      // showPopup: (ev) => {handleEvent(ev, "showPopup")},
      // hidePopup: (ev) => {handleEvent(ev, "hidePopup")},
      // select: (ev) => {handleEvent(ev, "select")},
      selectNode: (ev) => {handleEvent(ev, "selectNode")},
      selectEdge: (ev) => {handleEvent(ev, "selectEdge")},
      // deselectNode: (ev) => {handleEvent(ev, "deselectNode")},
      // deselectEdge: (ev) => {handleEvent(ev, "deselectEdge")},
      // hoverNode: (ev) => {handleEvent(ev, "hoverNode")},
      // hoverEdge: (ev) => {handleEvent(ev, "hoverEdge")},
      // blurNode: (ev) => {handleEvent(ev, "blurNode")},
      // blurEdge: (ev) => {handleEvent(ev, "blurEdge")},
    };
    return (
      <span>
    
      <VisGraph
      graph={graph}
      options={options}
      events={events}
      getNetwork={(network: any) => {
        //  if you want access to vis.js network api you can set the state in a parent component using this property
        //console.log(network);
      }}/>
      </span>
    )
  }

  private htmlTitle = (html):any => {   
    const container = document.createElement("div");
    container.innerHTML = html;
    return container;
  }
}

export default withStreamlitConnection(StreamlitVisGraph)
