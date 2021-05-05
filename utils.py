import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import dill
from pyvis import network as net
import pandas as pd
from os.path import join as os_join




def get_authors_from_node_id( dataset, node_id):
    author_info = dataset[dataset["id"] == node_id].AuthorNames.values[0]
    authors = str(author_info).split(";")
    return set(authors)

def get_mutual_authors(node_id_1, node_id_2, dataset):
    authors_1 = get_authors_from_node_id(dataset, node_id_1)
    authors_2 = get_authors_from_node_id(dataset, node_id_2)
    
    mutual_authors = set.intersection( authors_1, authors_2 )
    return mutual_authors
    


def get_mouseover_dict(dataset):
    id_title_abstract = "<b>Paper id</b>: " + dataset["id"].astype(str) + " ("  + dataset["Conference"] + ") " " - "\
    "<a href=\""  + dataset["Link"] + "\" target=\"_blank\">Link</a>" + \
    "<br><b>Authors: </b>: " + dataset["AuthorNames"] + \
    "<br><b>Title</b>: " + dataset["Title"] + \
    "<br><b>Abstract</b>: " + dataset["Abstract"]

    map_id_to_title={k: v for  k,v in zip(dataset.index, id_title_abstract)}
    return map_id_to_title


def get_node_id_color(node_id, df, color_dict):

    conference = df[df["id"] == int(node_id)].Conference.values[0]
    return color_dict[conference]

def get_node_color(node, df, color_dict):
    node_id = int(str(node["id"]).split("_")[-1])
    conference = df[df["id"] == node_id].Conference.values[0]
    return color_dict[conference]


def update_original_network(title, model_name, after_searching_path):

    with open("models/" + model_name + ".pkl", 'rb') as f:
        g = dill.load(f)

    looking_node = None
    neighbors = None

    for node in g.nodes:
        if str(title.strip().lower()) in str(node.get("title").lower()): 
            neighbors = g.neighbors(node["id"])
            looking_node = node
            break

    if neighbors:
        ## update the original network after filterring
        for node in g.nodes:
            if node["id"] == looking_node["id"]:
                node.update({"size": "60"})
            elif node["id"] in neighbors:
                pass
            else:
                node.update({"color": "gray"})
    else:
        for node in g.nodes:
            node.update({"color": "gray"})

    g.show(os_join(after_searching_path, model_name + ".html"))

    return neighbors, looking_node




def write_sub_network(model_name, dataset, neighbors, looking_node, small_network_path, color_dict, edge_colors):
    subnetwork_ids = list(neighbors) + [looking_node["id"]]
    subnetwork_edges = list()

    with open("models/" + model_name + ".pkl", 'rb') as f:
        g = dill.load(f)
    
    dataset_sub  = dataset[dataset["id"].isin(subnetwork_ids)]
    dataset_sub.to_csv(f"sub_network_data/{model_name}_sub_data.csv", index=False)
    
    for edge in g.edges:
        if edge['from'] in subnetwork_ids and edge["to"] in subnetwork_ids:

            mutual_authors = get_mutual_authors(edge['from'], edge["to"], dataset_sub)

            if len(mutual_authors) > 0:
                color = edge_colors["mutual_authors"]
            else:
                color = edge_colors["different_authors"]

            edge_tmp = {"title": ";".join(author for author in mutual_authors), "color": color,  "width": edge['width'], "from": edge['from'], "to":  edge['to']}
            subnetwork_edges.append( edge_tmp )


    g_sub = net.Network(height="500px", width="100%",heading=f'Sub Network - {model_name}')
    g_sub.set_template("html_files/template_2.html")
    g_sub.add_nodes(subnetwork_ids)

    for e in subnetwork_edges:
        g_sub.add_edge(e['from'], e['to'], color=e['color'], width=e['width']/2, title=e["title"])

    g_sub.set_edge_smooth('dynamic')

  
    map_id_to_title = get_mouseover_dict(dataset_sub)

    for node in g_sub.nodes:
        if node["id"] == looking_node["id"]:
            node.update({"size": "32"})
        node.update({"color": get_node_color(node, dataset_sub, color_dict)})
        node.update({"title": map_id_to_title.get(node["id"])})

    g_sub.show( os_join(small_network_path, f"{model_name}_sub_network.html"))




def write_shared_sub_networks(model_name_1, model_name_2, dataset, neighbors_1, neighbors_2, looking_node, small_network_path, color_dict, edge_colors):

    if neighbors_1:
        subnetwork_ids_1 = list(neighbors_1) + [looking_node["id"]]
    else:
        subnetwork_ids_1= []

    if neighbors_2:
        subnetwork_ids_2 = list(neighbors_2) + [looking_node["id"]]
    else:
        subnetwork_ids_2= []



    subnetwork_ids = set.union(set(subnetwork_ids_1), set(subnetwork_ids_2))
    dataset_sub  = dataset[dataset["id"].isin(subnetwork_ids)]
    dataset_sub.to_csv(f"sub_network_data/shared_sub_data.csv", index=False)

    subnetwork_edges = list()

    model_1_prefix = "doc_"
    model_2_prefix = "ref_"

    with open("models/" + model_name_1 + ".pkl", 'rb') as f:
        g_1 = dill.load(f)

    with open("models/" + model_name_2 + ".pkl", 'rb') as f:
        g_2 = dill.load(f)

    for edge in g_1.edges:
        if edge['from'] in subnetwork_ids_1 and edge["to"] in subnetwork_ids_1:
            mutual_authors = get_mutual_authors(edge['from'], edge["to"], dataset_sub)

            if len(mutual_authors) > 0:
                color = edge_colors["mutual_authors"]
            else:
                color = edge_colors["different_authors"]

            edge_tmp = {"title": ";".join(author for author in mutual_authors), "color": color,  "width": edge['width'], "from": model_1_prefix + str(edge['from']), "to":  model_1_prefix + str(edge['to'])}
            subnetwork_edges.append( edge_tmp )



    for edge in g_2.edges:
        if edge['from'] in subnetwork_ids_2 and edge["to"] in subnetwork_ids_2:

            mutual_authors = get_mutual_authors(edge['from'], edge["to"], dataset_sub)

            if len(mutual_authors) > 0:
                color = edge_colors["mutual_authors"]
            else:
                color = edge_colors["different_authors"]

            edge_tmp = {"title": ";".join(author for author in mutual_authors), "color":color, "width": edge['width'], "from": model_2_prefix + str(edge['from']), "to":  model_2_prefix + str(edge['to'])}
            subnetwork_edges.append( edge_tmp )

    g_sub = net.Network(height="700px", width="100%",heading=f'Sub Networks')
    g_sub.set_template("html_files/template_2.html")


    subnetwork_ids_1_add_prefix = [model_1_prefix + str(n) for n in subnetwork_ids_1]
    subnetwork_ids_2_add_prefix = [model_2_prefix + str(n) for n in subnetwork_ids_2]

    node_list = set.union(set(subnetwork_ids_1_add_prefix), set(subnetwork_ids_2_add_prefix))
    map_id_to_title = get_mouseover_dict(dataset_sub)

    for node_id_raw in node_list:
        node_id = str(node_id_raw).split("_")[-1]
        title =  map_id_to_title.get(int(node_id))

        if str(node_id) == str(looking_node["id"]): 
            g_sub.add_node( node_id_raw, size=32, title=title , color= get_node_id_color(node_id, dataset_sub, color_dict))

        else:
            g_sub.add_node( node_id_raw, title=title, color= get_node_id_color(node_id, dataset_sub, color_dict))

    # g_sub.add_edges([ [e['from'], e["to"], e["width"]] for e in subnetwork_edges]) 
    for e in subnetwork_edges:
        g_sub.add_edge(e['from'], e['to'], title=e["title"], color=e['color'], width=e['width']/2)
    g_sub.set_edge_smooth('dynamic')

   
    

    g_sub.show( os_join(small_network_path, "shared_sub_networks.html"))





def find_paper_title_for_1_model(neighbors_dict, looking_node_dict, model_name, dataset, color_dict, small_network_path, after_searching_path, edge_colors):

    found = None
    
    neighbors, looking_node = neighbors_dict[model_name], looking_node_dict[model_name]
    if neighbors:
        found = True
        write_sub_network(model_name, dataset, neighbors, looking_node, small_network_path, color_dict, edge_colors)
    else:
        found = False

    return {"model_name": model_name, "found":found}



def find_paper_title_all_models_separately(neighbors_dict, looking_node_dict, dataset, color_dict, small_network_path,
                    after_searching_path, edge_colors):
    
    found_citation = find_paper_title_for_1_model(neighbors_dict, looking_node_dict,"reference_similarity", dataset, color_dict, small_network_path, after_searching_path,edge_colors)
    found_doc2vec = find_paper_title_for_1_model(neighbors_dict, looking_node_dict,"doc2vec_similarity", dataset, color_dict, small_network_path, after_searching_path, edge_colors)
    return [found_citation, found_doc2vec]


def find_paper_title_all_models_shared_subnetworks(neighbors_dict, looking_node_dict, dataset, color_dict, small_network_path,
                    after_searching_path, edge_colors):
    
    model_name_1 = "doc2vec_similarity"
    model_name_2 = "reference_similarity"
    neighbors_1, looking_node_1 = neighbors_dict[model_name_1], looking_node_dict[model_name_1]
    neighbors_2, looking_node_2 = neighbors_dict[model_name_2], looking_node_dict[model_name_2]

    looking_node = looking_node_1 if looking_node_1 else looking_node_2

    if looking_node:
        found=True
        write_shared_sub_networks(model_name_1, model_name_2, dataset, neighbors_1, neighbors_2, looking_node, small_network_path, color_dict, edge_colors)

    else:
        found=False
    return found

