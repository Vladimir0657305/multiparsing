# multiparsing

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&pause=1000&width=435&lines=Scraping+coinmarketcap.com+site)](https://git.io/typing-svg)

This code parses data from the CoinMarketCap website.

1. Required modules and libraries are imported, such as selenium, requests, multiprocessing, urllib.parse, BeautifulSoup, datetime, time, csv, os and dotenv.

2. The settings are loaded from the .env file using dotenv.load_dotenv().

3. Set variables and proxy settings from environment variables using os.getenv(). A requests.Session() session is created and proxy servers for HTTP and HTTPS are specified.

4. The get_html function is defined, which uses Selenium WebDriver to load the page using Chrome. It scrolls down the page until the desired element is found or the end of the page is reached. It then returns the HTML code of the page.

5. The get_all_links function is defined, which takes the HTML code of the page and, using BeautifulSoup, extracts links to companies from the page and returns them as a list.

6. The get_html_data function is defined, which performs a GET request to the URL and returns the HTML code of the page as text.

7. The get_page_data function is defined, which takes a URL, loads the page using requests.get (or session.get if a proxy is used), then uses BeautifulSoup to retrieve the name and price data of the coin. The returned data is in the form of a dictionary.

8. The write_csv function is defined, which writes data to a CSV file.

9. The write_csv_links function is defined, which writes the links to the coins in the CSV file.

10. The make_all function is defined, which takes a reference to the coin, calls get_page_data to get the data about the coin, and writes it to a CSV file. If the coin data contains a 'None' value for the name, the function reloads the page and tries to get the data until the name value is determined.

11. The main function is defined, which executes the main logic of the program. It goes through the pages of the CoinMarketCap site, gets the links to the coins from each page, writes them to a CSV file, and generates a list of links for parallel execution. Then, using multithreading, the make_all function is executed for each link.

12. The main() function starts.

[![trophy](https://github-profile-trophy.vercel.app/?username=Vladimir0657305)]([https://github.com/ryo-ma/github-profile-trophy](https://github.com/Vladimir0657305))

[![Ashutosh's github activity graph](https://github-readme-activity-graph.cyclic.app/graph?username=Vladimir0657305&theme=react)](https://github.com/ashutosh00710/github-readme-activity-graph)

![](https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=Vladimir0657305&theme=solarized_dark)

![](https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=Vladimir0657305&theme=solarized_dark)
![](https://github-profile-summary-cards.vercel.app/api/cards/stats?username=Vladimir0657305&theme=solarized_dark)

![](https://komarev.com/ghpvc/?username=Vladimir0657305)
