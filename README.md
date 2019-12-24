# rapid-axolotl
Python-based interface for configuring IPTables firewall rules for CCDC.

This tool is designed to run on Linux distributions that support IPTables host-based firewall.

## Dependencies
* Python 3
* iptables binary (must be in the PATH)

## Installation & Use
Clone repository:       `git clone https://github.com/k-mistele/rapid-axolotl.git`

Run python script:      `python3 iptables-configure.py`

Follow the prompts to generate a bash script that will setup your IPTables firewall when run. 
The script will be saved to `rules.sh`. The tool will offer to run it for you, 
and to make the rules persistent.


_Developed by @0xBlackl1ght_