# OSINT_Ports
OSINT_Ports- Open Source Intelligence Tool for gathering information about publicly accessible IPv4 Hosts of an organization or a subnet.  

# Synopsis
Passive Reconnaissance is one of the most powerful and underestimated methods of knowing the target. This tool uses "Censys API" to query the Censys search engine. User can either input the name of an organization (Known Keyword), a subnet or both.    
The programs prints the IP addresses, location and the open ports of the hosts that belong to the organization or reside in the subnet input. The program also allows user to store the results in a database which can be used later for further research. The program confirms the ownership of an host by verifying the certificates or the AS (autonomous system) names.
https://censys.io/about
https://censys.io/data 

# Motivation
Active port scan usually creates a lot of noise, might get you blocked, alert the target or trigger an IDS. Basically why do the hardwork (port scanning) when somebody (censys.io) has already done it for you?  

# Installation Requirements:
Python3
Install "Censys" module: "pip install censys" https://censys.io/api
Install "Pandas" module: "pip install pandas"
Install "sqlite3" module: "pip install sqlite3"
Get the API Keys
Edit the Program/Enter API keys
RUN!

# API Reference:
Follow instructions on https://censys.io/api

# Tests:
root@kali:~/Desktop/Recon_ports# ./reconports.py 
 
Choose the Input:
1. Organization name
2. A subnet/IP
3. Organization name AND a subnet
4. Store in a database
5. Print exsiting Database
6. Select from exsiting Database [sqlquery]
Select(1/2/3/4/5/6): 


# Disclaimer:
The tool is intended for educational purposes only. I do not assume any responsibility for the tool. Use this material at your own discretion and with proper authorization. 




