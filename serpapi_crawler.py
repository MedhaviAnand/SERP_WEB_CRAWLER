from serpapi import GoogleSearch
from pytube import YouTube
from pytube import Channel
import json
import os
import csv
from dotenv import load_dotenv, find_dotenv

load_dotenv(".env")
API_KEY=os.getenv("API")

def creation_of_modified_data():
    # Open the JSON file and load the data
    with open("output/data_raw.json") as file:
        data = json.load(file)

    # Create a list of dictionaries
    list_modified_links = []

    # Iterate through the loaded data
    for item in data:
        try:
            video_link = YouTube(str(item['Link']))
            Channel_URL = video_link.channel_url
            dict = {
                "Channel Title": item['Title'],
                "Video Link": item['Link'],
                "Channel Link": Channel_URL
            }
            list_modified_links.append(dict)
        except:
            dict = {
                "Channel Title": item['Title'],
                "Video Link": item['Link'],
                "Channel Link": item['Link']
            }
            list_modified_links.append(dict)

    # Write the modified data into a JSON file
    with open('output/data_modified_serpapi.json', 'w') as f:
        json.dump(list_modified_links, f)

    # Write the modified data into a CSV file
    keys = list_modified_links[0].keys()
    with open('output/data_modified_serpapi.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(list_modified_links)

def generate_raw_data(results):
  list_links=[]

  #iterate through the generated dictionary

  for result in results["organic_results"]:       
    dictionary={"Title": f"{result['title']}", "Link": f"{result['link']}"}
    list_links.append(dictionary)

  if(os.path.exists(os.path.join(os.getcwd(), 'output'))):
     with open('output/data_raw.json', 'w') as f:
      json.dump(list_links, f)
  else:
    os.mkdir(os.path.join(os.getcwd(), 'output'))
    with open('output/data_raw.json', 'w') as f:
      json.dump(list_links, f)


#Parameters to be passed to the SerpAPI
parameters = {
  "engine": "google",
  "num": "10000", #number of results
  "q": "site:youtube.com openinapp.co", #query to be sent
  "google_domain": "google.com",
  "gl": "us",
  "hl": "en",
  "location": "Austin, Texas, United States",
  "api_key": f"{API_KEY}"
}


if __name__=='__main__':
  search = GoogleSearch(parameters)
  results = search.get_dict()
  generate_raw_data(results)
  creation_of_modified_data()