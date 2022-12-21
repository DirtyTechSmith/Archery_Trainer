import pprint
import time
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver


class SearchResult:
    """A class representing a search result from Amazon.

    Attributes:
        title (str): The title of the product.
        link (str): The URL of the product page.
        price (str): The price of the product.
        average_rating (str): The average rating of the product.
    """

    def __init__(self, title: str, link: str, price: str, average_rating: str) -> None:
        """Initialize the search result.

        Args:
            title (str): The title of the product.
            link (str): The URL of the product page.
            price (str): The price of the product.
            average_rating (str): The average rating of the product.
        """
        self.title = title
        self.link = f"https://www.amazon.com{link}"
        self.price = price
        self.average_rating = average_rating

    def __str__(self) -> str:
        """Return a string representation of the search result.

        Returns:
            str: The string representation of the search result.
        """
        return f"\tTitle: {self.title}\n\tLink: {self.link}\n\tPrice: {self.price}\n\tAverage Rating: {self.average_rating}\n"

    def __repr__(self) -> str:
        """Return a string representation of the search result.

        Returns:
            str: The string representation of the search result.
        """
        return f"SearchResult({self.title!r}, {self.link!r}, {self.price!r}, {self.average_rating!r})"


def get_results_with_price(search_term: str, browser: webdriver.Chrome, max_results: int = 3) -> List[SearchResult]:
    """Get the top-rated search results with a price for a given search term on Amazon.

    Args:
        search_term (str): The search term to use for the Amazon search.
        browser (webdriver.Chrome): The Headless Chrome browser to use for the search.
        max_results (int, optional): The maximum number of results with a price to return per search term. Default is 3.

    Returns:
        List[SearchResult]: A list of `SearchResult` objects representing the top-rated search results with a price for the given search term.
    """
    # Set up the URL for the Amazon search
    search_url = f"https://www.amazon.com/s?k={search_term}"

    # Navigate to the search URL using Headless Chrome
    browser.get(search_url)
    time.sleep(5)  # Wait for the page to load

    # Get the search results page HTML
    search_html = browser.page_source

    # Parse the search results page using BeautifulSoup
    soup = BeautifulSoup(search_html, "html.parser")

    # Find the list of search results
    search_results = soup.find_all("div", class_="s-result-item")

    # Extract the information for each result
    results_with_price = []
    num_results = 0
    for result in search_results:
        # Get the product title and link
        title_html = result.find("h2")
        if title_html:
            title = title_html.text
            link = title_html.find("a")["href"]

            # Get the product price
            price_html = result.find("span", class_="a-offscreen")
            if price_html:
                price = price_html.text

                # Get the product average rating
                rating_html = result.find("span", class_="a-icon-alt")
                if rating_html:
                    average_rating = rating_html.text
                else:
                    average_rating = "Average rating not available"

                results_with_price.append(SearchResult(title, link, price, average_rating))
                num_results += 1
                if num_results >= max_results:
                    break

    return results_with_price


def generate_shopping_list(search_terms: list[str], max_results: int = 3) -> dict[str, list[SearchResult]]:
    """Generate a shopping list of top-rated search results with a price for a list of search terms on Amazon.

    Args:
        search_terms (list[str]): The list of search terms to use for the Amazon search.
        max_results (int, optional): The maximum number of results with a price to return per search term. Default is 3.

    Returns:
        dict[str, list[SearchResult]]: A dictionary mapping search terms to lists of `SearchResult` objects representing the top-rated search results with a price for the given search term.
    """
    # Set up Headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)

    shopping_list = {}
    for search_term in search_terms:
        results = get_results_with_price(search_term, browser, max_results=max_results)
        shopping_list[search_term] = results

    # Close the browser
    browser.close()

    return shopping_list


if __name__ == "__main__":
    # Define the list of search terms
    search_terms = ["honey", "filtered water", "mead yeast", "fermentation vessel", "airlock", "hydrometer",
                    "bottles for mead", "corks or caps for bottles"]

    # Generate the shopping list
    shopping_list = generate_shopping_list(search_terms)

    # Print the shopping list
    print("Shopping List:")
    pprint.pprint(shopping_list)
