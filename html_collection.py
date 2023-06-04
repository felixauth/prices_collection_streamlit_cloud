from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from selenium.common.exceptions import NoSuchElementException
from utils import clean_prices
from datetime import date



def html_collection(website, marque, input_df, soup_df, driver):
    """
    Function that stores the html code for each website and each brand in a dataframe

    Parameters
    ----------
    website : list of the website names
    marque : list of the brands
    input_df : dataframe from parameters
    soup_df : dataframe storing the html content per website and brand
    driver : chrome driver

    Returns
    -------
    A dataframe with the name of the website, name of the brand and the html content
    
    """
    
    #Dealing with spaces in marque
    marque = marque.replace(" ","%20")

    #Manutan works with paging, while the other work with loadmore button, so we need to precise that we want the page 0
    if website == "manutan":
        marque = marque.replace("%20","-").lower()
        query=input_df.loc[input_df["website"]==website,"url"].values[0].format(marque_field = marque, max_product=0)
    elif website == "bruneau":
        query=input_df.loc[input_df["website"]==website,"url"].values[0].format(marque_field = marque, num_page=1)
    else:
        query=input_df.loc[input_df["website"]==website,"url"].values[0].format(marque_field = marque)

    #Opening web page
    driver.get(query)
    

    #Clicking on the accept cookies button if any
    try:
        driver.find_element(By.XPATH,input_df.loc[input_df["website"]==website,"xpath_cookies_accept"].values[0]).click()
    except NoSuchElementException:
        pass
    
    time.sleep(5)

    #Closing the promotion window for bruneau, if any
    if website == "bruneau":
        try:
            driver.find_element(By.XPATH,input_df.loc[input_df["website"]==website,"other"].values[0]).click()
        except:
            pass
    
    #Collecting the html code
    if website == "manutan":
        
        html_by_page = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        html_by_page.append(soup)
        match_html = re.search(r'sur(.*?)\)', soup.find("span",class_="num_products").text)
        print(match_html)
        if match_html:
            # match = re.search(r'sur\s+(\d+)', match_html.text)
            nb_products = int(match_html.group(1).replace('\xa0','').replace(' ',''))
            nb_pages = int(nb_products / 28) + 1
            print(nb_products)
            for nb_page in range(1,nb_pages):
                query = input_df.loc[input_df["website"]==website,"url"].values[0].format(marque_field = marque, max_product=nb_page * 28)    
                driver.get(query)
                driver.refresh()
                time.sleep(5)
                try:
                    driver.find_element(By.XPATH,input_df.loc[input_df["website"]==website,"xpath_cookies_accept"].values[0]).click()
                except:
                    pass
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                html_by_page.append(soup)

        marque = marque.replace("%20"," ")
        soup_df = pd.concat([soup_df, pd.DataFrame({"website": website,
                                                     "marque": marque,
                                                     "html_content": html_by_page},index=list(range(len(html_by_page))))]).reset_index(drop=True)

    elif website == "bruneau":
        
        html_by_page = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        html_by_page.append(soup)
        match_html = soup.find("h1",class_="isg-titre-camingo")
        if match_html:
            match = match_html.text
            nb_results = int(re.search(r'(\d+)\s+', match).group(0))
            n_resuls_by_page = 48
            if nb_results > n_resuls_by_page :
                nb_pages = int(nb_results / n_resuls_by_page) + 1
                for nb_page in range(2,nb_pages + 1):
                    query = input_df.loc[input_df["website"]==website,"url"].values[0].format(marque_field = marque, num_page=nb_page)    
                    driver.get(query)
                    
                    try:
                        driver.find_element(By.XPATH,input_df.loc[input_df["website"]==website,"xpath_cookies_accept"].values[0]).click()
                    except NoSuchElementException:
                        pass
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    html_by_page.append(soup)

        soup_df = pd.concat([soup_df, pd.DataFrame({"website": website,
                                                    "marque": marque,
                                                    "html_content": html_by_page},index=list(range(len(html_by_page))))]).reset_index(drop=True)
    else:
        e = True
        while e == True:
            try:
                loadMoreButton = driver.find_element(By.XPATH,input_df.loc[input_df["website"]==website,"xpath_load_more_button"].values[0])
                time.sleep(8)
                loadMoreButton.click()
                time.sleep(8)
                e = True
            except Exception:
                e = False
    
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        marque = marque.replace("%20"," ")
        soup_df = pd.concat([soup_df, pd.DataFrame({"website": website,
                                                        "marque": marque,
                                                        "html_content": soup},index=[0])]).reset_index(drop=True)
            
    return soup_df

def prices_collection(soup_df, input_df):

    """
    Function that extract information from html content

    Parameters
    ----------
    soup_df : dataframe with the name of the website, name of the brand and html content
    input_df : dataframe with html location of information wanted for each type of information and each website

    Returns
    -------
    A dataframe with the name of the website, name of the brand, the product name, the product reference and the product price
    
    """

    results_df = pd.DataFrame()

    for index, row in soup_df.iterrows():
            
            website = row["website"]
            marque = row["marque"]
            html_content = row["html_content"]

            # print(f"------------------extracting prices of {marque} from {website}---------------------")

            #Collecting products names
            results_names = html_content.find_all(input_df.loc[input_df["website"]==website,"class_name"].values[0][0],
                                                class_=input_df.loc[input_df["website"]==website,"class_name"].values[0][1])

            if website == "manutan":
                product_names = []
                for item in results_names:
                    try:
                        product_names.append(item["aria-label"])
                    except KeyError:
                        pass
            else:
                product_names = [product.text for product in results_names]

            #Collecting products references
            results_ref = html_content.find_all(input_df.loc[input_df["website"]==website,"class_ref"].values[0][0],
                                                class_=input_df.loc[input_df["website"]==website,"class_ref"].values[0][1])
            
            if website == "manutan":
                product_ref = [item["id"].lstrip("product_name_") for item in results_ref]
            elif website == "bruneau":
                product_ref = [product["id"].strip("product-") for product in results_ref]
            else:
                product_ref = [product.text for product in results_ref]

            #Collecting products prices
            results_prices = html_content.find_all(input_df.loc[input_df["website"]==website,"class_price"].values[0][0],
                                                class_=input_df.loc[input_df["website"]==website,"class_price"].values[0][1])
            
            if website == "bruneau":
                results_prices = [results_prices[i] for i in range(0,len(results_prices),2)]

            product_prices = [price.text for price in results_prices]

            #Collecting and storing data into a dataframe, if data found
            if (len(product_names)!=len(product_ref)) or (len(product_names)!=len(product_prices)) or (len(product_ref)!=len(product_prices)):
                pass

            else:

                # Getting current date  
                today = date.today().strftime("%Y-%m-%d")

                # Generating df with collected data
                results_marque_df = pd.DataFrame({
                                    "Date_extraction": today,
                                    "Site": website,
                                    "Marque": marque.replace("%20"," "),
                                    "Produit": product_names,
                                    "Référence": product_ref,
                                    "Prix": product_prices})
                #Price formating
                results_marque_df["Prix"] = results_marque_df["Prix"].apply(lambda x : clean_prices(x))
                results_marque_df["Prix"] = round(pd.to_numeric(results_marque_df["Prix"]),2)

                #Concatenation of data
                results_df = pd.concat([results_df,results_marque_df])
                results_df.reset_index(drop=True,inplace=True)

    return results_df