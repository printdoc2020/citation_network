import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import dill
from pyvis import network as net
import pandas as pd

def find_paper_title(title, model_name, physics, dataset,
                     path="html_files",
                     new_path="html_files/tmp/"):
    with open("models/" + model_name + ".pkl", 'rb') as f:
        g = dill.load(f)

    if physics:
        pass #g.show_buttons(filter_=["physics", "edges"])

    count = 0

    looking_node = None
    neighbors = None
    for node in g.nodes:
        if str(title.lower()) in str(node.get("title").lower()): 
            neighbors = g.neighbors(node["id"])
            looking_node = node
            break

    subnetwork_ids = list(neighbors) + [looking_node["id"]]
    subnetwork_edges = list()

    if neighbors:
        for node in g.nodes:
            if node["id"] == looking_node["id"]:
                node.update({"size": "60"})
            elif node["id"] in neighbors:
                pass
            else:
                node.update({"color": "gray"})


        for edge in g.edges:
            if edge['from'] in subnetwork_ids and edge["to"] in subnetwork_ids:
                subnetwork_edges.append(edge)
        g_sub = net.Network(height="500px", width="100%",heading='Sub Network')
        g_sub.set_template("html_files/template_2.html")
        g_sub.add_nodes(subnetwork_ids)
        g_sub.add_edges([ [e['from'], e["to"], e["width"]] for e in subnetwork_edges]) 


        for node in g_sub.nodes:
            if node["id"] == looking_node["id"]:
                node.update({"color": "red"})


        g_sub.show("html_files/small/sub_network.html")

        dataset_sub  = dataset[dataset["id"].isin(subnetwork_ids)]
        dataset_sub.to_csv("sub_network_data/sub_data.csv", index=False)



    else:
        for node in g.nodes:
            node.update({"color": "gray"})




                

    # for node in g.nodes:
    #     if str(title.lower()) not in str(node.get("title").lower()):
    #         node.update({"color": "gray"})
    #     else:
    #         node.update({"size": "60"})



    g.show(new_path + model_name + ".html")

    return


