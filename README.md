# Archivar
A Python script for automated PDF processing, including OCR and archiving, to streamline document management.

## Overview
Archivar is a document management tool designed to streamline the process of handling physical correspondence. By leveraging a document scanner with an automatic feeder, Archivar enables efficient scanning, categorization, and OCR processing of large volumes of documents. The scanned PDFs are named according to a defined convention, including the scan date, categories (e.g., household/bills), and a sequential number. The system integrates with a local network and a document server (Linux OS) to facilitate organized storage and easy retrieval.

## Motivation
Managing vast amounts of physical correspondence was a tedious and time-consuming task, requiring manual filing and hole-punching. This process made it difficult to locate specific documents when needed, such as for tax purposes.
To address this issue, I purchased a Brother ADS-2800W document scanner with an automatic feeder, allowing for efficient scanning and two-step categorization (e.g., household/bills). The scanner produced PDFs with a defined filename format, including the scan date, categories, and a sequential number. These scans were stored on a network drive, accessible by a client that is always on and collects the scans. The original documents are filed in cardboard archive boxes and most of them thrown away after ten years.

Archivar takes over when the document server is on, categorizing the files, applying OCR, adding a text layer, identifying the date of the correspondence, adjusting the filename, and moving the file to the appropriate storage location on the document server. All files can now be searched with respective indexing and search tools like DocFetcher or Lookeen. This solution has significantly reduced the time and effort required for managing physical correspondence, improving organization and retrieval efficiency.

## Dependencies
Ensure you have the following dependencies installed and configured before proceeding with the installation and setup:

- Automatic document scanner, that allows for two staged categorization, configurable filenames and storage on local network shares. Or any other solution to populate the input directory with PDF files providing the required information.
  
- Intermediate document strage: Network Drive on always-on client to store scanned documents.
  
- Document Server (Linux OS)
  - Python: Ensure you have Python installed on the document server (preferably Python 3.7 or later).
    - Configparser: A Python module to handle configuration files. Included in the standard library.
    - Subprocess: A Python module to spawn new processes. Included in the standard library.
    - Datetime: A Python module to work with dates and times. Included in the standard library.
    - RE: A Python module for regular expressions. Included in the standard library.
    - OS: A Python module to interact with the operating system. Included in the standard library.  
  - ocrmypdf: A command-line tool to add OCR text layer to PDFs. Install it using your package manager (e.g., sudo apt-get install ocrmypdf).
  - pdftotext: A tool to extract text from PDF files. Install it using your package manager (e.g., sudo apt-get install poppler-utils).
  - rsync: A utility for efficiently transferring and synchronizing files. Install it using your package manager (e.g., sudo apt-get install rsync).
    
## How to build

![ArchiverArchitektur drawio](https://github.com/user-attachments/assets/cc479eea-7e1f-40cc-93f1-12152e71a94a)

### Setup shared network drive to collect scanned PDF documents
Ensure that the network drive is accessible and grant read and write access for the relevant users to it. The respective credentials will be needed by the document scanner as well as the user that will be executing Archivar.

### Setup document scanner
Follow the manufacturer's instructions to set up the scanner. Connect the scanner to the local network and to the shared network drive. Make sure that your scanner supports assigning two categories to your file and storing these as part of the filename (brother ADS-2800W supports this). Currently, Archivar expects the filename in the following format: 

`YYYYMMDDHHMMSS-[Category1]-[Category2]-[SeqNo].pdf`

### Setup document processing and storage
I am using an intermediate document storage as I do not want my processing and storage server to be on at all times or have to start it before I scan documents. This is pretty much an usability and stakeholder acceptance requirement. Although Archivar is a python script it is not platform independent (yet).

- install software dependencies as described above.
- decide where you want to place the script and the config file, e.g., `/usr/bin/local/archivar_30/` grant access to the executing user and make it executable.
- fill in all required information into config file.
- make sure that the user executing the script has read and write access to all relevant paths (intermediate input/ output storage, path to log-files, and final document storage).
- decide in which cadence Archivar should look for new files, you can do so by using crontab or making it an systemd.service

## how to use
Once configured Archivar will be executed directly e.g. `python /usr/bin/local/archivar_30/archivar_30.py` or you execute it continuously utilizing crontab or systemd.services.
Archivar will then ...
1. iterate through all PDF files in `sourcedir` specified in `archivar_30.cfg` config file
2. OCR the document, adding a text-layer.
3. search for a valid date on the first page of the document to find out the document's original date.
4. rename the document accordingly: `YYYYMMDD[o|x][SeqNo]-[Category1]-[Category2].pdf` [o|x] indicates if the date has been changed. o means that the date submitted by the scanner is used, x indicates that a new date has been identified in the document and has been used.
5. sync all documents to `destdir` specified in `archivar_30.cfg`, where [Category1] will be used as directory and [Category2] as subdirectory in which the document will be stored.
6. log all activities to `logdir` specified in `archivar_30cfg`.

## how to benefit
With all PDF documents being searchable now, I am using search and index tools.
Our family Windows-Laptop uses Lookeen, which is able to index network shares and offers full text search.
I am currently playing around with DocFetcher and Recoll as well.
After scanning the documents, they are immediately dropped in a cardboard archive box, one for each calendar year. In case I need the original it is rather easy to find again, in most cases it is sufficient to have the PDF at hand. In Germany the typical retention duration for documents is 10 years. Aftrr that time we shred most of the content of the respective archive box and only keep documents that we want to keep. The rest is still available as PDF.

