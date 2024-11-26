# Blake Williams HW7_Socket_Programming 

import socket

def start_client():
    host = '127.0.0.1'
    port = 64321

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Connected to the bank server.")
    while True:
        print("\nMenu:")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Exit")

        try:
            choice = input("Choose an option: ")
            if choice == '1':
                amount = input("Enter deposit amount: ")
                if amount.isdigit():
                    client_socket.send(f"deposit/{amount}".encode())
                else:
                    print("Error: Invalid input. Please enter a valid number.")
                    continue

            elif choice == '2':
                amount = input("Enter withdrawal amount: ")
                if amount.isdigit():
                    client_socket.send(f"withdraw/{amount}".encode())
                else:
                    print("Error: Invalid input. Please enter a valid number.")
                    continue

            elif choice == '3':
                client_socket.send("balance".encode())

            elif choice == '4':
                print("Exiting...")
                break

            else:
                print("Error: Invalid option.")
                continue

            # Receive server response
            response = client_socket.recv(1024).decode()
            print(f"Server: {response}")

        except Exception as e:
            print(f"Error: {str(e)}")
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
