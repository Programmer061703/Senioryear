# Blake Williams HW7_Socket_Programming
import socket

# Initial balance
balance = 100

def handle_client(conn, addr):
    global balance
    print(f"Connected by {addr}")
    print("--------------------------------------")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Client {addr} disconnected.")
                print("--------------------------------------")
                break

            # Process client message
            if data.startswith("deposit/"):
                amount = data.split('/')[1]
                if amount.isdigit():
                    balance += int(amount)
                    print(f"Received deposit request for ${amount}.")
                    print("--------------------------------------")
                    conn.send(f"Deposit successful. New balance: ${balance}".encode())
                else:
                    print("Error: Invalid deposit amount received.")
                    conn.send("Error: Invalid deposit amount.".encode())

            elif data.startswith("withdraw/"):
                amount = data.split('/')[1]
                if amount.isdigit():
                    amount = int(amount)
                    if amount <= balance:
                        balance -= amount
                        print(f"Received withdrawal request for ${amount}.")
                        print("--------------------------------------")
                        conn.send(f"Withdrawal successful. New balance: ${balance}".encode())
                    else:
                        print("Error: Withdraw Request more than balance.")
                        print("--------------------------------------")
                        conn.send("Error: Insufficient funds.".encode())
                else:
                    conn.send("Error: Invalid withdrawal amount.".encode())

            elif data == "balance":
                print("Received balance check request.")
                print("--------------------------------------")
                conn.send(f"Current balance: ${balance}".encode())

            else:
                conn.send("Error: Invalid command.".encode())

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def start_server():
    host = '127.0.0.1'
    port = 64321

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is running and waiting for connections...")
    print("--------------------------------------")
    while True:
        conn, addr = server_socket.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    start_server()

