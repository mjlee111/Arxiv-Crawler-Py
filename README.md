# Arxiv-Crawler-Py

Python scripts for crawling arXiv papers and converting CSV to Markdown tables.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache-green.svg)](LICENSE)
</div>


## Overview
This repository contains two Python scripts:

1. `crawler.py`: Crawls arXiv papers and saves them to a CSV file.
2. `csv_to_markdown_table.py`: Converts a CSV file to a Markdown table.


## Requirements
| Component | Version | Notes |
| --------- | ------- | ----- |
| Python    | 3.8+    |       |
| BeautifulSoup4 | Latest | For XML parsing |
| Pandas | Latest | For data handling |
| Requests | Latest | For HTTP requests |

## Development Environment
| Component | Version |
| --------- | ------- |
| Python    | 3.10    |
| Cursor AI    | Latest  |
| OS        | Ubuntu 22.04 LTS |


## Scripts

<div align="center">

| Script | Description | Usage |
| --------- | ------- | ----- |
| crawler.py | Crawls arXiv papers and saves them to a CSV file. | `python crawler.py --start_year 2021 --end_year 2024 --max_results 1000` |
| csv_to_markdown_table.py | Converts a CSV file to a Markdown table. | `python csv_to_markdown_table.py <csv_file_path> [markdown_file_path]` |
</div>

## Features
`crawler.py`
- Search papers by topic
- Filter by year range
- Configurable maximum results
- Exports results to CSV
- Automatic rate limiting
- Error handling for missing data

`csv_to_markdown_table.py`
- Converts CSV to Markdown table format
- Collapsible summary sections
- Automatic file naming
- Handles special characters
- Preserves data formatting

## Usage
`crawler.py`
```bash
$ python3 crawler.py
# Follow the interactive prompts:
# 1. Enter search topic
# 2. Enter start year
# 3. Enter end year
# 4. Enter maximum results (-1 for unlimited)
``` 

`csv_to_markdown_table.py`
```bash
# With custom markdown filename
$ python3 csv_to_markdown_table.py input.csv output.md

# Using default filename (same as CSV)
$ python3 csv_to_markdown_table.py input.csv
```     

## Contributing
I welcome all contributions! Whether it's bug reports, feature suggestions, or pull requests, your input helps me to improve. If you're interested in contributing, please check out my contributing guidelines or submit an issue.

## License
This project is licensed under the [Apache 2.0 License](LICENSE). Feel free to use and distribute it according to the terms of the license.

## Contact
If you have any questions or feedback, don't hesitate to reach out! You can contact me at [menggu1234@naver.com][email].

[email]: mailto:menggu1234@naver.com
