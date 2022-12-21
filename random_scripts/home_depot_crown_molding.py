import math
import pprint
import requests
from bs4 import BeautifulSoup

def get_pricing_data(search_term: str) -> dict:
    """
    Queries all products from Home Depot that match the given search term and returns a dictionary of pricing data.

    Args:
        search_term: The search term to use when querying products from Home Depot.

    Returns:
        A dictionary of pricing data for products that match the given search term. The dictionary keys are the product titles
        and the values are the prices.
    """
    # Set the URL for the Home Depot search page
    url = 'https://www.homedepot.com/s/' + search_term.replace(' ', '%20')

    # Make a request to the Home Depot search page
    response = requests.get(url)

    # Parse the HTML of the search page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the products on the page
    products = soup.find_all('div', {'class': 'pod-inner'})

    # Calculate the number of products to process
    num_products = len(products)

    # Create an empty dictionary to store the pricing data
    pricing_data = {}

    # Loop through each product and extract the title and price
    for i, product in enumerate(products):
        # Calculate the progress percent
        progress_percent = math.floor((i / num_products) * 100)

        # Print the progress percent
        print(f'{progress_percent}%')

        title = product.find('h3').text
        price = product.find('span', {'class': 'price'}).text

        # Add the title and price to the dictionary
        pricing_data[title] = price

    return pricing_data

if __name__ == '__main__':
    # Example code
    pricing_data = get_pricing_data('crown molding')
    pprint.pprint(pricing_data)