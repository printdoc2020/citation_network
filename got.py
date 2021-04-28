import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import dill

def find_paper_title(title, model_name,
                     path="html_files",
                     new_path="html_files/tmp/"):
    with open("models/" + model_name + ".pkl", 'rb') as f:
        g = dill.load(f)

    count = 0

    looking_node = None
    neighbors = None
    for node in g.nodes:
        if str(title.lower()) in str(node.get("title").lower()): 
            neighbors = g.neighbors(node["id"])
            looking_node = node
            break

    if neighbors:
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

                

    # for node in g.nodes:
    #     if str(title.lower()) not in str(node.get("title").lower()):
    #         node.update({"color": "gray"})
    #     else:
    #         node.update({"size": "60"})



    g.show(new_path + model_name + ".html")

    return


