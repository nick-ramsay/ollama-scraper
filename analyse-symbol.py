import sys
import requests
import pprint
import threading
import itertools
import time
from bs4 import BeautifulSoup

# Get symbol from command line argument, default to AAPL
symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL" 

URL = f"https://finviz.com/quote.ashx?t={symbol}"
headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
      }
# Example static website
try:
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    html_content = response.content
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(html_content, "html.parser")
fundamentals = soup.find("table", class_="snapshot-table2")

company_symbol = soup.find("h1", class_="quote-header_ticker-wrapper_ticker").text.strip()
company_name = soup.find("h2", class_="quote-header_ticker-wrapper_company").a.text.strip()
print(f"Company: '{company_name}' ({company_symbol})")
print("--------------------------------")



stock_data = {
    "company_name": company_name,
    "company_symbol": company_symbol,
    "fundamentals": {}
}

if fundamentals:
    for row in fundamentals.find_all("tr"):
        cells = row.find_all("td")
        # Iterate in pairs: key at even index, value at odd index
        for i in range(0, len(cells), 2):
            if i + 1 < len(cells):
                key = cells[i].text.strip()
                value = cells[i + 1].text.strip()
                stock_data["fundamentals"][key] = value
    
    # Call LLM analysis with the scraped stock data
    print("Fundamentals:")
    print("--------------------------------")
    pprint.pprint(stock_data["fundamentals"])
    print("--------------------------------")
    print("LLM Analysis:")
    print("--------------------------------")
    from ollama_prompt import llm_analysis
    
    # Loading spinner
    stop_spinner = threading.Event()
    def spinner():
        for char in itertools.cycle('⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'):
            if stop_spinner.is_set():
                break
            sys.stdout.write(f'\r{char} Analyzing...')
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\r' + ' ' * 20 + '\r')  # Clear the spinner line
        sys.stdout.flush()
    
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()
    
    analysis = llm_analysis(stock_data)
    
    stop_spinner.set()
    spinner_thread.join()
    
    print(analysis)
else:
    print("No fundamentals found")
    
