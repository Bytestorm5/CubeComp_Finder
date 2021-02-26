# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Imports
import requests
from math import sin, cos, sqrt, atan2, radians, pi
from bs4 import BeautifulSoup
import urllib.request
import tkinter
#*********************************

# Variables
home_lat = radians(float(40.3794466))
home_lon = radians(float(-74.3051806))
url= "https://www.worldcubeassociation.org/competitions.html?region=USA"
#****************************************************************************
# Functions
def get_comp_date(whatever):
    return whatever.find('dd').text
def get_comp_address(whatever):
    return whatever.find('a').text
def get_comp_distance(home_lat, home_lon, comp_lat, comp_lon):
    comp_lat = radians(comp_lat)
    comp_lon = radians(comp_lon)
    
    R = float(6371.0)
    dlon = comp_lon - home_lon
    dlat = comp_lat - comp_lat
    a = sin(dlat/2) * sin(dlat/2) + cos(radians(home_lat)) * cos(radians(comp_lat)) * sin(dlon/2) * sin(dlon/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = float(R * c * 0.621371)
    return distance
def get_comp_link(complink):
    return "https://www.worldcubeassociation.org" + complink + ".html"

def send_email(message):
    # Import smtplib for the actual sending function
    import smtplib
    
    # Import the email modules we'll need
    from email.mime.text import MIMEText

    # Create a text/plain message
    msg = MIMEText(str(message))
    
    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'Upcoming Competitions as of [DEBUG]'
    msg['From'] = 'naila.firdaus@gmail.com'
    msg['To'] = 'kamil.m.arif@gmail.com'
    
    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.send_message(msg)
    s.quit()

#*****************************************************************************

#****************************
# Lists
master_list = list()
shown_comps = list()

# Check if connection is working.
response = requests.get(url)
if response.status_code == 200:
    
    print("Connected to WCA servers")
    
    # Acess Competition Main Page
    results_page = BeautifulSoup(response.content,'lxml')
    maincomplinks = results_page.findAll('div','competition-link')
    print("Found Competitions")
    # Repeat for every Competition link
    for maincomplink in maincomplinks:
        maincomplink = maincomplink.find('a').get('href')

        # Access Individual Competition page
        compurl = "https://www.worldcubeassociation.org" + maincomplink + ".html"       
        compresponse = requests.get(compurl)
        comp_page = BeautifulSoup(compresponse.content,'lxml')
        comp_info = comp_page.find('div', 'row competition-info')
        
        print("Accessed individual competition page")
        
        # Find all links on page
        comp_info_a_tags = comp_info.findAll('a')
        
        # Loop for every link on the page
        for comp_info_a_tag in comp_info_a_tags: 
            
            # If the link is a google maps link
            if (comp_info_a_tag.get('href').startswith("https://www.google.com/maps/place")):
                
                # Get Competition coordinates
                location_href = comp_info_a_tag.get('href')
                
                # Split Coordinates into Latitude and Longitude
                comp_lat = float(location_href.split("/")[5].split(',')[0])
                comp_lon = float(location_href.split("/")[5].split(',')[1])
            
                comp_list = list()

                # Append Competition info to list
                comp_list.append(get_comp_date(comp_info))
                comp_list.append(get_comp_address(comp_info))
                comp_list.append(round(get_comp_distance(home_lat, home_lon, comp_lat, comp_lon), 2))
                comp_list.append(get_comp_link(maincomplink))

                #Append competition list to the master_list
                master_list.append(comp_list)


    for comp in master_list:
        # Parameters
        d = 250
        
        # END Parameters
        if (float(comp[2]) <= float(d)):
            shown_comps.append(comp)
    print(shown_comps)
    
    print("Writing information to file...")
    
    f = open('data.xml', 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('<comps>')
    
    for comp in master_list :
        f.write('<comp>')
        f.write('<date>' + comp[0] + '</date>')
        f.write('<venue>' + comp[1] + '</venue>')
        f.write('<distance> ' + str(comp[2]) + '</distance>')
        f.write('<link> ' + str(comp[3]) + '</link>')
        f.write('</comp>')
    
    f.write('</comps>')
    f.close()
    
    
    print("Data transferred to local drive")
#    send_email(shown_comps)
    
            
else:
    print("Connection Failure: Check internet connection")

        
        
