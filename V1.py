import requests
import csv
import os.path
from os import path
import time
import json

# Set up API endpoint and parameters
url = 'https://ll.thespacedevs.com/2.0.0/launch'
filename = 'launch_data.csv'

# Check if CSV file already exists
if path.exists(filename):
    # Open CSV file in append mode
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Don't write header row if file already exists
        write_header = False
else:
    # Open CSV file in write mode and write header row
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Launch ID', 'Mission Name', 'Launch Date', 'Location', 'Launch Pad', 'Rocket', 'Mass', 'Thrust', 'Diameter', 'Height', 'Apogee', 'Maximum Stages', 'Minimum Stages', 'Status'])
        write_header = True

# Loop to fetch new launch data every hour
while True:
    # Send GET request to API and convert response to JSON format
    response = requests.get(url)
    launches = response.json()["results"]

    # Extract launch data from JSON response and save to CSV file
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header row if file was just created
        if write_header:
            writer.writerow(['Launch ID', 'Mission Name', 'Launch Date', 'Location', 'Launch Pad', 'Rocket', 'Mass', 'Thrust', 'Diameter', 'Height', 'Apogee', 'Maximum Stages', 'Minimum Stages', 'Status'])
            write_header = False
        for launch in launches:
            launch_id = launch['id']
            mission_name = launch['name']
            launch_date = launch['net']
            location = launch['pad']['location']['name']
            launch_pad = launch['pad']['name']
            status = launch['status']['name']

            # Get launcher data
            rocket_id = launch['rocket']['configuration']['id']
            rocket_response = requests.get(f'https://ll.thespacedevs.com/2.0.0/config/launcher/{rocket_id}/')
            rocket_data = rocket_response.json()

            # Check if the required keys exist in the JSON response before accessing their values
            if 'launch_mass' in rocket_data:
                liftoff_mass = rocket_data['launch_mass']
            else:
                liftoff_mass = 0
                
            if 'to_thrust' in rocket_data:
                liftoff_thrust = rocket_data['to_thrust']
            else:
                liftoff_thrust = 0
                
            if 'diameter' in rocket_data:
                diameter = rocket_data['diameter']
            else:
                diameter = 0
                
            if 'length' in rocket_data:
                height = rocket_data['length']
            else:
                height = 0

            if 'apogee' in rocket_data:
                Apogee = rocket_data['apogee']
            else:
                Apogee=0
            
            if 'max_stage' in rocket_data:
                max_stages = rocket_data['max_stage']
            else:
                max_stages=0
            
            if 'min_stage' in rocket_data:
                min_stage = rocket_data['min_stage']
            else:
                min_stage=0

            if 'name' in rocket_data:
                Rocket=rocket_data['name']
            else:
                Rocket=0

            writer.writerow([launch_id, mission_name, launch_date, location, launch_pad, Rocket, liftoff_mass, liftoff_thrust, diameter, height, Apogee, max_stages, min_stage, status])

#Turn the csv file into a list of dictionaries
with open('launch_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    launch_data = []
    for row in reader:
        launch_data.append(row)

   
    # Wait for an hour before fetching new launch data
    time.sleep(3600)
