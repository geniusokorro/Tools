import requests
import os
from xml.etree import ElementTree

# Function to search papers on arXiv based on keywords
def search_arxiv(keywords, max_results=5):
    search_url = "http://export.arxiv.org/api/query?"
    
    # Format the query with keywords and limit the number of results
    query = f"search_query=all:{keywords}&start=0&max_results={max_results}"
    response = requests.get(search_url + query)
    
    if response.status_code == 200:
        # Parse the XML response
        root = ElementTree.fromstring(response.content)
        entries = root.findall("{http://www.w3.org/2005/Atom}entry")
        
        papers = []
        for entry in entries:
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
            pdf_link = entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib['href']
            papers.append({
                "title": title,
                "authors": authors,
                "pdf_link": pdf_link
            })
        
        return papers
    else:
        print(f"Failed to retrieve papers: {response.status_code}")
        return []

# Function to download PDFs
def download_pdf(pdf_link, folder="downloads"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    response = requests.get(pdf_link)
    if response.status_code == 200:
        pdf_name = pdf_link.split("/")[-1]
        pdf_path = os.path.join(folder, pdf_name)
        
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Downloaded: {pdf_name}")
    else:
        print(f"Failed to download PDF from {pdf_link}")

# Main script to search and download papers based on keywords
def main():
    keywords = input("Enter keywords to search on arXiv: ")
    max_results = int(input("Enter the number of results to retrieve: "))
    
    # Search for papers
    papers = search_arxiv(keywords, max_results)
    
    if papers:
        print(f"Found {len(papers)} papers.")
        for i, paper in enumerate(papers):
            print(f"\nPaper {i+1}:")
            print(f"Title: {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"PDF Link: {paper['pdf_link']}")
            
            # Download PDFs
            download_pdf(paper['pdf_link'])
    else:
        print("No papers found.")

if __name__ == "__main__":
    main()
