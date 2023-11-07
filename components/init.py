import streamlit as st

def init():
    st.set_page_config(
        page_title="Pydantic to BNF Grammar Converter",
        page_icon="🔀",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    
    # App Header
def app_header():
    st.title('Pydantic to BNF Grammar Converter')
    with st.expander('Welcome!'):
        st.markdown(
            "Welcome to the BNF Converter!   \n\n"
            "Use this tool to convert your `Pydantic class definitions` into `BNF grammar`:  \n"
            "- Select a test case from the dropdown  \n"
            "- Or enter your own Pydantic class in the text area below."
        )


