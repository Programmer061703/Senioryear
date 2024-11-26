//Blake Williams Socket Programming Read Me

To run program 
1. Put both client.py and server.py onto the turing server 
	- For organization place them in their own directory 
2. Open 2 terminal sessions and ssh into the turing server 
3. Navigate to the created directory containing the client.py and server.py on both terminals
4. On one of the terminals type "python3 server.py" to start the server 
5. Now on the other terminal type "python3 client.py" to start the client
6. A list of 4 options will appear 
	- Deposit Money
	- Withdraw Money
	- Check Balance 
	- Exit
7. Press 1,2,3,or 4 to select the above options 
8. For Deposit money and withdraw money, the client program will ask you to input an amount you would like to deposit/withdraw
	- Only input numeric values
	- If you input a larger value to withdraw than what is currently in the bank, an error will appear. 
9. When finished press 4 on the menu to exit both the client and server programs
10. If two client sessions are open and connected to the server, only one will be able to interact with the server (Priority Client)
	- When the priority client is closed then the next client becomes the priority client, and is able to interact with the bank balance on the server
