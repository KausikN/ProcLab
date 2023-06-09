"""
Code to be run by Student for transmitting screen
"""

# Imports
import ScreenShareLibrary_Transmitter as ss
import json


# Main Functions
def Student(host, port):
    '''
    Student
    '''
    ss.ScreenShareServer(host=host, port=port)

# Driver Code
# Get Data from config
config = json.load(open("StudentConfig.json", "rb"))

# Update Data
ss.WIDTH_OUT = config["WIDTH"]
ss.HEIGHT_OUT = config["HEIGHT"]

# Run Transmitter
Student(host=config["HOST"], port=config["PORT"])