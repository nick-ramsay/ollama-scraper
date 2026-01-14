# Ollama Stock Analyzer

A command-line tool that scrapes stock fundamentals from Finviz and uses a local LLM (via Ollama) to provide investment analysis and recommendations.

Given a stock ticker symbol, the application fetches key financial metrics such as P/E ratio, market cap, dividend yield, and more, then sends this data to a locally-running LLM for analysis. The LLM returns a brief summary of the investment opportunity along with a buy/hold/sell recommendation.

**This application is merely a technical demonstration and should not be taken as financial advice.**

## How It Works

### Dependencies

- **requests** – HTTP library for fetching web pages and calling the Ollama API
- **beautifulsoup4** – HTML parsing library for extracting stock data from Finviz
- **Ollama** – Local LLM runtime (must be installed and running separately)

### Technical Overview

1. **Web Scraping** (`analyse-symbol.py`): The script fetches the Finviz quote page for the given stock symbol and uses BeautifulSoup to parse the HTML. It extracts the company name, ticker symbol, and a table of fundamental metrics (P/E, EPS, market cap, etc.).

2. **LLM Analysis** (`ollama_prompt.py`): The scraped data is passed to the `llm_analysis()` function, which sends a POST request to the local Ollama API. The prompt instructs the model to act as an investment analyst and provide a concise summary with a recommendation.

3. **Output**: The terminal displays the company info, raw fundamentals, and the LLM-generated analysis. A loading spinner provides feedback while waiting for the LLM response.

## Installation & Usage

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running locally on port 11434
- A compatible model pulled in Ollama (the script uses `gpt-oss:20b` by default)

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ollama-scraper
   ```

2. Install Python dependencies:
   ```bash
   pip install requests beautifulsoup4
   ```

3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

4. Pull the required model (or modify `ollama_prompt.py` to use a different model):
   ```bash
   ollama pull gpt-oss:20b
   ```

### Running the Application

Analyze a stock by passing the ticker symbol as an argument:

```bash
python analyse-symbol.py AAPL
```

If no symbol is provided, it defaults to `AAPL`:

```bash
python analyse-symbol.py
```

### Example Output

```
Company: 'Apple Inc.' (AAPL)
--------------------------------
Fundamentals:
--------------------------------
{'52W High': '-12.34%',
 '52W Low': '25.67%',
 'Dividend': '0.96',
 'EPS (ttm)': '6.42',
 'Market Cap': '2.89T',
 'P/E': '28.45',
 ...}
--------------------------------
LLM Analysis:
--------------------------------
Apple Inc. (AAPL) is a technology giant with strong fundamentals...

In my current opinion, this is a HOLD.
```

