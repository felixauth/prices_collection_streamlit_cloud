import streamlit as st
from html_collection import html_collection, prices_collection
from params import params
import pandas as pd
from tqdm import tqdm

"""
## Web scraping on Streamlit Cloud with Selenium

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)](https://github.com/snehankekre/streamlit-selenium-chrome/)

This is a minimal, reproducible example of how to scrape the web with Selenium and Chrome on Streamlit's Community Cloud.

Fork this repo, and edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:
"""

with st.echo():
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    @st.experimental_singleton
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled") 

    driver = get_driver()
    
    soup_df = pd.DataFrame()
    input_df = params()

    soup_df = html_collection("manutan", "TORK", input_df, soup_df, driver)
#     driver.get("https://www.bernard.fr/")

    st.write(soup_df)
