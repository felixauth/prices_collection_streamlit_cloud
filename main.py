from html_collection import html_collection, prices_collection
from params import params
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import sys
from utils import clean_path
from datetime import date
import os
from tqdm import tqdm
from datetime import date



def launch_html_collection(websites, marques, input_df):

    """
    Function that loops over each website and brands and collect the html content at each iteration using Selenium for Google Chrome

    Parameters
    ----------
    websites : list of the website names
    marques : list of the brands
    input_df : dataframe from parameters

    Returns
    -------
    A dataframe with the name of the website, name of the brand and the html content
    
    """

    soup_df = pd.DataFrame()

    for website in tqdm(websites):
        print("\n", f"---------------------- Extracting data from {website.upper()} -------------------------", "\n")
        for marque in marques :
            soup_df = html_collection(website, marque, input_df, soup_df, driver)
            print("\n", f"------{marque} information collected", "\n")

    print("\n", "Data collection complete.")

    return soup_df

