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

### SRX Configuration requirements
The User_logon.py script allows these attributes to be dynamically programmed into the SRX. The following configuration entries will be required within JUNOS to configure the webapi service, permit the client IP address and authentication. Currently the script supports only HTTP communications while it is  possible for JUNOS to also support TLS encrypted HTTP. In the below configuration changes the username and password are hard coded into the User_logon.py script. 

```
set system services webapi user <USERNAME>
set system services webapi user password <PASSWORD>
set system services webapi client <IP ADDRESS>
set system services webapi http port 8080
```

### Script usage - Users and Roles
Modify the User_logon.py script with the appropriate username/password (The provided script is using user1/password) The script has many possible parameters that can be modified; below is a basic example that could be triggered when a user logs into the network. 

```
./User-Logon.py -o logon -u Bob -a 192.168.0.56 -r Finance -d BigCorp -p Healthy
```

This simple example with perform a "logon" operation and assign the user to the role of Finance, AD Domain of BigCorp with a posture of Healthy. The bare minimum needed is username, role, IP Address and Posture. The IP Address can be either IPv4 or IPv6. 

When looking at the changes to the SRX the following dynamic user entry is now visible;

```
admin@SRX320> show services user-identification authentication-table authentication-source all extensive
Domain: bigcorp
Total entries: 1
  Source-ip: 192.168.0.56
    Username: bob
    Groups:posture-healthy, finance
    State: Valid
    Source: Aruba ClearPass
    Access start date: 2016-12-13
    Access start time: 11:38:59
    Last updated timestamp: 2016-12-13 11:40:31
    Age time: 0
```
To logoff a user from the network use the following command syntax

```
./User-Logon.py -o logoff -u Bob -a 192.168.0.56
```
### SRX policy enforcement - Posture

The SRX policy can now use the roles that are assigned as part of the source-identity. The source-identiy is a combination of the domain name (default is global) which in this example is bigcorp. 

```
set security policies from-zone trust to-zone untrust policy infected match source-address any
set security policies from-zone trust to-zone untrust policy infected match destination-address any
set security policies from-zone trust to-zone untrust policy infected match application any
set security policies from-zone trust to-zone untrust policy infected match source-identity "bigcorp\posture-infected"
set security policies from-zone trust to-zone untrust policy infected then deny
set security policies from-zone trust to-zone untrust policy healthy match source-address any
set security policies from-zone trust to-zone untrust policy healthy match destination-address any
set security policies from-zone trust to-zone untrust policy healthy match application any
set security policies from-zone trust to-zone untrust policy healthy match source-identity "bigcorp\posture-healthy"
set security policies from-zone trust to-zone untrust policy healthy then permit
```

Once this policy is in place we can see that is it being matched by examining the users authentication-table entry. Withing the groups referenced section it states "finance". If the users posture changed to "infected" this would also be show as a group reference. 

```
admin@SRX320> show services user-identification authentication-table ip-address 192.168.0.6
Domain: bigcorp
  Source-ip: 192.168.0.6
    Username: bob
    Groups:posture-healthy, finance
    Groups referenced by policy:finance
    State: Valid
    Source: Aruba ClearPass
    Access start date: 2016-12-13
    Access start time: 12:52:00
    Last updated timestamp: 2016-12-13 13:04:21
    Age time: 0
```

### Script usage - Device parameters
In addition to adding user details (Username, IP, Roles etc) it is also possible to associate a specific type of device and associated operating system details with the user. This can be enforced through policy to ensure that only specific corporate devices are allowed on the network. For example, only allow laptops running Windows 10 access to the Internet. 

```
./User-Logon.py -o logon -u Bob -a 192.168.0.6 -r Finance -d BigCorp -p Healthy --os windows --version 10 --vendor Lenovo -t laptop --hostname Bobs-Super-laptop --model X220
```

When looking at the changes to the SRX the following dynamic user entry is now visible;

```
admin@SRX320> show services user-identification device-information table all extensive
Domain: bigcorp
Total entries: 1
  Source IP: 192.168.0.6
    Device ID: bobs-super-laptop
    Device-Groups: N/A
    device-category: laptop
    device-vendor: lenovo
    device-os: windows
    device-os-version: 10
    device-model: x220
    Referred by: corp-laptop
```

### SRX policy enforcement - Device details

The SRX policy can now use the device specifics as part of the security policy. First a specific end-user-profile needs to be created to match your device paramters. 

```
set services user-identification device-information end-user-profile profile-name corp-laptop domain-name bigcorp
set services user-identification device-information end-user-profile profile-name corp-laptop attribute device-category string laptop
set services user-identification device-information end-user-profile profile-name corp-laptop attribute device-vendor string lenovo
set services user-identification device-information end-user-profile profile-name corp-laptop attribute device-os-version string 10
set services user-identification device-information end-user-profile profile-name corp-laptop attribute device-os string windows
```
Once this profile has been created it can now be used in a security policy. I'm re-using the healthy/infected policy here to ensure that we are matching on corporate devices and their posture. 

```
set security policies from-zone trust to-zone untrust policy corp-laptop match source-address any
set security policies from-zone trust to-zone untrust policy corp-laptop match destination-address any
set security policies from-zone trust to-zone untrust policy corp-laptop match application any
set security policies from-zone trust to-zone untrust policy corp-laptop match source-end-user-profile corp-laptop
set security policies from-zone trust to-zone untrust policy corp-laptop then permit
set security policies from-zone trust to-zone untrust policy deny match source-address any
set security policies from-zone trust to-zone untrust policy deny match destination-address any
set security policies from-zone trust to-zone untrust policy deny match application any
set security policies from-zone trust to-zone untrust policy deny then deny
```

### Third party integration - Splunk

Third party systems can use this scripting infrastructure to dynamically provision users and device details into the SRX firewall. An example of this would be having Splunk make changes in reaction to receiving a specific SYSLOG event. In Splunk terms this is an Alert Action. The splunk-wrapper.py script as well as the user-logon.py script should be placed into the /opt/splunk/bin/scripts directory. The "wrapper" script receives the log entry (passed as reference to a locally stored csv file) and extracts the relevant parameters that are then passed to the user-logon script. The below examples are purely for reference and based on the log events being passed would need to be modified to accomdate. Additionally to "test" scripts have been provided to indicate a host is "healthy" or "infected" 

The syslog_healthy.py and syslog_infected.py scripts will need to be mofified to change the IP Address of the Splunk server. Once these scripts are executed that generate a UDP SYSLOG event (on port 514) towards the Splunk server. These event lines are simply displaying a username, IP-Address and posture. These should be visible in the event viewer as follows;


![Image of Splunk Event entries
(https://github.com/farsonic/SRX-User-Logon/blob/master/Splunk-Event.png)


