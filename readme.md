
# Flow Log Computer Assessment

## Description

This project is a Python-based flow log analyzer that processes network flow logs and maps each entry to a tag based on a predefined lookup table. The script generates structured output with two key reports:

1. **Tag Frequencies**: The count of occurrences for each tag.

2. **Port/Protocol Combination Frequencies**: The count of occurrences for each unique (port, protocol) pair.

The script ensures efficiency and accuracy in analyzing extensive network traffic data while handling edge cases such as malformed log entries.

## Features

Efficient Flow Log Parsing: Reads large network logs and extracts relevant fields.

Protocol Mapping Based on IANA Standards: Supports an extensive list of protocols including TCP, UDP, ICMP, IGMP, GRE, ESP, AH, and SCTP.

Automated Categorization: Maps flow logs to tags using a CSV-based lookup table.

Robust Error Handling: Skips malformed entries, ensuring resilience against unexpected data.

Customizable Output: Writes structured analysis results to an output file.

Scalability: Optimized to process large log files efficiently.

## Requirements

Python 3.xx

## Assumptions

### Field Order in Flow Logs
The flow log entries are expected to follow a specific format:

```plaintext
version account-id interface-id srcaddr dstaddr dstport srcport protocol packets bytes start end action log-status
```

- The parser assumes this order when extracting fields.
- Malformed entries (less than 14 fields) are automatically skipped.


### Protocol Mapping
The script supports multiple protocols based on IANA standards:

| Protocol Name | Number |
|--------------:|:------:|
| ICMP         |   1    |
| IGMP         |   2    |
| TCP          |   6    |
| UDP          |  17    |
| GRE          |  47    |
| ESP          |  50    |
| AH           |  51    |
| SCTP         | 132    |

- Protocols are mapped in a case-insensitive manner.
- Unrecognized protocol numbers are preserved as-is in the results.
## Data Handling & Edge Cases
- Malformed Entries: Any log entry with fewer than 14 fields is ignored.
- Unknown Protocols: Logs with unknown protocol numbers retain the numerical protocol representation.
- Large Log Files: Successfully tested on log files up to 10 MB and lookup tables with up to 10,000 entries.

## Installation & Setup

Clone the Repository (Optional)

```plaintext
git clone <repository_url>
cd ASSESSMENT
python LogsParser.py
```

## Usage

Step 1: Prepare Input Files
```plaintext
Place your flow_logs.txt and lookup_table.csv files inside the data/ directory.
```
Step 2: Run the Log Parser

```plaintext
python LogsParser.py
```
- This script will process the flow logs and generate the analysis output.

- The results will be saved in output/output_results.txt.

Step 3: Check the Output

```plaintext
Open output/output_results.txt to view the structured report.
```
- Testing with Synthetic Logs

If you want to generate test logs, run the log generator script:
```plaintext
python LogsGenerator.py
```
- The generated logs will be stored in testingLogs/flow_logs_gen.txt.

- You can replace data/flow_logs.txt with this file for testing purposes.

## Testing & Performance Analysis

### Tests Conducted

- Extensive Dataset Testing: Evaluated on large log files (~10MB) with various structured and unstructured data.

- Malformed Log Entry Handling: Verified the script correctly skips logs with fewer than 14 fields.

- Protocol Recognition: Checked protocol number-to-name mapping using IANA standards.

- Edge Case Handling: Tested behavior with unknown protocols, missing ports, and partial logs.

- Performance Benchmarking: Ensured efficient execution with large datasets.

### Limitations

- Log Format: Only supports the predefined log format; does not handle custom formats.

- Protocol Mapping: While most common protocols are mapped, unrecognized protocols are logged as numbers.

- Data Size Constraints: Optimized for ~10MB log files and ~10,000 lookup table entries.

### Additional Notes

- Case Insensitivity: Protocol and tag lookups are case-insensitive.

- Data Size Handling: Designed to efficiently process large logs while skipping malformed entries.

- Log Generator: Use flow_log_generator.py to create synthetic logs for testing.