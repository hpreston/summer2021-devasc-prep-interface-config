#! /usr/bin/env python
"""
A script to create and apply interface descriptions from CSV
file based source of truth. 

Goal: 
 - Create interface description config from data in CSV file 
 - Allow users to apply configurations to devices with confirmation 
 - Record initial/old interface description back to CSV file for audit trail
 - Verify if interfaces are actually connected to devices documented in CSV
"""

import csv
from jinja2 import Template
from collections import defaultdict
from pyats.topology.loader import load


# Script entry point
if __name__ == "__main__": 
    print("Deploying standard interface descriptions to network.")
    # Use argparse retrieve script options : https://docs.python.org/3/library/argparse.html
    import argparse 
    parser = argparse.ArgumentParser(description='Deploying standard interface descriptions to network.')
    parser.add_argument('--testbed', required=True, type=str, help='pyATS Testbed File')
    parser.add_argument('--sot', required=True, type=str, help='Interface Connection Source of Truth Spreadsheet')
    parser.add_argument('--apply', action='store_true', help="Should configurations be applied to network. If not set, config not applied.")
    args = parser.parse_args()

    print(f"Generating interface descriptions from file {args.sot} for testbed {args.testbed}.")
    if args.apply: 
        print("Configurations will be applied to network devices.")
    else: 
        print("Configurations will NOT be applied to network devices. They will be output to the screen only.")
    
    print()

    # Create Jinja Template for Interface configuration by reading contents of file
    #   https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Template
    with open("interface_config_template.j2") as f: 
        interface_template = Template(f.read())

    # defaultdict variable for holding device interface configurations
    #   Example: 
        # {
        #     "my_rtr01": {
        #         "GigabitEthernet 2": "interface GigabitEthernet2 \n  description New Description", 
        #         "GigabitEthernet 3": "interface GigabitEthernet3 \n  description New Description", 
        #     }, 
        #     "my_rtr02": {
        #         "GigabitEthernet 2": "interface GigabitEthernet2 \n  description New Description", 
        #         "GigabitEthernet 3": "interface GigabitEthernet3 \n  description New Description", 
        #     }
        # }
    # defaultdicts - when an unexecting key is accessed, it is initialized with a value
    new_configurations = defaultdict(dict)

    # Read data from CSV source of truth
    print("Opening and readying Source of Truth File.\n")
    with open(args.sot, "r") as sot_file: 
        sot = csv.DictReader(sot_file)

        # Loop over each row in the Source of Truth
        for row in sot: 
            # For debugging, print out the raw data of the row
            # print(row)

            # Status message on interface being processed 
            if row["Device Name"]: 
                print(f'Device {row["Device Name"]:15} Interface {row["Interface"]:25} SOT connection: {row["Connected Device"]} {row["Connected Interface"]}')

                # Generate desired interface description configurations
                new_configurations[row["Device Name"]][row["Interface"]] = interface_template.render(
                    interface_name=row["Interface"], 
                    connected_device=row["Connected Device"], 
                    connected_interface=row["Connected Interface"],
                    purpose=row["Purpose"]
                )

        # Print a blank line
        print()


    # For debugging, print out the new_configurations data
    # print("Jinja Template rendered configuration data.")
    # print(new_configurations)

    # Display the new configurations for the devices to the user for verifications.
    print("New Device Configurations for Interface Descriptions")
    print("----------------------------------------------------")
    for device, interfaces in new_configurations.items(): 
        print(f"! Device {device}")
        for interface_name, interface_config in interfaces.items(): 
            print(interface_config)
        print("!\n")

    # Load pyATS testbed and connect to devices
    print(f"Loading testbed file {args.testbed}")
    testbed = load(args.testbed)
    print(f"Connecting to all devices in testbed {testbed.name}")
    testbed.connect(log_stdout=False)


    # Lookup current interface descriptions - But only for devices in SoT
    current_interface_details = {}
    for device in new_configurations.keys(): 
        try: 
            print(f'Learning current interface state for device {device}')
            current_interface_details[device] = testbed.devices[device].learn("interface")
        except KeyError: 
            print(f" ⚠️ Error: Device {device} from Source of Truth is NOT in the testbed")

    # For debugging, print the current_interface_details 
    #   Reference the Interface Model Details Docs: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    print("Output from learn interface operation")
    # print(current_interface_details)
    for device, interfaces in current_interface_details.items(): 
        print(f'Device {device} Current Interface Descriptions are: ')
        for interface, details in interfaces.info.items(): 
            try: 
                print(f'  {interface} : {details["description"]}')
            # Interfaces without descriptions won't have the key in the model
            except KeyError: 
                print(f'  {interface} : ')

    # Apply new interface description configuration (with confirmation)


    # Gather CDP/LLDP neighbor details from devices


    # Check if neighbor details match Source of Truth


    # Disconnect from devices
    for device in testbed.devices: 
        print(f"Disconnecting from device {device}.")
        testbed.devices[device].disconnect()


    # Update Source of Truth with Results

