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
script.write("#!/bin/bash\n")

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

    choice2 = input("\t[*] Are you going to specify a DNS server IP Address? Y/N: ")
    while(choice2.lower() != 'y' and choice2.lower() != 'n'):
        choice2 = input("\t[*] Are you going to specify a DNS server IP Address? Y/N: ")

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

# ALLOW OUTBOUND WEB REQUESTS FOR THINGS LIKE PACKAGE MANAGEMENT
choice = input("[*] Allow outbound HTTP requests? (enhances usability for package management but reduces security) Y/N: ")
while(choice.lower() != 'y' and choice.lower() != 'n'):
    choice = input("[*] Allow outbound HTTP requests? (enhances usability for package management but reduces security) Y/N: ")

if choice.lower() == 'y':
    script.write("\n# ALLOW OUTBOUND HTTP/S REQUESTS FOR PACKAGE MANAGEMENT ETC\n")
    script.write("# NOTE: ONLY WORKS FOR STANDARD PORTS\n")
    script.write("iptables -A OUTPUT -p tcp --dport 80 -j ACCEPT\n")
    script.write("iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT\n")
####################################################
# NON-USER-CONFIGURABLE RULES THAT ARE REQUIRED
####################################################

# ALLOW ALL TRAFFIC ON lo INTERFACE
script.write("\n# ALLOW ALL TRAFFIC ON LOOPBACK\n")
script.write("iptables -A INPUT -i lo -j ACCEPT\n")
script.write("iptables -A OUTPUT -o lo -j ACCEPT\n")

# ALLOW ALL ESTABLISHED AND RELATED CONNECTIONS
script.write("\n# ALLOW ALL ESTABLISHED AND RELATED CONNECTIONS\n")
script.write("iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n")
script.write("iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT\n")

########################################################
# CONFIGURE PORTSPOOF
########################################################
portspoof = ""
while portspoof.lower() != 'y' and portspoof.lower() != 'n':
    portspoof = input("[*] Install and auto-configure PortSpoof utility? Y/N: ")

if portspoof.lower() == 'y':
    print("\n[*] Attempting to install portspoof:")
    os.chdir('./portspoof')
    print("\n[*] Running 'sh configure'")
    print("====================================================")
    os.system('sh configure')
    print("\n[*] Running 'make'")
    print("====================================================")
    os.system('make')
    print("\n[*] Running 'make install'")
    print("====================================================")
    os.system('make install')
    print('\n')

    print("[*] PortSpoof Installation Complete")

    script.write("\nportspoof -D -c ./portspoof/tools/postspoof.conf -s ./portspoof/tools/portspoof_signatures\n")
    print("[*] Added PortSpoof startup to rules.sh")

# IF USER DESIRES, INSTALL AND CONFIGURE PORTSPOOF. THIS WILL REQUIRE BUFFERING ALL OUTPUT, TRACKING ALL PORTS MODDED,
# AND THEN APPENDING PORTSPOOF LINES AND THEN NORMAL PORT LINES
RULES = []
PORTS = []

#########################################################
# INSTALL FAIL2BAN
#########################################################
fail2ban = input("[*] Install and configure fail2ban? Y/N: ")

# IF USER DESIRES, INSTALL FAIL2BAN


##########################################################
# ROLE-BASED CONFIGURATION
##########################################################
print("\nRAPID AXOLOTL has a role-based configuration mode. In this mode, you can specify one or multiple server roles,")
print("for which pre-set IPTables rules will be used. This mode is optional, and should you use it, you can still opt")
print("to specify additional, custom rules.")
roleBased = input("\n[*] Enter role-based configuration mode? Y/N: ")

while(roleBased.lower() != 'y' and roleBased.lower() != 'n'):
    roleBased = input("\n[*] Enter role-based configuration mode? Y/N: ")

if(roleBased.lower() == 'y'):
    while(True):
        print("""
        [1] FTP
        [2] SSH
        [3] DNS
        [4] Web (ports 80 & 443 only)
        [5] Mail
        [6] DHCP
        [7] MySQL
        """)

        role = input("\t[*] Select: ")
        # FTP
        if role == '1':
            RULES.extend([
                "\n# FTP ROLE\n",
                "iptables -A INPUT -p tcp --dport 21 -j ACCEPT\n"
            ])
            PORTS.append(21)
        # SSH
        elif role == '2':
            RULES.extend([
                "\n# SSH ROLE\n",
                "iptables -A INPUT -p tcp --dport 22 -j ACCEPT\n"
            ])
            PORTS.append(22)
        # DNS
        elif role == '3':
            RULES.extend([
                "\n# DNS ROLE\n",
                "iptables -A INPUT -p udp --dport 53 --sport 1024:65535 -j ACCEPT\n",
                "iptables -A INPUT -p tcp --dport 53 --sport 1024:65535 -j ACCEPT\n",
            ])
            PORTS.append(53)
            # OUTPUT SHOULD BE ALLOWED BY THE EXPLICIT ALLOWING OF ANY ESTABLISHED OR RELATED CONNECTIONS
        # HTTP
        elif role == '4':
            RULES.extend([
                "\n# WEB ROLE\n",
                "iptables -A INPUT -p tcp --dport 80 -j ACCEPT\n",
                "iptables -A INPUT -p tcp --dport 443 -j ACCEPT\n"
            ])
            PORTS.append(80)
            PORTS.append(443)

            # ENABLE 8080 FOR HTTP-ALT?
            use8080 = input("\t[*] Allow port 8080 (http-alt) traffic? Y/N: ")
            while(use8080.lower() != 'y' and use8080.lower() != 'n'):
                use8080 = input("\t[*] Allow port 8080 (http-alt) traffic? Y/N: ")
            if use8080.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 8080 -j ACCEPT\n")
                PORTS.append(8080)

             # ENABLE 8000 FOR HTTP?
            use8000 = input("\t[*] Allow port 8000 traffic? Y/N: ")
            while(use8000.lower() != 'y' and use8000.lower() != 'n'):
                use8000 = input("\t[*] Allow port 8000 traffic? Y/N: ")
            if use8000.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 8000 -j ACCEPT\n")
                PORTS.append(8000)

             # ENABLE 8888 FOR HTTP?
            use8888 = input("\t[*] Allow port 8888 traffic? Y/N: ")
            while(use8888.lower() != 'y' and use8888.lower() != 'n'):
                use8000 = input("\t[*] Allow port 8000 traffic? Y/N: ")
            if use8888.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 8888 -j ACCEPT\n")
                PORTS.append(8888)

            print("\t[*] INFO: make sure to configure other ports for things like databases manually!")

        # MAIL
        elif role == '5':
            RULES.append("\n# MAIL ROLE\n")

            # ENABLE SMTP?
            use25 = input("\t[*] Allow SMTP traffic? (recommended) Y/N: ")
            while(use25.lower() != 'y' and use25.lower() != 'n'):
                use25 = input("\t[*] Allow SMTP traffic? (recommended) Y/N: ")
            if use25.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 25 -j ACCEPT\n")
                PORTS.append(25)

            # ENABLE POP3?
            use110 = input("\t[*] Allow POP3 traffic? (recommended) Y/N: ")
            while(use110.lower() != 'y' and use110.lower() != 'n'):
                use110 = input("\t[*] Allow POP3 traffic? (recommended) Y/N: ")
            if use110.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 110 -j ACCEPT\n")
                PORTS.append(110)

            # ENABLE POP3S?
            use995 = input("\t[*] Allow POP3S traffic? (recommended) Y/N: ")
            while(use995.lower() != 'y' and use995.lower() != 'n'):
                use995 = input("\t[*] Allow POP3S traffic? (recommended) Y/N: ")
            if use995.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 995 -j ACCEPT\n")
                PORTS.append(995)

            # ENABLE IMAP?
            use143 = input("\t[*] Allow IMAP traffic? (recommended) Y/N: ")
            while(use143.lower() != 'y' and use143.lower() != 'n'):
                use143 = input("\t[*] Allow IMAP traffic? (recommended) Y/N: ")
            if use143.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 143 -j ACCEPT\n")
                PORTS.append(143)

            # ENABLE IMAPS?
            use993 = input("\t[*] Allow IMAPS traffic? (recommended) Y/N: ")
            while (use993.lower() != 'y' and use993.lower() != 'n'):
                use993 = input("\t[*] Allow IMAPS traffic? (recommended) Y/N: ")
            if use993.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 993 -j ACCEPT\n")
                PORTS.append(993)
        # DHCP
        elif role == '6':
            RULES.extend([
                "\n# DHCP ROLE\n",
                "iptables -A INPUT -p udp --dport 67:68 -j ACCEPT\n"
            ])
            PORTS.append(67)
            PORTS.append(68)

        # MySQL
        elif role == '7':
            RULES.append("\n# PUBLIC MYSQL ROLE\n")
            isPublic = input("\t[*] Does the service need to be reachable from outside this subnet? Y/N: ")
            while(isPublic.lower() != 'y' and isPublic.lower() != 'n'):
                isPublic = input("\t[*] Does the service need to be reachable from outside this subnet? Y/N: ")
            if isPublic.lower() == 'y':
                RULES.append("iptables -A INPUT -p tcp --dport 3306 -j ACCEPT\n")
            else:
                subnet = input("\t[*] Enter host IP or subnet in CIDR notation that needs to connect to this service: ")
                RULES.append(f'iptables -A INPUT -p tcp --dport 3306 -s {subnet} -j ACCEPT\n')
            PORTS.append(3306)

        # PROMPT TO CONFIGURE ANOTHER ROLE?
        configureAnotherRole = input("\t[*] Configure another role for this host? Y/N: ")
        while(configureAnotherRole.lower() != 'y' and configureAnotherRole.lower() != 'n'):
            configureAnotherRole = input("\t[*] Configure another role for this host? Y/N: ")
        if (configureAnotherRole.lower() == 'y'):
            continue
        else:
            break

##########################################################
# CUSTOM CONFIGURATION
##########################################################
print("\nRAPID AXOLOTL also allows you to specify custom rules in addition to role-based configuration. In this mode,")
print("you will be prompted to specify a port, and then select configuration options. This mode is optional, and is ")
print("entirely compatible with role-based configuration")
customConfig = input("\n[*] Enter custom configuration mode? Y/N: ")

while(customConfig.lower() != 'y' and customConfig.lower() != 'n'):
    customConfig = input("\n[*] Enter custom configuration mode? Y/N: ")

if customConfig.lower() == 'y':
    print("\n[*] INFO: Allowing new inbound traffic to a port allows a remote host to establish a connection to that port")
    print("          on this host. e.g. allowing new inbound traffic to port 80 when this host is running an HTTP server")
    print("          would allow remote hosts to make web requests to the server.")
    print("[*] INFO: Allowing new outbound traffic to a port allows this host to establish a connection to that port on")
    print("          a remote host. e.g. allowing new outbound traffic to port 80 will allow this host to make web requests")
    print("[*] INFO: Restricting traffic by source port is not currently supported as it is not considered to be very")
    print("          useful: source ports are usually randomized and as such do not usually give us useful information")
    print("\n[*] INFO: Please be sure to be conscious of these distinctions when configuring ports.\n")
    while(True):

        # GET PORT
        port = input("\n[*] Enter a valid Port Number to configure: ")

        # ENSURE THE PORT IS A DIGIT AND IN THE RANGE OF VALID PORTS
        if port.isdigit():
            if int(port) < 0 or int(port) > 65535:
                continue
        else:
            continue

        # GET PROTOCOL
        protocol = input('\t[*] Protocol? tcp/udp: ')
        while (protocol != 'tcp' and protocol != 'udp'):
            protocol = input('\t[*] Protocol? tcp/udp: ')

        # CHECK IF INBOUND TRAFFIC TO THE PORT SHOULD BE ALLOWED
        allowInbound = ""
        while (allowInbound.lower() != 'y' and allowInbound.lower() != 'n'):
            allowInbound = input('\t[*] Allow new inbound traffic TO this port? Y/N: ')

        allowInbound = allowInbound == 'y'
        shouldLimitInbound = ""
        inboundLimit = ""

        # IF INBOUND TRAFFIC IS ALLOWED, CHECK IF IT SHOULD BE LIMITED TO A HOST OR SUBNET?
        if allowInbound:
            while (shouldLimitInbound.lower() != 'y' and shouldLimitInbound.lower() != 'n'):
                shouldLimitInbound = input("\t[*] Restrict inbound traffic to this port to a host/subnet? Y/N: ")

            shouldLimitInbound = shouldLimitInbound.lower() == 'y'

            if shouldLimitInbound:
                inboundLimit = input("\t\t[*] Enter host IP address or subnet in CIDR notation to whitelist: ")

        # CHECK IF OUTBOUND TRAFFIC TO PORT SHOULD BE ALLOWED
        allowOutbound = ""
        while (allowOutbound.lower() != 'y' and allowOutbound.lower() != 'n'):
            allowOutbound = input('\t[*] Allow new outbound traffic TO this port (on another host)? Y/N: ')

        allowOutbound = allowOutbound == 'y'
        shouldLimitOutbound = ""
        outboundLimit = ""

        # IF OUTBOUND TRAFFIC IS ALLOWED, CHECK IF IT SHOULD BE LIMITED TO A HOST OR SUBNET
        if allowOutbound:
            while (shouldLimitOutbound.lower() != 'y' and shouldLimitOutbound.lower() != 'n'):
                shouldLimitOutbound = input("\t[*] Restrict outbound traffic to this port to a host/subnet? Y/N: ")

            shouldLimitOutbound = shouldLimitOutbound.lower() == 'y'

            if shouldLimitOutbound :
                outboundLimit = input("\t\t[*] Enter host IP address or subnet in CIDR notation to whitelist: ")

        # BASED ON THIS INFORMATION, GENERATE RULES AND UPDATE PORTS LIST

        # UPDATE PORTS LIST
        if allowInbound:
            PORTS.append(port)

        # GENERATE INBOUND RULES
        if allowInbound and shouldLimitInbound:
            RULES.append(f'iptables -A INPUT -p {protocol} --dport {port} -s {inboundLimit} -j ACCEPT\n')
        elif allowInbound and not shouldLimitInbound:
            RULES.append(f'iptables -A INPUT -p {protocol} --dport {port} -j ACCEPT\n')

        # GENERATE OUTBOUND RULES
        if allowOutbound and shouldLimitOutbound:
            RULES.append(f'iptables -A OUTPUT -p {protocol} --dport {port} -d {outboundLimit} -j ACCEPT\n')
        elif allowOutbound and not shouldLimitOutbound:
            RULES.append(f'iptables -A OUTPUT -p {protocol} --dport {port} -j ACCEPT\n')

        print("\t[*] Port configured!")
        # CHECK TO SEE IF USER WANTS TO CONFIGURE ANOTHER PORT
        addAnother = ""
        while addAnother.lower() != 'y' and addAnother.lower() != 'n':
            addAnother = input("[*] Configure another port? Y/N: ")
        if (addAnother.lower() == 'y'):
            continue
        else:
            break

###################################################################################
# ACTUALLY DO THE PORTSPOOF INSTALL NOW THAT WE HAVE ALL THE PORTS TO WORK AROUND
###################################################################################
script.write("\n# PORTSPOOF CONFIG\n")
# INSTALL PORTSPOOF


# SORT PORTS LIST
PORTS.sort(reverse=False)

# DETERMINE RANGES TO SPOOF
portsToSpoof = ""
if (len(PORTS) >= 14):
    # WILL HAVE TO OVERLAP SOME RANGES
    start = 1
    i = 0
    while i < 14:
        portsToSpoof += f'{start}:{int(PORTS[i] - 1)} '
        start = int(PORTS[i]) + 1
        i += 1
    portsToSpoof += f'{max(PORTS)}:65535'

else:
    # CAN DO NORMAL CONFIG
    start = 1
    for port in PORTS:
        portsToSpoof += f'{start}:{int(port) - 1} '
        start = int(port) + 1
    portsToSpoof += f'{start}:65535'

print("[*] DEBUG: portspoof ports: " + portsToSpoof)
script.write(f'spoofPorts="{portsToSpoof}"\n')
script.write("for prange in ${spoofPorts}; do\n")
script.write("\tiptables -t nat -A PREROUTING -p tcp -m tcp --dport ${prange} -j REDIRECT --to-ports 4444\n")
script.write("done\n")
script.write("iptables -A INPUT -p tcp --dport 4444 -j ACCEPT\n")
script.write("iptables -A OUTPUT -p tcp --sport 4444 -j ACCEPT\n")

############################################################
# WRITE OUT ALL THE RULES WE CONFIGURED TO THE SCRIPT NOW
############################################################
script.write('\n')

for rule in RULES:
    script.write(rule)

#############################################################
# ALL OPTIONS SHOULD GO BEFORE HERE WHERE THE FILE IS CLOSED
#############################################################

# CLOSE THE SCRIPT
script.close()

# MAKE ROOT THE OWNER OF THE SCRIPT
os.system("chown root:root rules.sh")

# ENSURE ONLY ROOT CAN RUN THE SCRIPT
os.system("chmod 770 rules.sh")

##############################################################
# OFFER TO RUN SCRIPT
##############################################################
print("\n[*] script generation complete, can be found at " + os.curdir + '/rules.sh')
run = input('[*] Would you like to run the script? Y/N: ')
while run.lower() != 'n' and run.lower() != 'y':
    run = input('[*] Would you like to run the script? Y/N: ')

if run.lower() == 'y':
    os.system('sh rules.sh')
    print("[*] Executed rules.sh")

    persist = ""
    print("\n[*] INFO: Enabling rule persistence will prevent rules from being cleared on system restart")
    while persist.lower() != 'y' and persist.lower() != 'n':
        persist = input("[*] Would you like to enable rule persistence? Y/N: ")
    if persist.lower() == 'y':
        os.system('iptables-save')

