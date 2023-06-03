import pandas as pd

def params():
    """
    Fonction storing the scraping parameters:
        - websites
        - URL
        - xpath to cookies accept click button
        - xpath to the load more button
        - html tag of product prices per website
        - html tag of product names per website
        - html tag of product references per website
        - other : xpath to close promotion window on bruneau website

    Returns
    -------
    A dataframe with all the parameters

    """

    input_df = pd.DataFrame({
                "website":["bernard","jpg","raja","manutan","bruneau"],
                "url":["https://www.bernard.fr/?query={marque_field}&refinementList%5BMarque%20gamme%20web%5D%5B0%5D={marque_field}&SearchCat=natural&SearchQuery={marque_field}",
                        "https://www.jpg.fr/?query={marque_field}&refinementList%5BMarque%20gamme%20web%5D%5B0%5D={marque_field}&SearchCat=natural&SearchQuery={marque_field}",
                        "https://www.raja.fr/?query={marque_field}&refinementList%5BZ_CARACT_ATT_014%5D%5B0%5D={marque_field}&SearchCat=natural&SearchQuery={marque_field}",
                        "https://www.manutan.fr/SearchDisplay?categoryId=&storeId=11701&catalogId=11604&langId=-2&sType=SimpleSearch&resultCatEntryType=2&showResultsPage=true&searchSource=Q&pageView=&beginIndex=0&pageSize=28&isSearchDFType=ES&searchTerm={marque_field}&authToken=109810278%252CzwSxxg0us%252B7%252BT7tKqbwrdK2IL1SvC2bD8BElZz45B%252Fc%253D#productBeginIndex:{max_product}&orderBy:0&",
                        "https://www.bruneau.fr/search?page={num_page}&term={marque_field}"],
                "xpath_cookies_accept":["/html/body/div[4]/div[2]/div[1]/button[2]",
                            "/html/body/div[4]/div[2]/div[1]/button[2]",
                            "/html/body/div[4]/div[2]/div[1]/button[2]",
                            "/html/body/div[6]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/button[2]",
                            "/html/body/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/button[1]"],
                "xpath_load_more_button":["/html/body/div[5]/div[1]/div[1]/div[3]/div[4]/button[1]",
                                    "/html/body/div[5]/div[1]/div[1]/div[3]/div[4]/button[1]",
                                    "/html/body/div[5]/div[1]/div[1]/div[3]/div[4]/button[1]",
                                    None,
                                    "/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/a[1]"],
                "class_price":[("span","bold Price_overline Price_overline-yellow"),
                                ("span","bold Price_overline Price_overline-yellow"),
                                ("span","bold Price_overline Price_overline-yellow"),
                                ("span","price"),
                                ("span","isg-gros-text-arial-gras")],
                "class_name":[("span","Product-title text-black"),
                                ("span","Product-title text-black"),
                                ("span","Product-title text-black"),
                                ("a","prodlist-item"),
                                ("p","isg-catalog-product-title")],
                "class_ref":[("span","Product-sku"),
                                ("span","Product-sku"),
                                ("span","Product-sku"),
                                ("div","product_name"),
                                ("div","isg-catalog-product")],
                "other":[None,None,None,None,"/html/body/div[1]/div[3]/div[2]/div[1]/button[1]"]
                        })
    
    return input_df

def import_brands():

    marques_df = pd.read_excel("params.xlsx",sheet_name="marques")

    marques = list(marques_df["Marques"])

    return marques

def import_output_path():

    output_path_df = pd.read_excel("params.xlsx",sheet_name="dossier_destination")

    output_path = output_path_df["Chemin destination"].values[0]

    return output_path


if __name__ =="__main__":
    print(import_output_path())
