import streamlit as st
from html_collection import prices_collection, html_collection
from params import params
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import date
from tqdm import tqdm

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
    @st.cache_resource
    def get_driver():
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Setting the options for Chrome driver
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless=new')
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    options.add_argument('--ignore-certificate-errors-spki-list')

    # Adding argument to disable the AutomationControlled flag 
    options.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    options.add_experimental_option("useAutomationExtension", False) 

    driver = get_driver()

    # Lauching the collection of data
    # driver.implicitly_wait(10)

    soup_df = pd.DataFrame()

    # for website in tqdm(websites):
    #     print("\n", f"---------------------- Extracting data from {website.upper()} -------------------------", "\n")
    #     for marque in marques :
    #         soup_df = html_collection(website, marque, input_df, soup_df, driver)
    #         print("\n", f"------{marque} information collected", "\n")

    # print("\n", "Data collection complete.")

    soup_df = html_collection("raja", 'jex', input_df, soup_df, driver)
    
    st.write(soup_df)

    collect_df = prices_collection(soup_df, input_df)

    # Displaying the collected data
    st.write(collect_df)



