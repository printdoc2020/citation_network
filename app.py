import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import utils
import pandas as pd

st.set_page_config(
	 page_title="Citation Networks",
	 page_icon="random",
	 layout="wide",
	 initial_sidebar_state="expanded",
 )


height, width = 500, 1400
height_shared_subnetworks = 700
display_cols = ['id', 'Conference', 'Year', 'Title', 'DOI', 'PaperType',
       'Abstract', 'AuthorNames']

# full_cols = ['Conference', 'Year', 'Title', 'DOI', 'id', 'cite_to_list',
#        'cited_by_list', 'Link', 'FirstPage', 'LastPage', 'PaperType',
#        'Abstract', 'AuthorNames-Deduped', 'AuthorNames', 'AuthorAffiliation',
#        'InternalReferences', 'AuthorKeywords', 'AminerCitationCount_02-2020',
#        'XploreCitationCount - 2020-01', 'PubsCited', 'Award']

title = st.text_input('Search Paper Title', "")

if title:
	st.markdown(f'...Looking for paper: **{title}**')
else: 
	st.markdown("Enter a paper title here, for example:")
	st.markdown("**_Connecting the dots in visual analysis_**")
	st.markdown("**_ActiVis: Visual Exploration of Industry-Scale Deep Neural Network Models_**" )
	st.markdown("**_Streamline Variability Plots for Characterizing the Uncertainty in Vector Field Ensembles_**" )


after_searching_path = "html_files/search/"
small_network_path = "html_files/small/"

dataset_path = "vis_data.csv"


color_dict = {
	"InfoVis": "blue",
	"VAST": "orange",
	"SciVis": "red"
}

edge_colors= {
    "mutual_authors": "green",
    "different_authors": "gray"
}

st.text("Legends: " + str(color_dict))



dataset = pd.read_csv(dataset_path)



if title=="":
	HtmlFile = open("html_files/reference_similarity.html", 'r', encoding='utf-8')
	source_code = HtmlFile.read()
	components.html(source_code, height = height,width=width)


	HtmlFile = open("html_files/doc2vec_similarity.html", 'r', encoding='utf-8')
	source_code = HtmlFile.read()
	components.html(source_code, height = height,width=width)
else:
	model_name_list = ["reference_similarity", "doc2vec_similarity"]

	neighbors_dict = dict()
	looking_node_dict  = dict()

	for model_name in model_name_list:
		neighbors, looking_node = utils.update_original_network(title, model_name, after_searching_path)
		HtmlFile = open(after_searching_path+ model_name +".html", 'r', encoding='utf-8')
		source_code = HtmlFile.read()
		components.html(source_code, height = height,width=width)

		neighbors_dict[model_name] = neighbors
		looking_node_dict[model_name] = looking_node

	separate_sub_networks = st.checkbox("Separate Sub Networks")
	st.text("Legends: " + str(edge_colors))


	if separate_sub_networks:
		found_list = utils.find_paper_title_all_models_separately(neighbors_dict, looking_node_dict, dataset, color_dict, small_network_path, after_searching_path, edge_colors)
		for found_obj in found_list:
			if found_obj["found"]:
				HtmlFile = open(small_network_path + f"{found_obj['model_name']}_sub_network.html", 'r', encoding='utf-8')
				source_code = HtmlFile.read()
				components.html(source_code, height = height,width=width)

				sub_data = pd.read_csv("sub_network_data/" + f"{found_obj['model_name']}_sub_data.csv")
				st.dataframe(sub_data[display_cols]) 
	else:
		found = utils.find_paper_title_all_models_shared_subnetworks(neighbors_dict, looking_node_dict, dataset, color_dict, small_network_path,
               after_searching_path, edge_colors)
		if found:
			HtmlFile = open(small_network_path + "shared_sub_networks.html", 'r', encoding='utf-8')
			source_code = HtmlFile.read()
			components.html(source_code, height = height_shared_subnetworks,width=width)

			sub_data = pd.read_csv("sub_network_data/" + f"shared_sub_data.csv")
			st.dataframe(sub_data[display_cols]) 

		