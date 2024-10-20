from django.shortcuts import render
import json
# Create your views here.


def validate_and_assign_serial_numbers(json_data):
    # Serial number range for valid serial numbers (1470 to 1478)
    serial_number_range = range(1470, 1479)
    
    # Ensure that the "Internet_hubs" key exists
    if "Internet_hubs" not in json_data:
        raise ValueError("Missing 'Internet_hubs' key in JSON data")
    
    # Copy the original list of internet hubs
    internet_hubs = json_data["Internet_hubs"]
    
    # Track serial number assignments
    serial_number_mapping = {str(i): f"C25CTW0000000000{serial}" for i, serial in zip(range(1, 10), reversed(serial_number_range))}
    
    # List to hold updated hubs
    updated_hubs = []
    
    # Loop through each internet hub and validate/assign serial numbers
    for hub in internet_hubs:
        if "id" not in hub or "serial_number" not in hub:
            raise ValueError(f"Hub {hub} does not have both 'id' and 'serial_number' keys")
        
        # Get the last digit of the id (assumes 'mn1', 'mn2', ... 'mn9')
        hub_id = hub["id"]
        if not hub_id.startswith("mn") or not hub_id[2:].isdigit():
            raise ValueError(f"Invalid hub id: {hub_id}")
        
        # Extract the number from the id
        id_last_digit = int(hub_id[2:])
        
        # Check if it's a valid id number between 1 and 9
        if 1 <= id_last_digit <= 9:
            # Assign the serial number based on the reverse order of ids
            hub["serial_number"] = serial_number_mapping[str(id_last_digit)]
        
        # Append the updated hub to the new list
        updated_hubs.append(hub)
    
    # Return both original and updated JSON objects
    return json_data, {"Internet_hubs": updated_hubs}

# Example JSON data to test
example_json = {
    "comment": "Do NOT commit local changes to this file to source control",
    "Internet_hubs": [
        {"id": "men1", "serial_number": "C25CTW00000000001470"},
        {"id": "mn1", "serial_number": "<serial number here>"},
        {"id": "mn2", "serial_number": "<serial number here>"},
        {"id": "mn3", "serial_number": "<serial number here>"},
        {"id": "mn4", "serial_number": "<serial number here>"},
        {"id": "mn5", "serial_number": "<serial number here>"},
        {"id": "mn6", "serial_number": "<serial number here>"},
        {"id": "mn7", "serial_number": "<serial number here>"},
        {"id": "mn8", "serial_number": "<serial number here>"},
        {"id": "mn9", "serial_number": "<serial number here>"}
    ]
}

# Testing the function
original_json, updated_json = validate_and_assign_serial_numbers(example_json)

# Print results
print("Original JSON:")
print(json.dumps(original_json, indent=4))
print("\nUpdated JSON:")
print(json.dumps(updated_json, indent=4))
