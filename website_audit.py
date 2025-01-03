import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import matplotlib.pyplot as plt
import pandas as pd
import json

# Function to check the HTTP status of a website
def check_http_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

# Function to extract meta tags for SEO analysis
def extract_meta_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tags = {meta.get('name', '').lower(): meta.get('content', '') for meta in soup.find_all('meta') if meta.get('name')}
        return meta_tags
    except Exception as e:
        return f"Error: {e}"

# Function to check website links for broken URLs
def check_broken_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        broken_links = []

        for link in links:
            full_url = link if urlparse(link).netloc else urlparse(url)._replace(path=link).geturl()
            try:
                link_response = requests.get(full_url)
                if link_response.status_code != 200:
                    broken_links.append((full_url, link_response.status_code))
            except requests.RequestException as e:
                broken_links.append((full_url, str(e)))

        return broken_links
    except Exception as e:
        return f"Error: {e}"

# Function to evaluate text-to-HTML ratio for content assessment
def evaluate_text_to_html_ratio(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        text_length = len(text)
        html_length = len(response.text)
        ratio = (text_length / html_length) * 100
        return ratio
    except Exception as e:
        return f"Error: {e}"

# Function to visualize findings
def visualize_results(results, title, ylabel):
    plt.figure(figsize=(10, 5))
    plt.bar(results.keys(), results.values())
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.show()

# Main Function for Website Audit
def website_audit(url):
    print("Starting Website Audit...")
    
    # 1. Check HTTP Status
    http_status = check_http_status(url)
    print(f"HTTP Status: {http_status}")
    
    # 2. Extract Meta Tags
    meta_tags = extract_meta_tags(url)
    print("Meta Tags Found:")
    for tag, content in meta_tags.items():
        print(f"  {tag}: {content}")
    
    # 3. Check for Broken Links
    print("Checking for Broken Links...")
    broken_links = check_broken_links(url)
    if broken_links:
        print(f"Broken Links Found: {len(broken_links)}")
        for link, status in broken_links:
            print(f"  {link}: {status}")
    else:
        print("No Broken Links Found.")
    
    # 4. Evaluate Text-to-HTML Ratio
    print("Evaluating Text-to-HTML Ratio...")
    text_to_html_ratio = evaluate_text_to_html_ratio(url)
    print(f"Text-to-HTML Ratio: {text_to_html_ratio:.2f}%")

    # Visualize Text-to-HTML Ratio
    results = {"Text-to-HTML Ratio": text_to_html_ratio}
    visualize_results(results, "Website Content Analysis", "% Ratio")

# Example Usage
if __name__ == "__main__":
    target_url = input("Enter the URL of the website to audit: ")
    website_audit(target_url)


"""
How to Use
Save the code into a Jupyter Notebook cell.
Run the cell and provide the URL of the website you want to audit.
The tool will analyze the website and output:
    HTTP status.
    Meta tags for SEO analysis.
    Broken links (if any).
    Text-to-HTML ratio.
"""
