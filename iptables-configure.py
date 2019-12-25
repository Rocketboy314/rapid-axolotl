import time, os, sys, shutil

print("Blackl1ght presents...")
time.sleep(1.5)
print(
"""
  _______        __         _______   __     ________                         
 /"      \\      /""\\       |   __ "\\ |" \\   |"      "\\                        
|:        |    /    \\      (. |__) :)||  |  (.  ___  :)                       
|_____/   )   /' /\\  \\     |:  ____/ |:  |  |: \\   ) ||                       
 //      /   //  __'  \\    (|  /     |.  |  (| (___\\ ||                       
|:  __   \\  /   /  \\\\  \\  /|__/ \\    /\\  |\\ |:       :)                       
|__|  \\___)(___/    \\___)(_______)  (__\\_|_)(________/                        
                                                                              
      __       ___  ___   ______    ___        ______  ___________  ___       
     /""\\     |"  \\/"  | /    " \\  |"  |      /    " \\("     _   ")|"  |      
    /    \\     \\   \\  / // ____  \\ ||  |     // ____  \\)__/  \\\\__/ ||  |      
   /' /\\  \\     \\\\  \\/ /  /    ) :)|:  |    /  /    ) :)  \\\\_ /    |:  |      
  //  __'  \\    /\\.  \\(: (____/ //  \\  |___(: (____/ //   |.  |     \\  |___   
 /   /  \\\\  \\  /  \\   \\\\        /  ( \\_|:  \\\\        /    \\:  |    ( \\_|:  \\  
(___/    \\___)|___/\\___|\\"_____/    \\_______)\\"_____/      \\__|     \\_______) 
                                                                              
""")
print("RAPID AXOLOTL")
print("A python-based configuration tool for rapidly generating IPTables Firewall rules.")
print()
print("Disclaimer: this tool is intended to provide for easy configuration of BASIC rules.")
print("This tool is NOT designed for generating complicated rule sets. ")
print("It is STRONGLY recommended to verify rules work as expected before enabling rule persistence.")
print()
print()

# MAKE SURE THE SCRIPT IS NOT RUNNING ON WINDOWSS
if (os.name == 'nt'):
    sys.exit("\nThis tool does not support Windows hosts!")

# GET PATH OF IPTABLES BINARY
if (shutil.which('iptables') == None):
    sys.exit("\nIPTables is not in the PATH.")

# MAKE SURE THAT THE USER IS RUNNING THE SCRIPT AS ROOT SO THAT WE CAN ACTUALLY MODIFY IPTABLES RULES
if not os.geteuid() == 0:
    sys.exit("\nPlease run this script with SUDO or as root.\n")

# CREATE THE FILE; WILL OVERWRITE IF IT ALREADY EXISTS
script = open("rules.sh", "w+")
script.write("#!bin/bash\n")

# FLUSH IPTABLES RULES?
choice = input("[*] Flush existing IPTables rules? (recommended) Y/N: ")
while (choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Flush existing IPTables rules? (recommended) Y/N: ")

if (choice.lower() == 'y'):
    script.write("# FLUSH IPTABLES RULES\n")
    script.write("iptables -F\n")
    script.write("iptables -X\n")
    script.write("iptables -t nat -F\n")
    script.write("iptables -t nat -X\n")
    script.write("iptables -t mangle -F\n")
    script.write("iptables -t mangle -X\n")
    script.write("\n")

##############################################
# SET DEFAULT POLICIES
##############################################

script.write("# DEFAULT POLICIES\n")

# INPUT POLICY
choice = input("[*] Set default INPUT policy to DROP? (recommended) Y/N: ")
while(choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Set default INPUT policy to DROP? (recommended) Y/N: ")

if (choice.lower() == 'y'):
    script.write("iptables -P INPUT DROP\n")

# OUTPUT POLICY
choice = input("[*] Set default OUTPUT policy to DROP? (recommended) Y/N: ")
while(choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Set default OUTPUT policy to DROP? (recommended) Y/N: ")

if (choice.lower() == 'y'):
    script.write("iptables -P OUTPUT DROP\n")

# FORWARD POLICY
choice = input("[*] Set default FORWARD policy to DROP? (recommended) Y/N: ")
while(choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Set default FORWARD policy to DROP? (recommended) Y/N: ")

if (choice.lower() == 'y'):
    script.write("iptables -P FORWARD DROP\n")

#######################################################
# IMPORTANT MISCELLANEOUS STUFF
#######################################################

# IMCP ECHO
choice = input("[*] Block all inbound ICMP traffic? (May prevent host discovery and/or break things) Y/N: ")
while(choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Block all ICMP traffic? (May prevent host discovery and/or break things) Y/N: ")

if choice.lower() == 'y':
    script.write("\n# ICMP ECHO\n")
    script.write("iptables -A INPUT -p icmp -j DROP\n")

# ALLOW DNS RESOLUTION
choice = input("[*] Allow DNS resolution? (STRONGLY recommended) Y/N: ")
while(choice.lower() != 'y' and choice.lower != 'n'):
    choice = input("[*] Allow DNS resolution? (STRONGLY recommended) Y/N: ")

if choice.lower() == 'y':
    script.write("\n# ALLOW DNS RESOLUTION\n")

    choice2 = input("\t[*] Are you going to specify a DNS serve IP Address? Y/N: ")
    while(choice2.lower() != 'y' and choice2.lower() != 'n'):
        choice2 = input("\t[*] Are you going to specify a DNS serve IP Address? (recommended, if possible) Y/N: ")

    if choice2 == 'y':  # WITH A SPECIFIED IP ADDRESS
        ip = input("\t[*] Enter DNS server IP Address: ")
        script.write(f'iptables -A OUTPUT -p udp -d {ip} --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n')
        script.write(f'iptables -A INPUT  -p udp -s {ip} --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n')
        script.write(f'iptables -A OUTPUT -p tcp -d {ip} --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n')
        script.write(f'iptables -A INPUT  -p tcp -s {ip} --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n')
    else: # WITHOUT A SPECIFIED IP ADDRESS: THIS IS A BAD IDEA
        script.write(f'iptables -A OUTPUT -p udp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n')
        script.write(f'iptables -A INPUT  -p udp --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n')
        script.write(f'iptables -A OUTPUT -p tcp --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n')
        script.write(f'iptables -A INPUT  -p tcp --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n')

####################################################
# NON-USER-CONFIGURABLE RULES THAT ARE REQUIRED
####################################################

# ALLOW ALL TRAFFIC ON lo INTERFACE
script.write("iptables -A INPUT -i lo -j ACCEPT\n")
script.write("iptables -A OUTPUT -o lo -j ACCEPT\n")

# ALLOW ALL ESTABLISHED AND RELATED CONNECTIONS
script.write("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n")
script.write("iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n")

########################################################
# CONFIGURE PORTSPOOF
########################################################
portspoof = input("\n[*] Install and auto-configure PortSpoof utility? Y/N: ")

# IF USER DESIRES, INSTALL AND CONFIGURE PORTSPOOF. THIS WILL REQUIRE BUFFERING ALL OUTPUT, TRACKING ALL PORTS MODDED,
# AND THEN APPENDING PORTSPOOF LINES AND THEN NORMAL PORT LINES


#########################################################
# INSTALL FAIL2BAN
#########################################################
fail2ban = input("\n[*] Install and configure fail2ban? Y/N: ")

# IF USER DESIRES, INSTALL FAIL2BAN

##########################################################
# ROLE-BASED CONFIGURATION
##########################################################
print("RAPID AXOLOTL has a role-based configuration mode. In this mode, you can specify one or multiple server roles,")
print("for which pre-set IPTables rules will be used. This mode is optional, and should you use it, you can still opt")
print("to specify additional, custom rules.")
roleBased = input("\n[*] Enter role-based configuration mode? Y/N: ")

##########################################################
# CUSTOM CONFIGURATION
##########################################################
print("RAPID AXOLOTL also allows you to specify custom rules in addition to role-based configuration. In this mode,")
print("you will be prompted to specify a port, and then select configuration options. This mode is optional, and is ")
print("entirely compatible with role-based configuration")
customConfig = input("\n[*] Enter custom configuration mode? Y/N: ")

#############################################################
# ALL OPTIONS SHOULD GO BEFORE HERE WHERE THE FILE IS CLOSED
#############################################################
script.close()