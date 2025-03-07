import csv
import sys
from collections import defaultdict


# Mapping protocol names to their respective protocol numbers based on IANA standards
PROTOCOL_NAME_TO_NUMBER = {
    'icmp': 1,
    'igmp': 2,
    'tcp': 6,
    'udp': 17,
    'gre': 47,
    'esp': 50,
    'ah': 51,
    'sctp': 132
}

# Reverse mapping for lookup
PROTOCOL_NUMBER_TO_NAME = {v: k for k, v in PROTOCOL_NAME_TO_NUMBER.items()}

LOOKUP_TABLE_PATH = "./data/lookup_table.csv"
FLOW_LOGS_PATH = "./data/flow_logs.txt"
OUTPUT_FILE_PATH = "./output/output_results.txt"

def load_lookup_table(file_path):
    """
    - Reads the lookup table CSV file.
    - Extracts destination port, protocol, and tag information.
    - Maps (dstport, protocol_number) to corresponding tag.
    - Skips invalid or malformed entries.
    - Handles file not found or read errors.
    """
    lookup_table = {}
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    dst_port = int(row['dstport'])
                    protocol_name = row['protocol'].strip().lower()
                    tag = row['tag'].strip()
                    protocol_number = PROTOCOL_NAME_TO_NUMBER.get(protocol_name)
                    
                    if protocol_number is not None:
                        lookup_table[(dst_port, protocol_number)] = tag
                except (ValueError, KeyError):
                    continue  # Skip invalid entries
    except FileNotFoundError:
        print(f"Error: Lookup table file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading lookup table: {e}")
        sys.exit(1)
    
    return lookup_table

def analyze_flow_logs(file_path, lookup_table):
    """
    - Reads the flow log file line by line.
    - Extracts destination port and protocol number.
    - Maps protocol numbers to names using predefined mappings.
    - Counts occurrences of (port, protocol) pairs.
    - Matches logs against the lookup table to categorize traffic with tags.
    - Skips malformed lines and handles missing values gracefully.
    """
    tag_frequencies = defaultdict(int)
    port_protocol_frequencies = defaultdict(int)
    
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                fields = line.strip().split()
                if len(fields) < 14:
                    continue  # Skip malformed lines
                
                try:
                    dst_port = int(fields[6])  # Destination port from logs
                    protocol_number = int(fields[7])  # Protocol number from logs
                    
                    protocol_name = PROTOCOL_NUMBER_TO_NAME.get(protocol_number, str(protocol_number))
                    port_protocol_frequencies[(dst_port, protocol_name)] += 1
                    
                    tag = lookup_table.get((dst_port, protocol_number), 'Untagged')
                    tag_frequencies[tag] += 1
                except ValueError:
                    continue  # Skip lines with invalid numeric values
    except FileNotFoundError:
        print(f"Error: Flow logs file not found at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing flow logs: {e}")
        sys.exit(1)
    
    return tag_frequencies, port_protocol_frequencies

def write_output_to_file(tag_frequencies, port_protocol_frequencies, output_path):
    """
    - Writes aggregated statistics to an output file.
    - Saves tag count summary and port-protocol frequencies in a structured format.
    """
    try:
        with open(output_path, mode='w', encoding='utf-8') as file:
            file.write("Tag Frequencies:\n")
            file.write("Tag,Count\n")
            for tag, count in tag_frequencies.items():
                file.write(f"{tag},{count}\n")
            
            file.write("\nPort/Protocol Combination Frequencies:\n")
            file.write("Port,Protocol,Count\n")
            for (port, protocol), count in port_protocol_frequencies.items():
                file.write(f"{port},{protocol},{count}\n")
        print(f"Results written to {output_path}")
    except Exception as e:
        print(f"Error writing output to file: {e}")
        sys.exit(1)

def main():
    """
    - Orchestrates the execution of the script.
    - Loads the lookup table.
    - Processes flow logs and generates statistics.
    - Writes the results to an output file instead of printing.
    """
    lookup_table = load_lookup_table(LOOKUP_TABLE_PATH)
    tag_frequencies, port_protocol_frequencies = analyze_flow_logs(FLOW_LOGS_PATH, lookup_table)
    write_output_to_file(tag_frequencies, port_protocol_frequencies, OUTPUT_FILE_PATH)

if __name__ == "__main__":
    main()