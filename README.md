# EDGAR Python Data Pipeline

This project ingests, cleans, and organizes securities filings provided by the SEC. The SEC requires all companies to file reports and statements through their EDGAR (Electronic Data Gathering, Analysis, and Retrieval) system. The SEC provides programmatic access to their system up to 10 requests/second. For more information, see [Accessing EDGAR Data](https://www.sec.gov/os/accessing-edgar-data).

There is also an SEC API that offers direct access to a specific company's information; see [EDGAR Application Programming Interfaces](https://www.sec.gov/edgar/sec-api-documentation). There is also a [submission zip file](https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip) that contains the public EDGAR filing history for all filers--that contains the filing info (e.g., form name and date), but not the filing itself).

# Output

A data lake with unstructured and structured EDGAR data. 