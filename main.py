import socket
import threading


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


if __name__ == '__main__':
    # Example usage: binds to 0.0.0.0:1194 and forwards to 8.8.8.8:53 (DNS)
    # This is a basic TCP proxy and does not provide encryption or tunneling features
    start_vpn(ye
