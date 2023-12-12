# import requests

domain = "https://www.mr-jatt.im"
page_url = "https://www.mr-jatt.im/punjabi-music/cat/a/1/Punjabi.html"
import re
import requests
from bs4 import BeautifulSoup


songsDownloaded = 0
page_response = requests.get(page_url).text
page_soup = BeautifulSoup(page_response, 'html.parser')
#get all the album links
for album_url in page_soup.findAll('a',href=re.compile('/punjabi-music/album/')):
    print ("album:", album_url['href'])
    album_response = requests.get(domain+album_url['href']).text
    album_soup = BeautifulSoup(album_response, 'html.parser')

    for link in album_soup.findAll('a',href=re.compile('/punjabi-music/song/')):
        song_link = link.get('href')
        print(song_link)
        
        full_song_link = domain + song_link
        #print(full_song_link)

        song_response = requests.get(full_song_link).text
        song_soup = BeautifulSoup(song_response, 'html.parser')
        
        links = [a['href'] for a in song_soup.find_all('a',href=re.compile('http.*\.mp3'))]
        highest_quality_link = links[-1]
        #download the song
        song_name = highest_quality_link.split('/')[-1]
        print("Downloading song: ", song_name)
        r = requests.get(highest_quality_link, allow_redirects=True)
        open("songs/" + song_name, 'wb').write(r.content)
        print("Downloaded song: ", song_name)
        songsDownloaded += 1

print("All songs downloaded: ", songsDownloaded)