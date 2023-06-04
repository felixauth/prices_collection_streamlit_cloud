import streamlit as st
from html_collection import prices_collection
from main import launch_html_collection
from params import params
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import date

"""
## Collecte de données via web scraping - RAJA

[![Source](https://img.shields.io/badge/View-Source-<COLOR>.svg)]

"""


# Selecting the websites and brands to scrap
websites = st.multiselect(
    label='Sélectionner les sites souhaités :',
    options = ['manutan', 'jpg','bernard','raja','bruneau'],
    default=['manutan', 'jpg','bernard','raja','bruneau'])

marques = st.multiselect(
    label='Sélectionner les marques souhaitées :',
    options = ['TORK', 'JEX','ST MARC','HARPIC', 'AJAX','ROSSIGNOL','ANSELL','BLAKLADER'],
    default=['TORK', 'JEX','ST MARC','HARPIC', 'AJAX','ROSSIGNOL','ANSELL','BLAKLADER'])

launch_button = st.button("Lancer l'extraction des données")

if launch_button:

    
    # Importing params
    input_df = params()

    # Connecting the Chrome driver
    @st.experimental_singleton
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    options = Options()
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    options.add_argument("--disable-blink-features=AutomationControlled") 

    driver = get_driver()

    # Lauching the collection of data
    soup_df = launch_html_collection(websites,marques,input_df)
    collect_df = prices_collection(soup_df, input_df)

    # Displaying the collected data
    st.write(collect_df)



