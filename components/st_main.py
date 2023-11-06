import streamlit as st
from components.converter import pydantic_model_to_bnf
from components.utils import create_pydantic_model_from_string


def st_main():
    input_ = st.text_area('Your Pydatic Class')
    submitted = st.button('submit')
    if submitted: 
        st.code(input_)
        pydantic_class = create_pydantic_model_from_string(input_)
        bnf = pydantic_model_to_bnf(pydantic_class)
        st.code(
            bnf.replace('\n','  \n')
        )
