# SRX-User-Logon

Starting with the D70 release of software the SRX is capable of accepting dynamic variables for users and devices that are connected to the network. These variables are both fixed and user defined. Fixed variables include the following definitions

* Username
* IPv4 and/or IPv6 Address
* Active Directory Domain Name
* Network "roles" 
* Posture 
* Operation type (Logon, Logoff) 

End-user attributes exist for the device being used by the user, including;

* Device identity (Computer/Device name) 
* Groups the device belongs to
* Device Category
* Device Vendor name
* Device Type
* Device Operating System
* Operating System Version

Additionally the system allows for totally custom tags to be associated with each end user allowing for any any information to be populated and matched within firewall policy

The User_logon.py script allows these attributes to be dynamically programmed into the SRX. The following configuration entries will be required within JUNOS to configure the webapi service, permit the client IP address and authentication. Currently the script supports only HTTP communications while it is  possible for JUNOS to also support TLS encrypted HTTP. 

```
set system services webapi user <USERNAME>
set system services webapi user password <PASSWORD>
set system services webapi client <IP ADDRESS>
set system services webapi http port 8080
```
