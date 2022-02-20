
import subprocess, optparse, re

## optparse allows us to add arguments when you launch the script, like so:
## python3 MacAddressChanger.py -i eth0 -m 00:11:22:33:66


def get_arguments():
    
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface whose MAC Address you want to change')
    parser.add_option('-m', '--mac', dest='new_mac', help='New MAC Address')
    (values,arguments) = parser.parse_args()
    if not values.interface:
        parse.error('[-] Please specify an interface.')
    elif not values.new_mac:
        parse.error('[-] Please specify a new MAC address.')
    else:
        return values
        ## We only need the values, not the arguments
        


def change_mac(interface, new_mac):
    print('Changing MAC address for ' + interface + ' to ' + new_mac)
    subprocess.call(["ipconfig", interface, "down"])
    subprocess.call(["ipconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ipconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_str = str(ifconfig_result)

    mac_regex = re.compile(r"\w\w\:\w\w\:\w\w\:\w\w\:\w\w\:\w\w")
    mac_search_result = mac_regex.findall(ifconfig_str)

    if mac_search_result:
        return mac_search_result[0]
    else:
        print('[-] Could not find a MAC address')


# The function get_arguments() returns parser.parse_args(), which we then capture with the
# two variables 'values' and 'arguments'. We then call the function change_mac() and we
# feed it values.interface and values.new_mac 

# 1. With this function we capture the values of the arguments 'interface' and
# 'new_mac' we passed when launching the script and we assign them to the variable
# 'options'

options = get_arguments()
# options is an instance of the class 'optparse.Values', reminds me of a dictionary:
# {'interface': 'en0', 'new_mac': '00:11:22:33:44:66'}
print(options.new_mac[:10])
print(type(options))

# 2. With this function we capture the current MAC address we found using the
# regEx into the variable 'current_mac'

current_mac = get_current_mac(options.interface)
print('Current MAC is ' + str(current_mac))

# 3. With this function we change the MAC address to the one we pass as an attribute
# when launching the script
change_mac(options.interface, options.new_mac)

# 4. We notify the user whether the change was successful

current_mac = get_current_mac(options.interface)
# If the regex returns a MAC address that matches the MAC address we passed as
# an argument when launching the script, it means the MAC was successfully
# changed
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address was not successfully changed")






