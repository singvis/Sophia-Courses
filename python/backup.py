# =====================================================================
# Program Name: Automated Network Configuration Backup Tool
# Purpose: This program reads a list of network devices from an Excel file,
# connects to each device using SSH, retrieves their current configuration,
# and saves the configuration into individual text files for backup.
# =====================================================================

import os
import openpyxl
from netmiko import ConnectHandler
# Import specific exceptions to handle network connection errors
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

def main():
    # Define the names of the input file and the output folder
    excel_file = "devices.xlsx"
    output_dir = "Config_Backups"

    # Check if the backup folder exists. If it doesn't, create it.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Try to open the Excel file that contains the device list.
    try:
        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active
    except FileNotFoundError:
        print(f"Error: The file '{excel_file}' was not found. Please check the path.")
        return

    # Loop through every row in the Excel sheet, skipping the header row.
    for row in sheet.iter_rows(min_row=2, values_only=True):
        
        # Extract the data from the current row into separate variables
        device_name, ip, username, password, device_type = row

        # Create a dictionary for Netmiko connection
        device_info = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }

        print(f"\nConnecting to {device_name} ({ip})...")

        # Start a try block to handle potential network connection errors
        try:
            # Establish an SSH connection to the network device
            net_connect = ConnectHandler(**device_info)
            
            # Execute the command to fetch the configuration
            config_output = net_connect.send_command('show running-config')
            
            # Create the full file path for saving
            file_path = os.path.join(output_dir, f"{device_name}_config.txt")
            
            # Save the configuration text inside the file
            with open(file_path, 'w') as file:
                file.write(config_output)
                
            print(f"Successfully saved {device_name} configuration to {file_path}")
            
            # Close the SSH connection
            net_connect.disconnect()

        # Catch timeout errors (e.g., device offline)
        except NetmikoTimeoutException:
            print(f"Timeout error: {device_name} is unreachable. Skipping to next device.")
            
        # Catch authentication errors (e.g., wrong password)
        except NetmikoAuthenticationException:
            print(f"Authentication failed for {device_name}. Check credentials. Skipping.")
            
        # Catch any other unexpected errors so the whole program doesn't crash
        except Exception as e:
            print(f"An unexpected error occurred with {device_name}: {e}")

    # Print a final message when all rows in the Excel file have been processed
    print("\nBackup process completed. All devices processed.")

# This ensures the main() function only runs if this script is executed directly
if __name__ == "__main__":
    main()