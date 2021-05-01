import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import utils
import pandas as pd
st.title('Citation Networks')

title = st.text_input('Search Paper Title', "")

if title:
    st.markdown(f'...Looking for paper: **{title}**')
else: 
    st.markdown("Enter a paper title here, example: **_TenniVis: Visualization for Tennis Match Analysis_**" )

new_path = "html_files/tmp/"
sub_network_path = "html_files/small/"

dataset_path = "vis_data.csv"


st.sidebar.title('Choose your Graph')
option=st.sidebar.selectbox('select graph',('citation_similarity','doc2vec_similarity'))

color_dict = {
    "InfoVis": "blue",
    "VAST": "orange",
    "SciVis": "red"
}

st.text("Legends: " + str(color_dict))

dataset = pd.read_csv(dataset_path)



if title=="":
    if option=='citation_similarity':
        HtmlFile = open("html_files/similarity_using_citeTo_and_citedBy.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 1200,width=1200)


    if option=='doc2vec_similarity':
        HtmlFile = open("html_files/similarity_Doc2Vec.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 600,width=1200)
else:
    is_found = utils.find_paper_title(title, option, dataset)
    HtmlFile = open(new_path+option+".html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 600,width=1200)

    if is_found:
        HtmlFile = open(sub_network_path + "sub_network.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 500,width=1200)

        sub_data = pd.read_csv("sub_network_data/sub_data.csv")
        st.dataframe(sub_data) 


