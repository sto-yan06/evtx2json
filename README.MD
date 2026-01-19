# EVTX to JSON Converter (Robust CLI Tool)

A high-performance, reliable Command Line Interface (CLI) tool designed to convert Windows Event Log (** .evtx **) files into **JSON** format. 

Unlike standard converters, this tool is built for **Digital Forensics and Incident Response (DFIR)**. It is specifically engineered to handle corrupted records, malformed XML, and the notorious `utf-16-le` encoding errors that often crash other parsers.

## Key Features
* **XML Sanitization:** Automatically strips illegal control characters and null bytes that break standard XML parsers.
* **Memory Efficient:** Uses a generator-based approach to process massive "Security" or "System" logs without exhausting RAM.
* **Fault Tolerant:** Skips individual corrupted records while ensuring the rest of the file is successfully converted.
* **Analysis Ready:** Converts Windows timestamps into standardized ISO 8601 strings.

## Prerequisites

Before running the script, ensure you have **Python 3.8+** installed.

### Required Libraries:
You must install the following dependencies:

1.  **`python-evtx`**: For parsing the binary structure of `.evtx` files.
2.  **`xmltodict`**: For converting sanitized XML data into clean Python dictionaries (JSON compatible).

---

## Installation

Clone the repository and install the dependencies using `pip`:

```bash
# Clone the repository
git clone [https://github.com/yourusername/evtx-to-json.git](https://github.com/yourusername/evtx-to-json.git)
cd evtx-to-json

# Install dependencies
pip install -r requirements.txt

```
## Usage

1. Save to a JSON file

```bash
python convert.py System.evtx -o system_logs.json

```

2. Stream to Terminal

```bash
python convert.py Security.evtx
```

## Troubleshooting

Handling Encoding & "Not Well-Formed" Errors
Windows logs frequently contain non-printable characters or "junk" data in the binary stream. If you see messages like Skipping a record due to encoding error, it means the script has successfully isolated a corrupted event and moved on to the next one to protect the integrity of your total output. 