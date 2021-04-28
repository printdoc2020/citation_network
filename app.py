import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import got
#Network(notebook=True)
st.title('Hello Pyvis')
# make Network show itself with repr_html

#def net_repr_html(self):
#  nodes, edges, height, width, options = self.get_network_data()
#  html = self.template.render(height=height, width=width, nodes=nodes, edges=edges, options=options)
#  return html

#Network._repr_html_ = net_repr_html

title = st.text_input('paper title', "")
st.write('Looking for Paper:', title)

new_path = "html_files/tmp/"

st.sidebar.title('Choose your Graph')
option=st.sidebar.selectbox('select graph',('citation_similarity','doc2vec_similarity'))
physics=st.sidebar.checkbox('add physics interactivity?')

if title=="":
    if option=='citation_similarity':
        HtmlFile = open("html_files/similarity_using_citeTo_and_citedBy.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 1200,width=1200)


    if option=='doc2vec_similarity':
        HtmlFile = open("html_files/similarity_Doc2Vec.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 1200,width=1200)
else:
    got.find_paper_title(title, option)
    HtmlFile = open(new_path+option+".html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 1200,width=1200)



