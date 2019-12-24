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
if (shutil.which('iptables') != str):
    sys.exit("\nIPTables is not in the PATH.")
if not os.geteuid() == 0:
    sys.exit("\nPlease run this script with SUDO or as root.\n")


