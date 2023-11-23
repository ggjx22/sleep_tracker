import streamlit as st

def title(text):
    # display title
    colT1,colT2 = st.columns([1,5])
    with colT2:
        st.title(text)
        
def markdown(text):
    # display markdown
    st.markdown(text)
    
def text(text):
    # display text
    st.text(text)