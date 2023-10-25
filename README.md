# Olx listings web scraper with Python
## Video Demo: [Video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
## Project description
This program takes as input a search query, takes all the listings from Olx that match the search query and returns for every listing each listing's ID, posting date, title, price, currency, the seller's name, the date at which the seller has registered on Olx, the listing description and the listing's link. All these elements are appended into a .csv file.

The purpose of this project was creating an automated program that, when launched and given a specific search query, it will return in a .csv file all the data that was specified. This way, the user can create his own .csv file containing all the listings from Olx for a certain item at a certain date, allowing him to keep track of price changes over time, the average price of the item etc.


## Introduction
Olx is an online market. It allows everyone to open an account and post a listing of a product,second hand or brand new. It is used mostly by people to sell and buy things, but it is not uncommon to see shops or retailers seeling their products on it too.

Web scraping is the process of extracting data from a site. Using various libraries, this process can hand the user data from a site, allowing the user to do with them as they see fit. In this project, the library used is called Beautiful Soup.

This project was created for personal purposes, those being collecting all listings of a specific motorcycle from Olx. I plan to run this program every week so I can acquire in my .csv file a lot of listings of that motorcycle. The reason for me doing this project is so I can see how the price varies summer and winter and to be able to easily find in the future good deals, for when I will decide to buy that motorcycle.

## How to use
Using this program is pretty straight forward. It takes as a command line argument the search query (for example, `python project.py bmw s1000rr`) and uses that to search for it on Olx. If the search query is not specified in the command line (for example, `python project.py`), the program will prompt the user for the search query in the terminal window.

After specifying the search query, the user has nothing left to do. The program will get every listing related to the search query and will extract from it the data, appending it to a .csv file called `output.csv`.

The process of getting the links for every single listing, entering that specific page of the listing and get the data is quite lenghty, taking on average 0.5 to 2 seconds per listing (this time was recorded during testing on 20 Octomber 2023 and it may vary from user to user). In order to show progress, after getting all the listings the program will announce it (via `print()`) and will continue to enter every single listing and get the data from it, printing the link of the listing to show progress to the user.

In the end, the user will get an `output.csv` file that he can use as is or can be imported into an Excel for a better viewing experience.

**Note:** This program appends to the output.csv all new data. If the output.csv file is present in the same directory as the program, it will append all the data from the listings to the same file, leaving the responsability to the user to use Excel (example in the video) or other program to filter out duplicates (in case the listings from the previous run of the program are the same as the listings from the current run of the program). If there isn't an output.csv file in the same directory, the program will write a new output.csv file, containing the header + the data.

**Using the same directory**: In case the output.csv file does not appear in the same directory as project.py, do not worry. It is being saved in the directory that you are in at the moment. In order for it to be created in the same directory, use `cd` to enter in the directory that has project.py and then call out `python project.py`.

If there are any **errors**, ensure you have the required dependencies installed. You can install them using the following command:
``` console
pip install -r requirements.txt
```

## Structure
The project contains 5 files:
- README.md
- requirements.txt
- test_project.html
    - this file represents a mock file for a certain listing's html. It is used to test functions and it was created because testing using listings that change over time is not reliable.
- test_project.py
    - this file tests the function get_search_term and, using the mock html file from above, tests the functions that fetch the required data from the listing's html.
- project.py
    - this file contains the main function and all functions requires to run it.


For proper use, it's recommended that all the files are located in the same directory.
#### Functions
- **main()**
    - using all the functions mentioned below, allows the user to specify a search query, as terms they would search for on Olx, and appends to a .csv file the data found in each listing that appears on the site regarding that search query.
- `get_search_term()`
    - used to get the search query as a link from user input through the terminal window or through the command line arguments.
    - it returns the search query as a link.
- `if_no_file_create_header()`
    - used to check if there is an output.csv file in the same directory. If there isn't such a file, the program will create it and will add the header to it.
- `olx_get_raw_links(link)`
    - using the search query link, this function makes a request to get the html content of the page and uses BeautifulSoup to parse through it, extracting all the links after "href=" from the `<a>` tags.
    - takes as argument the link of the page (search query link, in this case) and it returns a list of all the links from the page.
- `olx_get_links_from_raw(raw_links)`
    - using regular expressions, take from the links in the page (raw_links) only the ones that fit the regular expression (the links for listings) and add them to a set (to filter out duplicates).
    - takes as argument the list of raw links and returns a set containing the listing links.
- `olx_get_pages_from_raw(raw_links)`
    - using regular expressions, take from the links in the page (raw_links) only the ones that fit the regular expression (the links for pages) and add them to a set (to filter out duplicates).
    - takes as argument the list of raw links and returns a set containing the links for the pages.
- `olx_get_all_links(raw_links, pages)`
    - creates a set for the links, takes all the  listing links from the first page and, if there are multiple pages, uses the pages links as raw_links and calls olx_get_links_from_raw function, adding each listing link to the set.
    - takes as argument raw_links (the link for the first page) and pages (the links for the other pages, if there are any) and it returns a set containing all the listing links from all pages.
- `olx_get_ad_info_and_append_to_csv(link)`
    - using requests and BeautifulSoup, it gets the html data from a specific listing link, calls out other functions to get the specific element needed from the html (listing ID, price etc.) and using another function, appends all the data extracted from the listing to a .csv file
    - takes as argument a listing link (in this case, from the set containing all the listing links) and does not have a return value, this function's purpose being to append the data to the .csv file.
- `olx_append_to_csv(ad_id, ad_date, ad_title, ad_price, ad_currency, seller_name, seller_on_olx_since, ad_description, ad_link)`
    - using the csv library, it opens a csv as "append" and writes in it with a DictWriter the current date, current time and the rest of the function's arguments.
    - takes as argument the data that needs to be appended in the csv and does not have a return value, this function's purpose being appending the given data to the .csv file, completing the function mentioned above.
- All the next functions take as argument the soup object, created with BeautifulSoup, in order to find in the html content the data needed.
    - `olx_get_ad_id(soup)`
        - using regular expressions, searches for the listing id in the html and returns it
    - `olx_get_ad_post_date(soup)`
        - using regular expressions, searches for the listing post date in the html and returns it
    - `olx_get_ad_title(soup)`
        - using regular expressions, searches for the title of the listing in the html and returns it
    - `olx_get_ad_price_and_currency(soup)`
        - using regular expressions, searches for the price and currency of the listing in the html and returns them
    - `olx_get_ad_seller_info(soup)`
        - using regular expressions, searches for the seller name and the date at which they joined Olx in the html and returns them
    - `olx_get_ad_description(soup)`
        - using regular expressions, searches for the listing description in the html and returns it

### Contributions
This project was developed solely by [Andrei-Laureţiu Sofronie](https://github.com/Sofronie0) using knowledge acquired from CS50's Introduction to Programming with Python (CS50P), personal expertise and research.


##### Questions and Contact
For any inquiries or further assistance, feel free to reach out via email at andreilaurentiusofronie@gmail.com.
