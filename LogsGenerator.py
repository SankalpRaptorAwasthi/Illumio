#Testing the log with mass Logs enteries 

import random
import time

def create_random_ip():
    """Generates a random IPv4 address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_flow_log_entry():
    """
    - Generates a single flow log entry with random network traffic data.
    - Includes source/destination IPs, ports, protocol, packet details, timestamps, and action.
    """
    flow_log_components = {
        "version": '2',
        "account_id": '123456789012',
        "eni_id": 'eni-0a1b2c3d',
        "srcaddr": create_random_ip(),
        "dstaddr": create_random_ip(),
        "srcport": str(random.randint(1, 65535)),
        "dstport": str(random.randint(1, 65535)),
        "protocol": str(random.choice([1, 6, 17])),  # ICMP, TCP, UDP
        "packets": str(random.randint(1, 10000)),
        "bytes_sent": str(random.randint(1, 1000000)),
        "start_time": str(int(time.time()) - random.randint(0, 10000)),
        "end_time": str(int(time.time())),
        "action": random.choice(['ACCEPT', 'REJECT']),
        "log_status": 'OK'
    }
    return " ".join(flow_log_components.values()) + "\n"

def generate_flow_log_file(output_path, file_size_mb):
    """
    - Creates a flow log file with random log entries.
    - Writes until the file reaches the specified size (MB).
    """
    target_size_bytes = file_size_mb * 1024 * 1024
    try:
        with open(output_path, mode='w', encoding='utf-8') as file:
            while file.tell() < target_size_bytes:
                file.write(generate_flow_log_entry())
        print(f"Flow log file generated successfully at {output_path}")
    except Exception as e:
        print(f"Error writing flow log file: {e}")

if __name__ == "__main__":
    LOG_FILE_PATH = "./testingLogs/flow_logs_gen.txt"
    FILE_SIZE_MB = 10
    generate_flow_log_file(LOG_FILE_PATH, FILE_SIZE_MB)