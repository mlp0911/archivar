# Archivar
A Python script for automated PDF processing, including OCR and archiving, to streamline document management.

## Overview
Archivar is a document management tool designed to streamline the process of handling physical correspondence. By leveraging a document scanner with an automatic feeder, Archivar enables efficient scanning, categorization, and OCR processing of large volumes of documents. The scanned PDFs are named according to a defined convention, including the scan date, categories (e.g., household/bills), and a sequential number. The system integrates with a local network and a document server (Debian 12) to facilitate organized storage and easy retrieval.

## Motivation
Managing vast amounts of physical correspondence was a tedious and time-consuming task, requiring manual filing and hole-punching. This process made it difficult to locate specific documents when needed, such as for tax purposes.
To address this issue, I purchased a Brother ADS-2800W document scanner with an automatic feeder, allowing for efficient scanning and two-step categorization (e.g., household/bills). The scanner produced PDFs with a defined filename format, including the scan date, categories, and a sequential number. These scans were stored on a network drive, accessible by a client that is always on and collects the scans. The original documents are filed in cardboard archive boxes and most of them thrown away after ten years.

Archivar takes over when the document server is on, categorizing the files, applying OCR, adding a text layer, identifying the date of the correspondence, adjusting the filename, and moving the file to the appropriate storage location on the document server. All files can now be searched with respective indexing and search tools like DocFetcher or Lookeen. This solution has significantly reduced the time and effort required for managing physical correspondence, improving organization and retrieval efficiency.

## Dependencies
Ensure you have the following dependencies installed and configured before proceeding with the installation and setup:

- Automatic document scanner, that allows for two staged categorization, configurable filenames and storage on local network shares. Or any other solution to populate the input directory with PDF files providing the required information.
- Network Drive on always-on client to store scanned documents.
  
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

    Install the Document Scanner

        Follow the manufacturer's instructions to set up the Brother ADS-2800W scanner.

        Connect the scanner to the local network.

    Set Up Network Drive

        Ensure the network drive is accessible on the always-on client.

        Create a directory on the network drive to store scanned documents.

    Configure the Document Scanner

        Set up the scanner to save scanned PDFs directly to the network drive.

        Define the filename convention to include the scan date, categories, and a sequential number.

    Install Debian 12 on Document Server

        Download and install Debian 12 on your document server.

        Ensure the server can access the network drive.

    Install Required Software Dependencies
    
