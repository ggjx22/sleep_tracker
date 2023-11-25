import streamlit as st

def title(text):
    # display title
    st.title(text)

def title_algin(text, column_position):
    # display title
    colT1,colT2 = st.columns(column_position)
    with colT2:
        st.title(text)
        
def markdown(text):
    # display markdown
    st.markdown(text)
    
def text(text):
    # display text
    st.text(text)
    
def write(text):
    # display statement
    st.write(text)