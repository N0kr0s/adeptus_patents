# Adeptus Patents

A parser and data processing tool for patent data from Google Patents.

> **RTU MIREA introductory practice project**  
> Practical assignment completed as part of the introductory internship at RTU MIREA.  
> Study program: **AI Technologies and Data Analysis**.

---

## About

The project is designed to automatically collect additional information about patents and build a structured CSV dataset.

The input is a CSV file containing basic patent information. For each patent, the program opens its Google Patents page, extracts additional data, and combines it with the original record.

The main idea is to turn a basic list of patents into a more detailed dataset that can be used for further analysis and processing.

---

## How It Works

The application consists of several main stages.

### Data Preparation

`data_processing.py` reads the source CSV, filters invalid records, and creates the dataset that will be processed.

The number of patents can be configured without changing the source code.

### Patent Parsing

`parser.py` downloads patent pages using `Requests` and parses their HTML with `BeautifulSoup`.

The parser extracts:

- abstract;

- description;

- claims;

- images;

- classifications;

- inventors;

- patent status;

- patent citation count;

- citation count;

- priority application count.

The extracted information is stored in a `PatentDocument` object.

### Dataset Processing

`csv_patents.py` combines the original patent information with the data collected by the parser and creates the final CSV dataset.

---

## Parallel Processing

Processing thousands of web pages sequentially can take a significant amount of time.

The project uses Python's `ThreadPoolExecutor` to process multiple patents simultaneously.

The number of concurrent requests can be configured:

```env
MAX_WORKERS=10
```

For example:

```env
MAX_WORKERS=20
```

allows up to 20 patents to be processed at the same time.

---

## Error Handling

HTTP requests use a configurable timeout and retry mechanism.

```env
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

If a request fails, the parser can retry it before marking the patent as failed.

This helps handle temporary network problems without stopping the entire processing pipeline.

---

## Saving Progress

The results are periodically saved to the output CSV file.

```env
SAVE_EVERY=1000
```

This prevents losing already processed data if the program is interrupted.

The application also checks the existing output file when started again and skips patents that have already been processed.

---

## Configuration

The main processing parameters are configured through `.env`:

```env
SOURCE_CSV_PATH=data/gp.csv
DATASET_PATH=data/patents.csv
OUT_CSV_PATH=data/patents(1).csv

MAX_ROWS_VALUE=5000

MAX_WORKERS=10
SAVE_EVERY=1000

REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

This allows the processing behavior to be changed without modifying the source code.

---

## Output

The resulting CSV contains the original patent information together with the additional data extracted from Google Patents:

```text
id
title
assignee
inventor/author
priority date
filing/creation date
publication date
grant date
url
abstract
images
classifications
description
claims
status
inventor
patent_citation_number
cited_number
priority_applications_number
```

---

## Technologies

- Python

- Pandas

- Requests

- BeautifulSoup

- python-dotenv

- ThreadPoolExecutor

---

## Project Structure

```text
adeptus_patents/
├── src/
│   ├── config.py
│   ├── csv_patents.py
│   ├── data_downloading.py
│   ├── data_processing.py
│   ├── parser.py
│   └── patent.py
├── main.py
├── requirements.txt
└── README.md
```

---

## Academic Project

This project was developed as part of an **introductory practice at RTU MIREA**.

**RTU MIREA introductory practice project**
