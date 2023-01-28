#!/usr/bin/python3

import requests
import re
from iso3166 import countries

base_url = "https://storage.googleapis.com/29f98e10-a489-4c82-ae5e-489dbcd4912f/"
url = base_url
openaip_index = ""

while True:
    response = requests.get(url)
    xml_data = response.text
    openaip_index += response.text

    # Search for the NextMarker tag in the XML data
    next_marker = None
    match = re.search(r'<NextMarker>(.*?)</NextMarker>', xml_data)
    if match:
        next_marker = match.group(1)
    if next_marker is None:
        break

    url = f"{base_url}?marker={next_marker}"

contents = re.findall(r'<Contents>(.*?)</Contents>', openaip_index)
for content in contents:
    key = re.search(r'<Key>(.*?)</Key>', content)
    if key.group(1).__contains__(".cup"):
      updatedate = re.search(r'<LastModified>(.*?)</LastModified>', content)
      countrycode = key.group(1)[0:2]
      print("name=OpenAip-" + key.group(1)) 
      print("uri=" + base_url + key.group(1)) 
      print("type=waypoint")
      if key.group(1).__contains__("hgl.cup"):
         print("description=" + "OpenAIP Hang gliding sites for " + countries.get(countrycode).name)
      elif key.group(1).__contains__("hot.cup"):
         print("description=" + "OpenAIP Thermal hotspots for " + countries.get(countrycode).name)
      elif key.group(1).__contains__("nav.cup"):
         print("description=" + "OpenAIP Navaids for " + countries.get(countrycode).name)
      elif key.group(1).__contains__("obs.cup"):
         print("description=" + "OpenAIP Obstacles for " + countries.get(countrycode).name)
      elif key.group(1).__contains__("rpp.cup"):
         print("description=" + "OpenAIP Reporting points for " + countries.get(countrycode).name)
      elif key.group(1).__contains__("apt.cup"):
         print("description=" + "OpenAIP Airports for " + countries.get(countrycode).name)
      else:
         print("description=")

      print("area=" + key.group(1)[0:2])
      print("update=" + updatedate.group(1)[0:10]) 
      print('')

    if key.group(1).__contains__("asp.txt"):
      updatedate = re.search(r'<LastModified>(.*?)</LastModified>', content)
      print("name=OpenAip-" + key.group(1)) 
      print("uri=" + base_url + key.group(1)) 
      print("type=airspace")
      print("description=" + "OpenAIP Airspace for " + countries.get(countrycode).name)
      print("area=" + key.group(1)[0:2])
      print("update=" + updatedate.group(1)[0:10]) 
      print('')
