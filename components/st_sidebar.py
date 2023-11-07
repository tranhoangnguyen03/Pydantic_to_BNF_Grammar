import streamlit as st

def st_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.markdown("## About The App")
        st.markdown("""
        This app is brought to you by an enthusiast of open-source generative models, inspired by the great work at https://grammar.intrinsiclabs.ai/.
                    
        Whereas OpenAI's GPT models are well-tuned for function calling, open-source models need guidance in order to produce good results. One such guidance is BNF grammar which lets the LLM know your expectation of its json outputs.        
                    
        Should you have any queries or suggestions, feel free to raise an issue on the project [GitHub repository](https://github.com/tranhoangnguyen03/Pydantic_to_BNF_Grammar) or send me an [email](tranhoangnguyen03@gmail.com).
        
        Thank you and have fun!
        """)
