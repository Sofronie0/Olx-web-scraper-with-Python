import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
import sys
import os.path


def main():
    search_query = get_search_term()
    if_no_file_create_header()
    raw_links = olx_get_raw_links(search_query)
    pages = olx_get_pages_from_raw(raw_links)
    print("Getting links: ", end="")
    links = olx_get_all_links(raw_links, pages)
    print(f" completed! ({len(links)})")
    print("Appending to csv data from individual links: ")
    for link in links:
        link = f"https://www.olx.ro/{link}"
        while True:
            try:
                olx_get_ad_info_and_append_to_csv(link)
                break
            except (TypeError):
                print("BeautifulSoup attempt failed (JavaScript not loading), retrying...")
    print("Completed!")


# Get user input from command line or prompt input and return it as an olx search query link
def get_search_term():
    if len(sys.argv) > 1:
        joined = "-".join(sys.argv[1:])
        link = f"https://www.olx.ro/oferte/q-{joined}"
        return link
    else:
        try:
            search_term = input("Search for: ")
            joined = search_term.replace(" ", "-")
            link = f"https://www.olx.ro/oferte/q-{joined}"
            return link
        except:
            sys.exit("Invalid search")


# If the csv file has not been created already, create it and write the header in it
def if_no_file_create_header():
    if os.path.isfile("output.csv") == False:
        with open("output.csv", "a", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "Current date",
                    "Current time",
                    "Ad ID",
                    "Ad date",
                    "Title",
                    "Price",
                    "Currency",
                    "Seller name",
                    "Seller is on OLX since",
                    "Ad description",
                    "Ad link",
                ],
            )
            writer.writeheader()


# Get all links from the page
def olx_get_raw_links(link):
    # Make a request at the search query link
    req = requests.get(link)
    # Use BeautifulSoup to get the html content of the page
    soup = BeautifulSoup(req.content, "html.parser")
    raw_links = []
    # Append in raw_links all links from the "a" tag, specificalyl from "href=..."
    for link in soup.find_all("a"):
        raw_links.append(link.get("href"))
    return raw_links


# Get the useful links
def olx_get_links_from_raw(raw_links):
    # Create a set to filter out duplicate links (for example, the promoted ads at the top of the page)
    links = set()
    for link in raw_links:
        if isinstance(link, str):
            # Only get the links that contain in them "/d/oferta/.+\.html"
            if re.search(r"/d/oferta/.+\.html", link):
                links.add(link)
    return links


# Search and return pages of search query, if there are (first page is not included in this)
def olx_get_pages_from_raw(raw_links):
    # use a set to filter out duplicates
    pages = set()
    for link in raw_links:
        if isinstance(link, str):
            # Only get the links that contain in them "/oferte/q\-.+/(?:\?page=[0-9]+)"
            if re.search(r"/oferte/q\-.+/(?:\?page=[0-9]+)", link):
                # Add the links for the pages in a variable called "pages"
                pages.add(link)
    # Return the pages found, excluding the first page (first page has different URL)
    return sorted(pages)


# Get all links related to the search query
def olx_get_all_links(raw_links, pages):
    # Get all the links from the first page
    links = olx_get_links_from_raw(raw_links)
    # If there are aditional pages, use each page to get new search query links
    if len(pages) > 0:
        search_links = []
        for page in pages:
            search_links.append(f"https://www.olx.ro{page}")
        new_links = set()
        # For each search link (specific to one page), get all links
        for search_link in search_links:
            new_raw_link = olx_get_raw_links(search_link)
            # Get links from that page and add them in the new_links set
            new_links |= olx_get_links_from_raw(new_raw_link)
        # Return the set formed from the links from page 1 and the links from the other pages
        return links | new_links
    else:
        # If no other pages, only return links from page 1
        return links


# Get the informations from the ad and put them in a .csv file
def olx_get_ad_info_and_append_to_csv(link):
    # Using a given link, make a get request
    req = requests.get(link)
    # Print that link so user can see progress
    print(link)
    # Use BeautifulSoup to get the html content of the page
    soup = BeautifulSoup(req.content, "html.parser")
    # Get information from page
    ad_id = olx_get_ad_id(soup)
    ad_date = olx_get_ad_post_date(soup)
    ad_title = olx_get_ad_title(soup)
    ad_price, ad_currency = olx_get_ad_price_and_currency(soup)
    seller_name, seller_on_olx_since = olx_get_ad_seller_info(soup)
    ad_description = olx_get_ad_description(soup)
    # Append to the .csv file the information taken from the link
    olx_append_to_csv(
        ad_id,
        ad_date,
        ad_title,
        ad_price,
        ad_currency,
        seller_name,
        seller_on_olx_since,
        ad_description,
        link,
    )


# Append to the .csv file relevant information
def olx_append_to_csv(
    ad_id,
    ad_date,
    ad_title,
    ad_price,
    ad_currency,
    seller_name,
    seller_on_olx_since,
    ad_description,
    ad_link,
):
    # Open the .csv file and append to it
    with open("output.csv", "a", encoding="utf-8") as file:
        # use a dict writer to write in the file and to set the field names
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Current date",
                "Current time",
                "Ad ID",
                "Ad date",
                "Title",
                "Price",
                "Currency",
                "Seller name",
                "Seller is on OLX since",
                "Ad description",
                "Ad link",
            ],
        )
        # Get today's date and time to append into the csv
        now = datetime.now()
        current_date = now.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")
        # Write a row in the .csv containing relevant information, as seen below
        writer.writerow(
            {
                "Current date": current_date,
                "Current time": current_time,
                "Ad ID": ad_id,
                "Ad date": ad_date,
                "Title": ad_title,
                "Price": ad_price,
                "Currency": ad_currency,
                "Seller name": seller_name,
                "Seller is on OLX since": seller_on_olx_since,
                "Ad description": ad_description,
                "Ad link": ad_link,
            }
        )


# Get the ID of a certain ad posted on Olx
def olx_get_ad_id(soup):
    # In the "soup" object search for a "span" tag that has the class mentioned below
    ad_id = str(soup.find("span", "css-12hdxwj er34gjf0"))
    # If text that fits the regular expression is found, return int(text)
    if matches := re.search(r"^<span.+>(.+)</span>$", ad_id):
        ad_id = matches.group(1)
        return int(ad_id)


# Get the post date of a certain ad posted on Olx
def olx_get_ad_post_date(soup):
    # In the "soup" object search for a "span" tag that has the class mentioned below
    ad_date = str(soup.find("span", "css-19yf5ek"))
    # If text that fits the regular expression is found, return it
    if matches := re.search(r"^<span.+>(.+)</span>$", ad_date):
        ad_date = matches.group(1)
        return ad_date


# Get the title of a certain ad posted on Olx
def olx_get_ad_title(soup):
     # In the "soup" object search for an "h1" tag that has the class mentioned below
    ad_title = str(soup.find("h1", "css-dq22zc er34gjf0"))
    if matches := re.search(r"^<h1.+>(.+)</h1>$", ad_title):
        # If text that fits the regular expression is found, return it
        ad_title = matches.group(1)
        return ad_title

# Get the price and currency from a certain ad posted on Olx
def olx_get_ad_price_and_currency(soup):
    # Try to get price and currency
    try:
        # In the "soup" object search for an "h3" tag that has the class mentioned below
        ad_price = str(soup.find("h3", "css-t9ee1 er34gjf0"))
        # If text that fits the regular expression is found, pass it to ad_price
        if matches := re.search(r"^<h3.+>(.+)</h3>$", ad_price):
            ad_price = matches.group(1)
            # Split the text by whitespace
            ad_price = ad_price.split(" ")
            # Use as currency the last element of the list
            currency = ad_price[-1]
            # Use as ad_price all the elements up to the currency, not including currency
            ad_price = ad_price[:-1]
            price = ""
            # Since price can be as big as it can get and it is separated by " " on Olx
            for i in range(len(ad_price)):
                # For each element in the splitted list of prices, append it from start to finish to "price"
                price += ad_price[i]
            # Return the price and the currency
            return price, currency
    # Except there is a TypeError, return (0, 0) to signal an error but not crash the program
    except (TypeError):
        return 0, 0


# Get the seller's information from a certain ad posted on Olx
def olx_get_ad_seller_info(soup):
    # In the "soup" object search for an "h4" tag that has the class mentioned below
    seller_name = str(soup.find("h4", "css-1lcz6o7 er34gjf0"))
    # If text that fits the regular expression is found, store it as seller_name
    if matches := re.search(r"^<h4.+>(.+)</h4>$", seller_name):
        seller_name = matches.group(1)
    # In the "soup" object search for a "div" tag that has the class mentioned below
    seller_on_olx_since = str(soup.find("div", "css-16h6te1 er34gjf0"))
    # If text that fits the regular expression is found, store it as seller_on_olx_since
    if matches := re.search(r"^<div.+>Member Since (.+)</div>$", seller_on_olx_since):
        seller_on_olx_since = matches.group(1)
    # Return the values obtained
    return seller_name, seller_on_olx_since

# Get the description from a certain ad posted on Olx
def olx_get_ad_description(soup):
    # In the "soup" object search for a "div" tag that has the class mentioned below and replace <br/> with ""
    ad_description = str(soup.find("div", "css-1t507yq er34gjf0")).replace("<br/>", "")
    # If text that fits the regular expression is found
    if matches := re.search(r"^<div.+>(.+)+</div>$", ad_description, re.DOTALL):
        # Replace new line with semicolon so it can be more easily read in .csv files and in excel files
        ad_description = matches.group(1).replace("\n", "; ")
        # Return the description
        return ad_description


if __name__ == "__main__":
    main()
