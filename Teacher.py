"""
Code to be run by Teacher for receiving screen
"""

# Imports
import ScreenShareLibrary_Receiver as ss
import json


# Main Functions
def Teacher(hosts, ports):
    '''
    Teacher
    '''
    ss.ScreenShareClient(hosts=hosts, ports=ports)

# Driver Code
# Get Data from config
TeacherConfig = json.load(open("TeacherConfig.json", "rb"))
StudentConfig = json.load(open("StudentConfig.json", "rb"))

# Update Data
ss.WIDTH_DISPLAY = TeacherConfig["WIDTH"]
ss.HEIGHT_DISPLAY = TeacherConfig["HEIGHT"]
ss.WIDTH_IN = StudentConfig["WIDTH"]
ss.HEIGHT_IN = StudentConfig["HEIGHT"]

# Run Transmitter
Teacher(hosts=TeacherConfig["HOSTS"], ports=TeacherConfig["PORTS"])