# Archivar
A Python script for automated PDF processing, including OCR and archiving, to streamline document management.

## Overview
Archivar is a document management tool designed to streamline the process of handling physical correspondence. By leveraging a document scanner with an automatic feeder, Archivar enables efficient scanning, categorization, and OCR processing of large volumes of documents. The scanned PDFs are named according to a defined convention, including the scan date, categories (e.g., household/bills), and a sequential number. The system integrates with a local network and a document server (Debian 12) to facilitate organized storage and easy retrieval.

## Motivation
Managing vast amounts of physical correspondence was a tedious and time-consuming task, requiring manual filing and hole-punching. This process made it difficult to locate specific documents when needed, such as for tax purposes.
To address this issue, I purchased a Brother ADS-2800W document scanner with an automatic feeder, allowing for efficient scanning and two-step categorization (e.g., household/bills). The scanner produced PDFs with a defined filename format, including the scan date, categories, and a sequential number. These scans were stored on a network drive, accessible by a client that is always on and collects the scans. The original documents are filed in cardboard archive boxes and most of them thrown away after ten years.

Archivar takes over when the document server is on, categorizing the files, applying OCR, adding a text layer, identifying the date of the correspondence, adjusting the filename, and moving the file to the appropriate storage location on the document server. All files can now be searched with respective indexing and search tools like DocFetcher or Lookeen. This solution has significantly reduced the time and effort required for managing physical correspondence, improving organization and retrieval efficiency.

