from django.shortcuts import render

# Create your views here.
import requests
import csv
import os
import pandas as pd

# Define the API URL and headers
BASE_URL = "https://pysoftware.com/v1"
API_KEY = "ssfdsjfksjdhfgjfgvjdshgvshgkjsdlgvkjsdgjkl"
HEADERS = {"X-API-KEY": API_KEY}

# Function to retrieve the total number of customers
def get_customer_count():
    url = f"{BASE_URL}/customer_numbers"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return int(response.text)  # Assuming the response is just the number
    else:
        raise Exception(f"Failed to get customer numbers: {response.status_code}")

# Function to retrieve the address for a given customer number
def get_customer_address(customer_number):
    url = f"{BASE_URL}/address_inventory/{customer_number}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # Returning the JSON data directly
    else:
        raise Exception(f"Failed to retrieve address for customer {customer_number}: {response.status_code}")

# Function to validate address data
def validate_address(address):
    # Check if the address fields are valid types and formats
    try:
        # Ensuring all the fields exist and have the correct types
        assert isinstance(address['id'], int)
        assert isinstance(address['first_name'], str)
        assert isinstance(address['last_name'], str)
        assert isinstance(address['street'], str)
        assert isinstance(address['postcode'], str)
        assert isinstance(address['state'], str)
        assert isinstance(address['country'], str)
        assert isinstance(address['lat'], (float, int))
        assert isinstance(address['lon'], (float, int))
        
        # Basic validations for fields that need specific formats (e.g., postcode, lat/lon)
        if len(address['postcode']) != 6:  # Example: valid postcode should be of length 6
            raise ValueError("Invalid postcode length.")
        if not (-90 <= address['lat'] <= 90):
            raise ValueError("Invalid latitude value.")
        if not (-180 <= address['lon'] <= 180):
            raise ValueError("Invalid longitude value.")
        
        return True  # If all checks pass, return True
    
    except (AssertionError, KeyError, ValueError) as e:
        print(f"Validation error for address ID {address.get('id', 'N/A')}: {e}")
        return False

# Function to write customer addresses to a CSV file
def write_addresses_to_csv(addresses, file_name):
    # Define the CSV fieldnames
    fieldnames = ["id", "first_name", "last_name", "street", "postcode", "state", "country", "lat", "lon"]
    
    # Write to CSV
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for address in addresses:
            writer.writerow(address)
    
    return file_path

# Main function to retrieve, clean, and save customer addresses
def get_all_customer_addresses():
    # Step 1: Get the total number of customers
    total_customers = get_customer_count()
    print(f"Total number of customers: {total_customers}")

    all_addresses = []
    
    # Step 2: Iterate over each customer number and retrieve their address
    for customer_number in range(1, total_customers + 1):
        try:
            # Fetch address for the current customer
            address = get_customer_address(customer_number)
            
            # Step 3: Validate and clean the address data
            if validate_address(address):
                all_addresses.append(address)
        
        except Exception as e:
            print(f"Skipping customer {customer_number} due to error: {e}")

    # Step 4: Write the cleaned addresses to a CSV file
    file_name = "customer_addresses.csv"
    file_path = write_addresses_to_csv(all_addresses, file_name)
    
    # Step 5: Display the CSV path and data in tabular form
    print(f"\nAddresses saved to: {file_path}")
    
    # Load the CSV file and display in tabular form using pandas
    df = pd.read_csv(file_path)
    print("\nCustomer Addresses:")
    print(df)

    return df

if __name__ == "__main__":
    # Run the main function
    get_all_customer_addresses()
