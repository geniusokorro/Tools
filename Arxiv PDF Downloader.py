'''
Using Arxiv API, this solution downloads research papers based on given keywords and quantities
#To use this app install Requests by running 'pip install requests' in cmd/shell/bash
'''

import requests 
import os
import time
from xml.etree import ElementTree

# Function to search for papers on arXiv based on keywords
def search_arxiv(keywords, max_results=5):
    search_url = "http://export.arxiv.org/api/query?"
    
    # Format the search query with the given keywords and limit the number of results
    query = f"search_query=all:{keywords}&start=0&max_results={max_results}"
    
    # Send a GET request to the arXiv API with the search query
    response = requests.get(search_url + query)
    
    # Check if the response is successful
    if response.status_code == 200:
        # Parse the XML response from arXiv API
        root = ElementTree.fromstring(response.content)
        
        # Extract all entries (papers) from the XML response
        entries = root.findall("{http://www.w3.org/2005/Atom}entry")
        
        papers = []  # List to store paper details
        for entry in entries:
            # Extract the paper's title
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            
            # Extract the authors of the paper
            authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]
            
            # Extract the link to the PDF of the paper
            pdf_link = entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib['href']
            
            # Append paper details (title, authors, and PDF link) to the list
            papers.append({
                "title": title,
                "authors": authors,
                "pdf_link": pdf_link
            })
        
        return papers
    else:
        # If the request fails, print the error code
        print(f"Failed to retrieve papers: {response.status_code}")
        return []

# Function to download the PDF of a paper
def download_pdf(pdf_link, folder="downloads"):
    # If the 'downloads' folder does not exist, create it
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Send a GET request to download the PDF
    response = requests.get(pdf_link)
    
    # Check if the PDF download was successful
    if response.status_code == 200:
        # Get the name of the PDF file (last part of the URL) and ensure it has a .pdf extension
        pdf_name = pdf_link.split("/")[-1]
        
        # Ensure the file ends with '.pdf'
        if not pdf_name.endswith(".pdf"):
            pdf_name += ".pdf"
        
        # Define the path to save the PDF
        pdf_path = os.path.join(folder, pdf_name)
        
        # Save the PDF content to the file
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        # Print a confirmation message
        print(f"Downloaded: {pdf_name}")
    else:
        # If the download fails, print an error message
        print(f"Failed to download PDF from {pdf_link}")


# Main function to search for papers and download them
def main():
    # Ask the user for keywords to search for papers
    keywords = input("Enter keywords to search on arXiv: ")
    
    # Ask the user for the number of results they want to retrieve
    max_results = int(input("Enter the number of results to retrieve: "))
    
    # Search for papers based on the keywords
    papers = search_arxiv(keywords, max_results)
    
    # If papers are found, display details and download them
    if papers:
        print(f"Found {len(papers)} papers.")
        
        # Loop through the papers and display details
        for i, paper in enumerate(papers):
            print(f"\nPaper {i+1}:")
            print(f"Title: {paper['title']}")
            print(f"Authors: {', '.join(paper['authors'])}")
            print(f"PDF Link: {paper['pdf_link']}")
            
            # Download the PDF of the paper
            download_pdf(paper['pdf_link'])
        #time.sleep(5)
    else:
        # If no papers are found, print a message
        print("No papers found.")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()