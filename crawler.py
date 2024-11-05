from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime
import requests
import time
import threading

def get_citation_count(arxiv_url):
    try:
        arxiv_id = arxiv_url.split('/abs/')[-1].split('v')[0]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        api_url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('citationCount', 0)
        return 0
    except Exception as e:
        print(f"\rError getting citation for {arxiv_id}: {str(e)}", end='')
        return 0

def get_arxiv_papers(search_query, start_year, end_year, max_results=100):
    unlimited = max_results == -1  
    if unlimited:
        max_results = float('inf') 
    
    date_query = f' AND submittedDate:[{start_year}0101 TO {end_year}1231]'
    full_query = search_query + date_query
    
    base_url = 'http://export.arxiv.org/api/query?search_query=all:{}&start={}&max_results={}&sortBy=submittedDate&sortOrder=descending'
    
    papers = []
    start = 0
    stop_crawling = False
    
    def check_input():
        nonlocal stop_crawling
        while True:
            if input().lower() == 'q':
                stop_crawling = True
                break
    
    input_thread = threading.Thread(target=check_input, daemon=True)
    input_thread.start()
    
    print("\nType 'q' and press Enter to stop crawling...")
    
    while (unlimited or len(papers) < max_results) and not stop_crawling:
        current_url = base_url.format(full_query, start, 100)
        response = requests.get(current_url)
        soup = bs(response.content, 'xml')
        
        entries = soup.find_all('entry')
        if not entries:
            break
            
        for entry in entries:
            if stop_crawling:
                break
                
            try:
                pub_date = datetime.datetime.strptime(entry.published.text.split('T')[0], '%Y-%m-%d')
                pub_year = pub_date.year
                
                if start_year <= pub_year <= end_year:
                    paper = {
                        'title': entry.title.text.replace('\n', ' ').strip(),
                        'authors': '; '.join([author.find('name').text for author in entry.find_all('author')]),
                        'published': entry.published.text.split('T')[0],
                        'summary': entry.summary.text.replace('\n', ' ').strip(),
                        'link': entry.id.text
                    }
                    time.sleep(1)
                    paper['citations'] = get_citation_count(entry.id.text)
                    papers.append(paper)
                    
                    if not unlimited and len(papers) >= max_results:
                        stop_crawling = True
                        break
                    
                    print(f'\rCurrently found {len(papers)} papers...', end='')
            except AttributeError:
                continue
        
        if not stop_crawling:
            time.sleep(3)
            start += 100
    
    if stop_crawling:
        print("\nCrawling stopped by user.")
        while True:
            save_choice = input("Do you want to save the currently collected papers? (y/n): ").lower()
            if save_choice in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")
        
        if save_choice == 'y':
            return papers
        return []
    
    print() 
    return papers


def validate_year(year_str, year_type):
    try:
        year = int(year_str)
        current_year = datetime.datetime.now().year
        if year < 1900 or year > current_year: 
            print(f"{year_type} year is not valid. Please enter a value between 1900 and {current_year}.")
            return None
        return year
    except ValueError:
        print(f"{year_type} year is not valid. Please enter a number.")
        return None

def save_to_csv(papers, filename='arxiv_papers.csv'):
    df = pd.DataFrame(papers)
    df = df.sort_values(by='citations', ascending=False)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f'File saved: {filename}')
    print(f'Papers are sorted by citation count (highest to lowest)')
    print("----------------------------------------------------------")

def main():
    print("Welcome to the Arxiv Paper Crawler! Made by @mjlee111")
    print("Please enter the following information to search for papers.")
    print("----------------------------------------------------------")
    
    search_query = input("Enter the search topic: ")
    print(f"Search topic: {search_query}")
    print("----------------------------------------------------------")

    
    while True:
        start_year = validate_year(input("Enter the start year (1900-current): "), "start")
        if start_year is not None:
            break
    
    while True:
        end_year = validate_year(input("Enter the end year (start year-current): "), "end")
        if end_year is not None and end_year >= start_year:
            break
        elif end_year is not None:
            print("The end year must be greater than the start year.")
    print("Crawling Papers between", start_year, "and", end_year)
    print("----------------------------------------------------------")

    
    max_results = int(input("Enter the maximum number of papers to search (-1: unlimited, default: 100): ") or 100)
    print("Crawling papers maximum", max_results    )
    print("----------------------------------------------------------")
    
    print("Crawling...")
    papers = get_arxiv_papers(search_query, start_year, end_year, max_results)
    
    if not papers:
        print("Crawling cancelled. No data saved.")
        return
        
    print(f"Found {len(papers)} papers.")
    print("----------------------------------------------------------")
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'arxiv_{search_query}_{start_year}-{end_year}_{timestamp}.csv'
    save_to_csv(papers, filename)

if __name__ == "__main__":
    main()