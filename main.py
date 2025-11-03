import socket
import threading
import argparse

# Mapping of US state abbreviations to VPN server addresses
STATE_SERVERS = {
    'AL': 'us-al.server.example.com',
    'AK': 'us-ak.server.example.com',
    'AZ': 'us-az.server.example.com',
    'AR': 'us-ar.server.example.com',
    'CA': 'us-ca.server.example.com',
    'CO': 'us-co.server.example.com',
    'CT': 'us-ct.server.example.com',
    'DE': 'us-de.server.example.com',
    'FL': 'us-fl.server.example.com',
    'GA': 'us-ga.server.example.com',
    'HI': 'us-hi.server.example.com',
    'ID': 'us-id.server.example.com',
    'IL': 'us-il.server.example.com',
    'IN': 'us-in.server.example.com',
    'IA': 'us-ia.server.example.com',
    'KS': 'us-ks.server.example.com',
    'KY': 'us-ky.server.example.com',
    'LA': 'us-la.server.example.com',
    'ME': 'us-me.server.example.com',
    'MD': 'us-md.server.example.com',
    'MA': 'us-ma.server.example.com',
    'MI': 'us-mi.server.example.com',
    'MN': 'us-mn.server.example.com',
    'MS': 'us-ms.server.example.com',
    'MO': 'us-mo.server.example.com',
    'MT': 'us-mt.server.example.com',
    'NE': 'us-ne.server.example.com',
    'NV': 'us-nv.server.example.com',
    'NH': 'us-nh.server.example.com',
    'NJ': 'us-nj.server.example.com',
    'NM': 'us-nm.server.example.com',
    'NY': 'us-ny.server.example.com',
    'NC': 'us-nc.server.example.com',
    'ND': 'us-nd.server.example.com',
    'OH': 'us-oh.server.example.com',
    'OK': 'us-ok.server.example.com',
    'OR': 'us-or.server.example.com',
    'PA': 'us-pa.server.example.com',
    'RI': 'us-ri.server.example.com',
    'SC': 'us-sc.server.example.com',
    'SD': 'us-sd.server.example.com',
    'TN': 'us-tn.server.example.com',
    'TX': 'us-tx.server.example.com',
    'UT': 'us-ut.server.example.com',
    'VT': 'us-vt.server.example.com',
    'VA': 'us-va.server.example.com',
    'WA': 'us-wa.server.example.com',
    'WV': 'us-wv.server.example.com',
    'WI': 'us-wi.server.example.com',
    'WY': 'us-wy.server.example.com',
}


def handle_client(client_socket, remote_host, remote_port):
    """Forward traffic between client and remote host."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_socket:
        remote_socket.connect((remote_host, remote_port))
        def forward(src, dst):
            while True:
                data = src.recv(4096)
                if not data:
                    break
                dst.sendall(data)
        # Start forwarding in both directions
        t1 = threading.Thread(target=forward, args=(client_socket, remote_socket))
        t2 = threading.Thread(target=forward, args=(remote_socket, client_socket))
        t1.start()
        t2.start()
        t1.join()
        t2.join()


def start_vpn(bind_host='0.0.0.0', bind_port=1194, remote_host='8.8.8.8', remote_port=53):
    """Start a simple TCP forwarder (not secure VPN)."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((bind_host, bind_port))
        server.listen(5)
        print(f'Football VPN listening on {bind_host}:{bind_port} and forwarding to {remote_host}:{remote_port}')
        while True:
            client, addr = server.accept()
            threading.Thread(target=handle_client, args=(client, remote_host, remote_port)).start()


def main():
    parser = argparse.ArgumentParser(description='Football VPN - Connect within U.S. states')
    parser.add_argument('--state', required=True, help='Two-letter US state abbreviation')
    parser.add_argument('--bind-port', type=int, default=1194, help='Local port to bind on')
    parser.add_argument('--remote-port', type=int, default=53, help='Remote port to forward to')
    args = parser.parse_args()
    state = args.state.upper()
    if state not in STATE_SERVERS:
        print(f"Error: invalid state {state}. Please provide a valid two-letter US state abbreviation.")
        return
    remote_host = STATE_SERVERS[state]
    start_vpn(bind_port=args.bind_port, remote_host=remote_host, remote_port=args.remote_port)


if __name__ == '__main__':
    main()
