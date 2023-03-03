# Cisco & Huawei Telnet & SSH via LDAP

This Python script enables you to connect to a CPE via Telnet and SSH, regardless of whether it is Huawei or Cisco, by determining the appropriate commands to be sent according to the CPE.

The script also works with LDAP to authenticate the user, and based on the connection method (Telnet or SSH), it sends the necessary commands to the CPE.

The following libraries are used in this script:

- sys
- paramiko
- paramiko_expect
- telnetlib
- queue
- threading

# Installation

1. Make sure that you have Python installed on your machine. If you don't have Python, you can download it from the official website.

2. Download the script and save it to your preferred location.

3. Install the necessary libraries:

paramiko

paramiko_expect

You can install these libraries via pip. Open your terminal or command prompt and enter the following commands:

pip install paramiko

pip install paramiko_expect

4. Configure the script. Open the script with your preferred code editor and edit the following lines to suit your environment:


ldap_user = 'LDAP_USER'
ldap_pass = 'LDAP_PASS'
defaultuser = 'defaultuser'
defaultuserpass = 'defaultpass'

Replace LDAP_USER and LDAP_PASS with your LDAP username and password, respectively.

5. Run the script by running the following command in your terminal or command prompt:

python script.py

Replace script.py with the name of the script file that you downloaded in step 2.

**Note: This script was tested on Python 3.8.8 on Windows 10.**


# How to Use

After running the script, you will be prompted to enter the IP address of the CPE that you want to connect to.

Wait for the script to complete the connections to the CPEs. The results will be written to the Cisco&Huawei-Telnet&SSH-LDAP.txt file.



# Note
If the script cannot connect to a CPE, it will write a message to the Cisco&Huawei-Telnet&SSH-LDAP.txt file, saying that the CPE is unreachable.
The script also writes the type of the CPE (Cisco or Huawei), the protocol (Telnet or SSH), and the success status (successful access or unreachable) to the Cisco&Huawei-Telnet&SSH-LDAP.txt file.

