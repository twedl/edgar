# EDGAR Python Data Pipeline

This project ingests, cleans, and organizes securities filings provided by the SEC. The SEC requires all companies to file reports and statements through their EDGAR (Electronic Data Gathering, Analysis, and Retrieval) system. The SEC provides programmatic access to their system up to 10 requests/second. For more information, see [Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data).

Related resources:

* [EDGAR Application Programming Interfaces](https://www.sec.gov/edgar/sec-api-documentation): SEC API that offers direct access to a specific company's information
* [submission zip file](https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip): contains the public EDGAR filing history for all filers--contains the filing info (e.g., form name and date), but not the filing itself.
* Company ticket / CIK / company name crosswalks (from the [Developers FAQ](https://www.sec.gov/os/webmaster-faq#developers): 
    - [ticket.txt](https://www.sec.gov/include/ticker.txt) tab delimited text file for ticker/CIK
    - [company_tickers.json](https://www.sec.gov/files/company_tickers.json): json file for ticker/CIK/name 
* [Financial Statement Data Sets](https://www.sec.gov/dera/data/financial-statement-data-sets.html): numeric information from the "face" (?) financials of all financial statements. There's also the [Financial Statement and Notes Data Sets](https://www.sec.gov/dera/data/financial-statement-and-notes-data-set.html), which has more info.
* [EDGAR Public Dissemination Subsystem Technical Specification](https://www.sec.gov/info/edgar/specifications/pds_dissemination_spec.pdf): provides file specifications for parsing the EDGAR submissions

Similar projects:

* [OpenEDGAR](https://github.com/LexPredict/openedgar): 
* [sec-data-parser](https://github.com/paulgb/sec-data-parser): a Rust parser for EDGAR SGML files

# Output

A data lake with unstructured and structured EDGAR data. 