import streamlit as st
from components.st_sidebar import st_sidebar
from components.st_main import st_main
from components.init import init, app_header


init()
app_header()
st_sidebar()
st_main()