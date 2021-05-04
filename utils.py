import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import dill
from pyvis import network as net
import pandas as pd

def get_mouseover_dict(dataset):
    id_title_abstract = "<b>Paper id</b>: " + dataset["id"].astype(str) + " ("  + dataset["Conference"] + ") " " - "\
    "<a href=\""  + dataset["Link"] + "\" target=\"_blank\">Link</a>" + \
    "; <br><b>Authors: </b>: " + dataset["AuthorNames"] + \
    "; <br><b>Title</b>: " + dataset["Title"] + \
    "; <br><b>Abstract</b>: " + dataset["Abstract"]

    map_id_to_title={k: v for  k,v in zip(dataset.index, id_title_abstract)}
    return map_id_to_title


def get_node_color(node, df, color_dict):
    conference = df[df["id"] == node["id"]].Conference.values[0]
    return color_dict[conference]


def find_paper_title(title, model_name, dataset, color_dict,
                     path="html_files",
                     new_path="html_files/tmp/"):

    found = True
    with open("models/" + model_name + ".pkl", 'rb') as f:
        g = dill.load(f)

    count = 0

    looking_node = None
    neighbors = None
    for node in g.nodes:
        if str(title.strip().lower()) in str(node.get("title").lower()): 
            neighbors = g.neighbors(node["id"])
            looking_node = node
            break

 

    if neighbors:
        subnetwork_ids = list(neighbors) + [looking_node["id"]]
        subnetwork_edges = list()

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


        dataset_sub  = dataset[dataset["id"].isin(subnetwork_ids)]
        dataset_sub.to_csv("sub_network_data/sub_data.csv", index=False)
        
        map_id_to_title = get_mouseover_dict(dataset_sub)


        for node in g_sub.nodes:
            if node["id"] == looking_node["id"]:
                node.update({"size": "35"})
            node.update({"color": get_node_color(node, dataset_sub, color_dict)})
            node.update({"title": map_id_to_title.get(node["id"])})



        g_sub.show("html_files/small/sub_network.html")

       

    else:
        found = False
        for node in g.nodes:
            node.update({"color": "gray"})




                

    # for node in g.nodes:
    #     if str(title.lower()) not in str(node.get("title").lower()):
    #         node.update({"color": "gray"})
    #     else:
    #         node.update({"size": "60"})



    g.show(new_path + model_name + ".html")

    return found


