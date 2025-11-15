import streamlit as st
from PIL import Image
icon=Image.open('assets/icons/icon_process.png')
st.image(icon,width=48)
st.markdown('<h1>Structure Level</h1>', unsafe_allow_html=True)
st.write('Conteúdo...')