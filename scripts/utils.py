import os

def clean_path(path: str):
    """Function to replace special character in path.

    Parameters
    ----------
    path : path with string format

    Returns
    ----------
    path : clean path as string
    
    """
    #Normalizing the path to deal with backslash and integer in a string (ex : \3 becomes \x03 without the code below)
    path = '%r' %path
    path = path.replace("x0","").replace("x8","20").replace("'","")
    path = os.path.normpath(path)

    return path

def clean_prices(price: str):
    """Function to clean prices extracting from websites.

    Parameters
    ----------
    price : raw price as string
    
    Returns
    ----------
    price : clean price as string

    """

    price = price.replace(",",".").replace("€","").replace(" ht","").rstrip().replace(" ","").replace("\xa0","").replace("\u202f","")
    return price