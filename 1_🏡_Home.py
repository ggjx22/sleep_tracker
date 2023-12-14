import src.utils_styling as style
import streamlit as st

def main():
    st.set_page_config(
        page_title='Sleeping',
        page_icon='😴'
    )

    style.title('Welcome to the Sleep Tracker Web App.')
    style.text("It's a litte boring now. Stay tuned for more features!")

    # web app version
    style.text('Web app release version 1.3.2')
    
if __name__ == '__main__':
    main()