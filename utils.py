import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import dill
from pyvis import network as net
import pandas as pd
from os.path import join as os_join

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

def find_paper_title(title, dataset, color_dict, small_network_path,
                    after_searching_path):
    
    found_citation = find_paper_title_for_1_model(title, "reference_similarity", dataset, color_dict, small_network_path, after_searching_path)
    found_doc2vec = find_paper_title_for_1_model(title, "doc2vec_similarity", dataset, color_dict, small_network_path, after_searching_path)
    return [found_citation, found_doc2vec]

def find_paper_title_for_1_model(title, model_name, dataset, color_dict, small_network_path, after_searching_path):

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
        g_sub = net.Network(height="500px", width="100%",heading=f'Sub Network - {model_name}')
        g_sub.set_template("html_files/template_2.html")
        g_sub.add_nodes(subnetwork_ids)
        g_sub.add_edges([ [e['from'], e["to"], e["width"]] for e in subnetwork_edges]) 

        g_sub.set_edge_smooth('dynamic')


        dataset_sub  = dataset[dataset["id"].isin(subnetwork_ids)]
        dataset_sub.to_csv(f"sub_network_data/{model_name}_sub_data.csv", index=False)
        
        map_id_to_title = get_mouseover_dict(dataset_sub)


        for node in g_sub.nodes:
            if node["id"] == looking_node["id"]:
                node.update({"size": "35"})
            node.update({"color": get_node_color(node, dataset_sub, color_dict)})
            node.update({"title": map_id_to_title.get(node["id"])})



        g_sub.show( os_join(small_network_path, f"{model_name}_sub_network.html"))

       

    else:
        found = False
        for node in g.nodes:
            node.update({"color": "gray"})


    g.show(os_join(after_searching_path, model_name + ".html"))

    return {"model_name": model_name, "found":found}


