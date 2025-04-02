'''
Using Arxiv API, this solution downloads research papers based on given keywords and quantities
#To use this app install Requests by running 'pip install requests' in cmd/shell/bash
#Use Visual Studio Code or any preferred IDE to view the report after the download is complete
'''
'''
#Major Changes:
Updates documentation
Included a function to write the download report to a report.txt file for documentation of downloads 
Included a date and timestamp to record when it is downloaded
Added time.sleep preventing the app from being block when downloaded many files 
Changed the download foleder name to papers as downloads was creating an error running on windows from a the downloads folder the the reports.txt file fails to write
#Q&A:
pdf filename is the Arxiv document number because some titles are longer than windows systems filename capability
'''

import requests  # Install required
import os
import time
from datetime import datetime
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
def download_pdf(pdf_link, folder="papers"):
    # If the 'papers' folder does not exist, create it
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
        
        # Return the name of the downloaded file for logging
        return pdf_name
    else:
        # If the download fails, print an error message
        return None

# Function to write output to report.txt
def write_to_report(content, folder="papers", file_name="report.txt"):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    report_path = os.path.join(folder, file_name)
    with open(report_path, "a") as report_file:  # Open in append mode to keep updating the report
        report_file.write(content + "\n")

now = datetime.now().strftime("%d-%m-%Y %H:%M")

# Main function to search for papers and download them
def main():
    # Ask the user for keywords to search for papers
    keywords = input("Enter keywords to search on arXiv: ")
    
    # Ask the user for the number of results they want to retrieve
    max_results = int(input("Enter the number of results to retrieve: "))
    
    # Define the folder for PDFs and report file
    folder = "papers"
    
    # Initialize the report.txt file if it doesn't exist, or update it for new searches
    write_to_report(f"New Search - {now}\n", folder)
    write_to_report(f"Keywords: {keywords}\n", folder)
    write_to_report(f"Number of results: {max_results}\n", folder)
    
    # Search for papers based on the keywords
    papers = search_arxiv(keywords, max_results)
    
    # If papers are found, display details and download them
    if papers:
        write_to_report(f"Found {len(papers)} papers.\n", folder)
        
        # Loop through the papers and display details
        for i, paper in enumerate(papers):
            content = f"\nPaper {i+1}:\n"
            content += f"Title: {paper['title']}\n"
            content += f"Authors: {', '.join(paper['authors'])}\n"
            content += f"PDF Link: {paper['pdf_link']}\n"
            
            # Log to report.txt
            write_to_report(content, folder)
            
            # Download the PDF of the paper
            pdf_name = download_pdf(paper['pdf_link'], folder)
            if pdf_name:
                write_to_report(f"Downloaded: {pdf_name}", folder)
            else:
                write_to_report(f"Failed to download PDF from {paper['pdf_link']}", folder)
            
            # Add a small delay between requests
            time.sleep(0)  # Adjust to 1 or higher if there are a lot of papers to download
    
        write_to_report("\n" + "=" * 30 + "\n", folder)
    else:
        # If no papers are found, print a message
        write_to_report("No papers found.", folder)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()