import googleapiclient.discovery
import numpy
import os
import re
import bs4
import json
import requests
from requests_html import AsyncHTMLSession
from pip._vendor import requests

# grab the title of single video
def get_title(url):
    this_id = re.search("v=(.*?)&", url+'&', re.M|re.I).group(1)
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyBc_c3SVM8AMVp9SIUvanuLTiumk-MXneM")
    request = youtube.videos().list(
        part = "snippet",
        id = this_id)
    return request.execute()["items"][0]['snippet']['title']

# grab the title and url of playlist
def grab_playlist(url,maxima_song = 25):

    playlist_id = re.search("list=(.*?)(?:&|$)", url, re.M|re.I).group(1)
    print(playlist_id)
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "AIzaSyBc_c3SVM8AMVp9SIUvanuLTiumk-MXneM")
    request = youtube.playlistItems().list(
        part = "snippet",
        playlistId = playlist_id,
        maxResults = maxima_song
    )
    response = request.execute()
    playlist_items = []
    Total_number   = 0
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)
        Total_number += 1
        if (Total_number == maxima_song):
            break
    playlist_set = []
    for i in playlist_items:
        this_set = (
            i['snippet']['title'],
            f"https://www.youtube.com/watch?v={i['snippet']['resourceId']['videoId']}"
            )
        playlist_set.append(this_set)
    return playlist_set

async def grab_Lyrics_spotify(song_name):


    search_url = f"https://cse.google.com/cse?cx=partner-pub-9427451883938449%3Agd93bg-c1sx&q={song_name}#gsc.tab=0&gsc.q={song_name}&gsc.page=1"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    print("[*] Start Web grabing")
    session = AsyncHTMLSession()
    r =  await session.get(search_url)
    await r.html.arender(scrolldown = 4 , sleep = 0.1)
    print("[*] Finish Web grabing")

    output = ""
    get_all_url = r.html.xpath("//a[@class='gs-title']")
    get_links = list(get_all_url)#[0]
    print(f"[*] Found {len(get_links)} result")
    Found = False
    for each in get_links: 
        each_links = list(each.links)
        if (len(each_links) == 0): continue

        Lyrics_r  = requests.get(each_links[0],headers= headers).content
        soup      = bs4.BeautifulSoup(Lyrics_r,"lxml")

        find_ly   = soup.find_all("div",id="kanji")
        if (len(find_ly) !=0):
            Found = True
            output = output + "Song name : "+each.text + "\n"
            for i in find_ly:
                output = output + i.text.replace(" "," ").replace("Lyrics from Animelyrics.com","")
                output = output + "\n\n"
            break

        find_ly   = soup.find_all("td",class_="romaji")
        if (len(find_ly) !=0):
            Found = True
            output = output + "Song name : "+each.text + "\n\n\n"
            for i in find_ly:
                output = output + i.text.replace(" "," ").replace("Lyrics from Animelyrics.com","")
                output = output + "\n\n"
            break

    output = output + "Lyrics from Animelyrics.com\n"
    return Found, output

if __name__ == "__main__":
    # pass
    # print(
    #     grab_playlist(r"https://www.youtube.com/watch?v=vWpc7f6b9kA&list=RDvWpc7f6b9kA&start_radio=1")
    #     )

    print(get_title('https://www.youtube.com/watch?v=mnta9Pp2LqA'))
    # import asyncio
    # loop2 = asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()
    # forecast = loop.run_until_complete(
    #     grab_Lyrics_spotify("在泥濘中綻放")
    #     )
    # print(forecast[1])
