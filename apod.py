import nasapy
import os
from datetime import datetime
import urllib.request

#For API
try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"

#Initialize nasa class by creating an object:
nasa = nasapy.Nasa(key=SOME_SECRET)

# Get current date
apod_date = datetime.today().strftime('%Y-%m-%d')
                                             
#Get information
apod = nasa.picture_of_the_day(date=apod_date, hd=True)

#Get another one if its not an image
while apod["media_type"] != "image":
    # Generate a random date
    apod_date = random_date(start, end).strftime('%Y-%m-%d')                                 
    #Get information
    apod = nasa.picture_of_the_day(date=apod_date, hd=True)

#Removes image and log every run
try:
    os.remove("Astro_Images/image.jpg")
    os.remove("Astro_Images/image_log.txt")
except OSError:
    pass
    
#Saving name for image:
title = "image.jpg"

#Path of the directory:
image_dir = "Astro_Images"

#Checking if the directory already exists?
dir_res = os.path.exists(image_dir)

#If it doesn't exist then make a new directory:
if (dir_res==False):
  os.makedirs(image_dir)

#Writing in log
with open("Astro_Images/image_log.txt", "a") as f:
  if("date" in apod.keys()):
    print("<br />**Date image released:** ", apod["date"], file=f)
  if("copyright" in apod.keys()):
    print("<br />**This image is owned by:** ", apod["copyright"], file=f)
  if("title" in apod.keys()):
    print("<br />**Title of the image:** ", apod["title"], file=f)
  if("explanation" in apod.keys()):
    print("<br />**Description for the image:** ", apod["explanation"], file=f)
  if("hdurl" in apod.keys()):
    print("<br />**URL for this image:** ", apod["hdurl"], file=f)

#Saving the image:
urllib.request.urlretrieve(url = apod["hdurl"], filename = os.path.join(image_dir, title))
