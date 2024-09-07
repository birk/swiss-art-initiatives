#Make sure to install requests and beautifulsoup4
#Command is ==>
# pip install requests beautifulsoup4 langdetect
#replace by brew install python-requests for macimport csv
import requests, csv
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory

# Ensure consistent language detection results
DetectorFactory.seed = 0

# Language Q numbers
LANGUAGE_Q_NUMBERS = {
    'en': 'Q1860',  # English
    'fr': 'Q150',   # French
    'de': 'Q188',   # German
    'it': 'Q76'     # Italian
}

# Function to detect language from a given URL
def detect_language_from_url(url):
    try:
        # Fetch website content
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for language in <html lang="..."> attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.has_attr('lang'):
            return html_tag['lang']
        
        # If not available, detect language from the text content
        text_content = soup.get_text()
        if text_content:
            return detect(text_content)
        
        return "unknown"
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return "error"

# Load URLs from CSV file (adjust the file path and column name as needed)
csv_file = 'projects_websites_q_number.csv'  # Replace with your actual input CSV file path
rows = []

try:
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            url = row.get('website_first_wiki')  # Column name in the CSV file
            if url:
                # Detect language and get the Q number
                language_code = detect_language_from_url(url)
                q_number = LANGUAGE_Q_NUMBERS.get(language_code, 'null')
                row['website_q_language'] = q_number
                rows.append(row)
except FileNotFoundError:
    print(f"File not found: {csv_file}")
    exit(1)

# Write results to a new CSV file
output_file = 'project_with_web_lang.csv'  # Output CSV file path
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['itemLabel', 'website_q_number', 'website_first_wiki', 'website_q_language']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Processed {len(rows)} URLs and saved results to {output_file}.")


#url is sometimes empty, so we need to not open the empty urls