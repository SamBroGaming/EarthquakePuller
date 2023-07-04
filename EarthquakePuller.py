from bs4 import BeautifulSoup
import requests
import time

caching_var = ""
mag_var = ""

while True:

    response = requests.get("https://www.emsc-csem.org/Earthquake/world/M2/?view=1").content #url pulls all magnitude 2 earthquakes globally from a feed

    soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8") #strips down the html

    latlon = soup.find_all(class_="tabev1") #contains latitude and longitude

    lat = str(latlon[0]) #assigns latitude
    lon = str(latlon[1]) #assigns longitude

    lat = float(lat[19:len(lat)-6]) #does some string manipulation to get the values of the latitude excluding html junk
    lon = float(lon[19:len(lon)-6]) #same for longitude

    latlonletter = soup.find_all(class_="tabev2") #has the letters for lat/lon (n, s, e, w) as well as the magnitudes for an earthquake

    lat_letter = str(latlonletter[0])
    lon_letter = str(latlonletter[1])
    mag = str(latlonletter[2]) #assigning the relevant values

    lat_letter = lat_letter[19:len(lat_letter)-7]
    lon_letter = lon_letter[19:len(lon_letter)-7]
    mag = mag[19:len(mag)-5] #more string manipulation to get rid of junk

    quakes = soup.find_all("a") 

    for i in range(len(quakes)):
        if str(quakes[i])[0:39] == '<a href="/Earthquake/earthquake.php?id=': #this finds the url pointing to the actual earthquake's data
            quakes = str(quakes[i])
            break

    quakes = quakes[10:46] #more string manipulation to clean up

    newest_quake = requests.get(F"https://www.emsc-csem.org/{quakes}").content #requests the data on the specific earthquake, rather than the list of earthquakes

    soup2 = BeautifulSoup(newest_quake, 'html.parser')

    date_time = soup2.find_all(class_="point2")
    date_time = date_time[2].next_element

    date = date_time.split('   ')[0] #first value of date_time has the data, second has the time

    time_of_day = date_time.split('   ')[1]

    city_and_pop = str(soup2.find_all(class_="point")[5].next_sibling.contents[1]) #finds 6th "point" since it contains the city and population values, then filters it to take the second one

    city_and_pop = city_and_pop[4:len(city_and_pop)-11].split(' / local time:', 1)[0] #more string manipulation to remove the " / local time:" as raw string is something like 214 km W of Temuco, Chile / pop: 238,000 / local time: 16:56:39.0 2023-03-14 and i only want the part before local time

    if int(city_and_pop.split(" km ")[0]) > 250:
        population = ''
        region = str(soup.find_all(class_="tb_region")[0]) #if the mearest major city is >250 km away, use the Flinn-Engdahl region instead
        region = region[33:len(region)-5]

    else:
        city = str(city_and_pop.split(' / ', 1)[0]) #otherwise use the values obtained earlier
        population = city_and_pop.split(' / ', 1)[1][5:] #this removes the text literally saying "pop: "

    if quakes != caching_var: #check if we have different results as before to check if the earthquake is different. If it is, update all values
        caching_var = quakes
        mag_var = mag
        try: #the try block attempts to upload the result of this code to a website in a specific format
            if population != '':
                print(F"Mag {mag} at latitude and longitude of ({lat}{lat_letter}, {lon}{lon_letter}) {city} which has a population of {population} people at {time_of_day}".encode().decode("utf-8"))
                data = {'earthquakes' : F"Mag {mag} at latitude and longitude of ({lat}{lat_letter}, {lon}{lon_letter}) {city} which has a population of {population} people at {time_of_day}".encode().decode("utf-8")}
                post_request = requests.post(url = "https://developers.force-13.com/publish_eq.php", data = data)
            else:
                print(F"Mag {mag} at latitude and longitude of ({lat}{lat_letter}, {lon}{lon_letter}) at {region} at {time_of_day}".encode().decode("utf-8"))
                data = {'earthquakes' : F"Mag {mag} at latitude and longitude of ({lat}{lat_letter}, {lon}{lon_letter}) at {region} at {time_of_day}".encode().decode("utf-8")}
                post_request = requests.post(url = "https://developers.force-13.com/publish_eq.php", data = data)
        except Exception as e:
            print(F"Earthquake text failed to load: https://www.emsc-csem.org/{quakes}")
    
    if quakes == caching_var and mag != mag_var: #this is a check to see whether the magnitude updated. sometimes magnitudes update, so this prevents such a change from breaking my code and creating duplicates
        print(F"Earthquake revised to magnitude {mag}")
        mag_var = mag

    time.sleep(5) #pause the while loop for a little so it doesn't run too many times. can be changed based on desired frequency