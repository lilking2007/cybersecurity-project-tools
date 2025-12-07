import socket
import time
import random
import datetime

HOST = 'localhost'
PORT = 5000

# Sample data
PROGRAMS = ["sshd", "kernel", "sudo", "nginx"]
HOSTS = ["web-server-01", "db-server-01", "firewall-edge"]
MESSAGES = [
    "Failed password for invalid user admin from 192.168.1.105 port 22 ssh2",
    "Accepted password for root from 10.0.0.5 port 22 ssh2",
    "Connection closed by 192.168.1.100 port 443",
    "Segfault at 0 ip 0000000000000000 sp 00007ffcc89c9e80 error 14 in libc-2.31.so",
    "pam_unix(sudo:session): session opened for user root by (uid=0)"
]

def generate_syslog():
    timestamp = datetime.datetime.now().strftime("%b %d %H:%M:%S")
    hostname = random.choice(HOSTS)
    program = random.choice(PROGRAMS)
    pid = random.randint(1000, 9999)
    message = random.choice(MESSAGES)
    
    # Construct syslog message
    # Format: <PRI>Timestamp Hostname Program[PID]: Message
    # PRI is often <13> or similar but Logstash grok in main.conf expects standard text format:
    # "MMM  d HH:mm:ss" Hostname Program[PID]: Message
    
    log_line = f"{timestamp} {hostname} {program}[{pid}]: {message}"
    return log_line

def send_logs():
    print(f"Sending logs to TCP {HOST}:{PORT} (Ctrl+C to stop)...")
    try:
        while True:
            log = generate_syslog()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((HOST, PORT))
                sock.sendall((log + "\n").encode('utf-8'))
                sock.close()
                print(f"Sent: {log}")
            except ConnectionRefusedError:
                print("Connection refused. Is Logstash running?")
            
            time.sleep(random.uniform(0.5, 2.0))
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    send_logs()
