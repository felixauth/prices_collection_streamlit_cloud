from html_collection import html_collection, prices_collection
from params import params, import_brands, import_output_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import sys
from utils import clean_path
from datetime import date
import os
from tqdm import tqdm


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


    s = Service('chromedriver.exe')
    chromeOptions = Options()

    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--blink-settings=imagesEnabled=false")

    chromeOptions.add_argument('--ignore-certificate-errors-spki-list')

    # Adding argument to disable the AutomationControlled flag 
    chromeOptions.add_argument("--disable-blink-features=AutomationControlled") 
    
    # Exclude the collection of enable-automation switches 
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    
    # Turn-off userAutomationExtension 
    chromeOptions.add_experimental_option("useAutomationExtension", False) 

    driver = webdriver.Chrome(service=s, options=chromeOptions)
    driver.implicitly_wait(10)

    soup_df = pd.DataFrame()

    for website in tqdm(websites):
        print("\n", f"---------------------- Extracting data from {website.upper()} -------------------------", "\n")
        for marque in marques :
            soup_df = html_collection(website, marque, input_df, soup_df, driver)
            print("\n", f"------{marque} information collected", "\n")

    print("\n", "Data collection complete.")

    return soup_df


def save_data(data, path):
    """
    Function that saves the output to a specific folder

    Parameters
    ----------
    data : dataframe to be saved
    path : path of the folder where to save the data

    Returns
    -------
    nothing

    """
    path = clean_path(path)

    data.to_excel(path,index=False)

    print("\n", "Extraction saved in the selected folder.")


if __name__ =="__main__":

    #Choice of websites
    websites = ["bruneau","manutan","jpg","raja","bernard"] #"manutan","bruneau","jpg","raja","bernard"

    #Choice of brands
    marques = import_brands()

    #Importing params
    input_df = params()

    #Launching html content collection for each website and brand
    soup_df = launch_html_collection(websites,marques,input_df)

    #Extracting products names, references and prices
    collect_df = prices_collection(soup_df, input_df)

    #Adding the date of the extraction
    today = date.today().strftime("%Y-%m-%d")
    collect_df.insert(0, 'Date_extraction', today)

    #Saving data to the repository chosen by the user
    file_path = import_output_path()
    file_name = f"{today}_Extract.xlsx"
    path = os.path.join(file_path,file_name) #Concatenating the path of the folder and the name of the file
    save_data(collect_df, path)

