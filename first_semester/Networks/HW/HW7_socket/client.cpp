#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <unordered_map>
#include <fstream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <cerrno>
#include <cstring>
#include <string>
#include <stdio.h>
#include <limits.h>
//Bind server receive port 7501 do not bind 7500 broadcast but still create it
//127.0.0.1

const int PORT = 7501;
const int BROADCAST_PORT = 7500;
const int BUFFER_SIZE = 1024;
int shooterID, killedID, tempShooter;
const char* responseMessage = "Default response";
const char* ip = "127.0.0.1";

std::string redBase = "53";
std::string greenBase = "43";


void printMapContents(const std::unordered_map<int, std::string>& map) {
    for (const auto& pair : map) {
        std::cout << "Machine ID: " << pair.first << ", Player ID: " << pair.second << std::endl;
    }
}

int pipeInsert(const std::string& shooterCodename, const std::string& killedCodename, char* pipePath) {
    //const char* pipePath = "pipe";
    int fd = open(pipePath, O_WRONLY | O_NONBLOCK);
    if (fd == -1) {
        std::cerr << "Error opening pipe: " << std::strerror(errno) << std::endl;
        return 1; // Failure
    }

    // Format the message with codenames instead of IDs
    std::string message = shooterCodename + ":" + killedCodename + "\n";
    ssize_t bytesWritten = write(fd, message.c_str(), message.length());
    if (bytesWritten == -1) {
        std::cerr << "Error writing to pipe: " << std::strerror(errno) << std::endl;
        close(fd);
        return 1;
    }

    close(fd);
    return 0;
}







int main() {
    const char* pipe = new char[5]; //For concatenation later
    pipe = "/udp/pipe"; 
    char  pathBuffer[PATH_MAX];
    //Get the current dir and store in buffer
    if (getcwd(pathBuffer, sizeof(pathBuffer)) != NULL) {
        printf("Current working directory : %s\n", pathBuffer);
    } else {
        perror("getcwd() error");
    }
    char temp[64];
    //Calculate total length of final concatenated path, plus one for null terminator :)
    int total_length = strlen(pathBuffer) + strlen(pipe) + 1;
    //Allocate the memory
    char* pipePath = new char[total_length];
    //Copy the current working directory
    strcpy(pipePath, pathBuffer);
    //Append "pipe"
    strcat(pipePath, pipe);
    //Free the allocated memory
    // delete[] pipe;
    // delete[] pathBuffer;
    //Print the result
    std::cout << "Pipe path is: " << pipePath <<std::endl;

    int socketFD = socket(AF_INET, SOCK_DGRAM, 0);
    if (socketFD == -1) {
        std::cerr << "Error creating socket" << std::endl;
        return 1;
    }

    //Enables Broadcasting
    int broadcastEnable=1;
    if(setsockopt(socketFD, SOL_SOCKET, SO_BROADCAST, &broadcastEnable, sizeof(broadcastEnable)) == -1){
        std::cerr << "Error setting socket to broadcast" << std::endl;
        close(socketFD);
        return 1;
    }

    struct sockaddr_in serverAddress;
    memset(&serverAddress, 0, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    serverAddress.sin_addr.s_addr = INADDR_ANY;
    serverAddress.sin_port = htons(PORT);

    if (bind(socketFD, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) == -1) {
        std::cerr << "Error binding socket" << std::endl;
        close(socketFD);
        return 1;
    }

    std::cout << "UDP Server is listening on port " << PORT << std::endl;

    std::unordered_map<int, std::string> machineToPlayerMap;


    char buffer[BUFFER_SIZE];
    while (true) {
        struct sockaddr_in clientAddress;
        socklen_t clientAddrLen = sizeof(clientAddress);
        ssize_t receivedBytes = recvfrom(socketFD, buffer, BUFFER_SIZE, 0, (struct sockaddr*)&clientAddress, &clientAddrLen);
        if (receivedBytes == -1) {
            std::cerr << "Error receiving data" << std::endl;
            continue;
        }

        buffer[receivedBytes] = '\0'; // Null-terminate the received data
        std::cout << "Received: " << buffer << std::endl;

        // Respond based on the received message
        
        if (strcmp(buffer, "202") == 0) {
            struct sockaddr_in broadcastAddress;
            memset(&broadcastAddress, 0, sizeof(broadcastAddress));
            broadcastAddress.sin_family = AF_INET;
            broadcastAddress.sin_port = htons(BROADCAST_PORT);
            broadcastAddress.sin_addr.s_addr = inet_addr(ip);

            sendto(socketFD, buffer, strlen(buffer), 0, (struct sockaddr*)&broadcastAddress, sizeof(broadcastAddress));
            
        } else if (strcmp(buffer, "221") == 0) {
            struct sockaddr_in broadcastAddress;
            memset(&broadcastAddress, 0, sizeof(broadcastAddress));
            broadcastAddress.sin_family = AF_INET;
            broadcastAddress.sin_port = htons(BROADCAST_PORT);
            broadcastAddress.sin_addr.s_addr = inet_addr(ip);

            sendto(socketFD, buffer, strlen(buffer), 0, (struct sockaddr*)&broadcastAddress, sizeof(broadcastAddress));
        }
        else if (strncmp(buffer, "Hardware/", 9) == 0) {
           
             int machineID;
            char playerCodenameBuffer[128]; // Make sure the buffer is large enough for the codename
            sscanf(buffer, "Hardware/%d/%s", &machineID, playerCodenameBuffer);
            std::string playerCodename(playerCodenameBuffer);
            machineToPlayerMap[machineID] = playerCodename;
            printMapContents(machineToPlayerMap);
            



            // std::string playerCodename;
            // sscanf(buffer, "Hardware/%d/%s", &machineID, &playerCodename);
            // machineToPlayerMap[machineID] = playerCodename; 
            // printMapContents(machineToPlayerMap); 
            
         

            // Broadcast the ID to all clients right now it only echos back to the client
            struct sockaddr_in broadcastAddress;
            memset(&broadcastAddress, 0, sizeof(broadcastAddress));
            broadcastAddress.sin_family = AF_INET;
            broadcastAddress.sin_port = htons(BROADCAST_PORT);
            broadcastAddress.sin_addr.s_addr = inet_addr(ip);

            //Converts machineID to a char so it can be broadcasted
            char idBuffer[32];
            snprintf(idBuffer, sizeof(idBuffer),"%d",machineID);


            sendto(socketFD, idBuffer, strlen(idBuffer), 0, (struct sockaddr*)&broadcastAddress, sizeof(broadcastAddress));
        } 

        // Else-if block to handle "id/id" format
        else if (sscanf(buffer, "%d:%d", &shooterID, &killedID) == 2) {
            auto shooterEntry = machineToPlayerMap.find(shooterID);
            
            sprintf(temp, "%d", killedID);
            std::cout << killedID << std::endl;
            

            if (killedID == 53 || killedID == 43){
            std::string& playerShooterCodename = shooterEntry->second;
            pipeInsert(playerShooterCodename,std::to_string(killedID),pipePath);

            }
            else if((killedID%2 == 1 && shooterID%2 == 1)){
                struct sockaddr_in broadcastAddress;
                memset(&broadcastAddress, 0, sizeof(broadcastAddress));
                broadcastAddress.sin_family = AF_INET;
                broadcastAddress.sin_port = htons(BROADCAST_PORT);
                broadcastAddress.sin_addr.s_addr = inet_addr(ip);

                std::string message = "TeamR";
                auto shooterEntry = machineToPlayerMap.find(shooterID);
                std::string& playerShooterCodename = shooterEntry->second;
                pipeInsert(playerShooterCodename,message,pipePath);
                sendto(socketFD, temp, strlen(temp), 0, (struct sockaddr*)&clientAddress, clientAddrLen);
            }
            else if((killedID%2==0 && shooterID%2==0)){
                struct sockaddr_in broadcastAddress;
                memset(&broadcastAddress, 0, sizeof(broadcastAddress));
                broadcastAddress.sin_family = AF_INET;
                broadcastAddress.sin_port = htons(BROADCAST_PORT);
                broadcastAddress.sin_addr.s_addr = inet_addr(ip);

                std::string message = "TeamG";
                auto shooterEntry = machineToPlayerMap.find(shooterID);
                std::string& playerShooterCodename = shooterEntry->second;
                pipeInsert(playerShooterCodename,message,pipePath);
                sendto(socketFD, temp, strlen(temp), 0, (struct sockaddr*)&clientAddress, clientAddrLen);
            }
        
        auto killedEntry = machineToPlayerMap.find(killedID);
    if (shooterEntry != machineToPlayerMap.end() && killedEntry != machineToPlayerMap.end()) {
                struct sockaddr_in broadcastAddress;
                memset(&broadcastAddress, 0, sizeof(broadcastAddress));
                broadcastAddress.sin_family = AF_INET;
                broadcastAddress.sin_port = htons(BROADCAST_PORT);
                broadcastAddress.sin_addr.s_addr = inet_addr(ip);
                
        // Found both shooter's and killed's player codenames in the map
         std::string& playerShooterCodename = shooterEntry->second;
         std::string& playerKilledCodename = killedEntry->second;
        std::cout << "Shooter Player Codename: " << playerShooterCodename << ", Killed Player Codename: " << playerKilledCodename << std::endl;
        
        

            pipeInsert(playerShooterCodename, playerKilledCodename, pipePath);
            sendto(socketFD, temp, strlen(temp), 0, (struct sockaddr*)&clientAddress, clientAddrLen);
        
        
        
    } else {
        if (shooterEntry == machineToPlayerMap.end()) {
            std::cerr << "Shooter machine ID " << shooterID << " not found in player map." << std::endl;
        }
        if (killedEntry == machineToPlayerMap.end()) {
            std::cerr << "Killed machine ID " << killedID << " not found in player map." << std::endl;
        }
    }

    

}

else if (strcmp(buffer, "Clean")==0){

    machineToPlayerMap.clear();  // Clears the unordered_map of all elements
    std::cout << "All entries cleared from the map." << std::endl;

}
else if (strcmp(buffer, "Response")==0){
            struct sockaddr_in broadcastAddress;
            memset(&broadcastAddress, 0, sizeof(broadcastAddress));
            broadcastAddress.sin_family = AF_INET;
            broadcastAddress.sin_port = htons(BROADCAST_PORT);
            broadcastAddress.sin_addr.s_addr = inet_addr(ip);

            sendto(socketFD, temp, strlen(temp), 0, (struct sockaddr*)&broadcastAddress, sizeof(broadcastAddress));

}



        sendto(socketFD, responseMessage, strlen(responseMessage), 0, (struct sockaddr*)&clientAddress, clientAddrLen);

    }

    close(socketFD);
    return 0;
}