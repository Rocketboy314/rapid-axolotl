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
    script.write("iptables -A OUTPUT -p udp -d $ip --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n")
    script.write("iptables -A INPUT  -p udp -s $ip --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n")
    script.write("iptables -A OUTPUT -p tcp -d $ip --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT\n")
    script.write("iptables -A INPUT  -p tcp -s $ip --sport 53 -m state --state ESTABLISHED     -j ACCEPT\n")
#############################################################
# ALL OPTIONS SHOULD GO BEFORE HERE WHERE THE FILE IS CLOSED
#############################################################
script.close()