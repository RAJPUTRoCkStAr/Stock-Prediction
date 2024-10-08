import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
from lotti import lottie_company
def company():
    st.header("List of Companies and Industry Exploration",divider='rainbow')
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("Welcome to the Company Exploration App! Select the column from your existing dataset that contains company names or related information. From there, choose an industry from the dropdown menu to view companies associated with that industry. You'll be able to explore additional details such as symbols or other relevant information for each company. Whether you're conducting market research, analyzing industry trends, or seeking investment opportunities, this app provides a convenient way to delve into the world of companies within your dataset. Start exploring now and uncover valuable insights!")
    with col2:
        lottie_company
        st_lottie(lottie_company, speed=1, reverse=True, loop=True, quality='medium', height=150, width=None, key=None)
    st.subheader("Explore Companies by Industry")
    df = pd.read_csv("fdata.csv", encoding='latin-1')
    selected_industry = st.selectbox("Select an industry", df['Industry'].unique(), index=0,label_visibility="hidden")
    if selected_industry:
        selected_data = df[df['Industry'] == selected_industry][['Company Name', 'Symbol', 'Market Cap']]
        st.markdown(f"<h2 style='text-align: center;color:#ff4b4b;'>Companies related to <mark style='background-color: blue;color:#ff4b4b'>{selected_industry}</mark> industry are 👇:</h2>", unsafe_allow_html=True)
        st.dataframe(selected_data,hide_index=True,use_container_width=True,height=1200)
