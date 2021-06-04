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

    # Read data from CSV source of truth
    print("Opening and readying Source of Truth File.\n")
    with open(args.sot, "r") as sot_file: 
        sot = csv.DictReader(sot_file)

        # Loop over each row in the Source of Truth
        for row in sot: 
            # For debugging, print out the raw data of the row
            print(row)


    # Generate desired interface description configurations


    # Load pyATS testbed and connect to devices


    # Lookup current interface descriptions


    # Apply new interface description configuration (with confirmation)


    # Gather CDP/LLDP neighbor details from devices


    # Check if neighbor details match Source of Truth


    # Disconnect from devices


    # Update Source of Truth with Results

