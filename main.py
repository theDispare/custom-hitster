import spotipy
import requests
import io
import re
from sympy.abc import x
from PIL import Image, ImageDraw, ImageFont, ImageOps
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

#
client_id = 'XXXX'
client_secret = 'XXXX'
redirect_uri = 'https://localhost:8888/callback'

#playlists pl = my custom selected playlist https://open.spotify.com/playlist/6AeFzelGKQQWNDP9ONzOa7
pl = '6AeFzelGKQQWNDP9ONzOa7'
test = 'https://open.spotify.com/playlist/2b4MCNj1TwVyMuprvbjNcM?si=51da7a8390774ac4'


# scope = "user-library-read"
# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

path = "out/"

#get tracks from playlist. there could be multiple "pages" depending on playlist size
results = spotify.playlist_tracks(test)
tracks = results['items']
while results['next']:
    results = spotify.next(results)
    tracks.extend(results['items'])

#create a years.txt file with years and number of songs for each year. only for playlist creation control
dict = {} 
for track in tracks:
    song = track['track']
    year = song['album']['release_date'][:4]
    if year in dict: dict[year] = dict[year] + 1
    else: dict[year] = 1
# sorted_dict = sorted(dict.items(), key=lambda item: item[1], reverse=True)
sorted_dict = sorted(dict.items())
#print(sorted_dict)
with open(path+"years.txt", "w") as txt_file:
    for line in sorted_dict:
        txt_file.write((str(line[0])+ " "+str(line[1])) + "\n") # works with any number of elements in a line
txt_file.close()

#create a tracklist.txt file with years and song name and interpret, sorted by year. only for playlist creation control
tracklist = []
for track in tracks:
    song = track['track']
    title = song['name']
    if re.search("Remaster", title):
            title = title.split("-")[0].rstrip()
    artists = ""
    for artist in song['artists']:        
        if artists == "":
            artists = artist['name']
        else: 
            artists = artists + ", " +  artist['name']
    year = song['album']['release_date'][:4]
    out = str(year)+ " "+ artists+ " - "+ title
    tracklist.append(out)
    tracklist.sort()
with open(path+"tracklist.txt", "w") as txt_file:
    for line in tracklist:
        print(str(line))
        txt_file.write((str(line)) + "\n") # works with any number of elements in a lin
txt_file.close()

#helper function to split text in two parts based on input width of a text object
def wrap_text(message :str, width :int , font :ImageFont.FreeTypeFont):
    wrap_width = 500
    if font.getbbox(message)[2] > width - 20: 
        a = message.split()
        l = len(a)
        i = 0
        lhalf = ""
        rhalf = ""
        for s in a:
            if i < l/2:
                lhalf += " " + s
            else: rhalf += " " + s
            i += 1
    else: 
        lhalf = message
        rhalf = ""
    return lhalf, rhalf

#helper function to clean tiles
def clean_title(title :str):
    if re.search("Remaster", title):
        title = title.split("-")[0].rstrip()
    if re.search("Version", title):
        title = title.split("-")[0].rstrip()
    if re.search("Mono", title):
        title = title.split("-")[0].rstrip()
    if re.search("\d{4}\sRemast", title):
        print("found:" + title)
        title = re.sub(r'\(\d{4}\s.*\)', '', title)
    return title


page_width, page_height = int(2480), int(3508) # A4 at 300dpi
page_front = Image.new('RGB', (page_width, page_height), 'white')
page_back = Image.new('RGB', (page_width, page_height), 'white')
w , h = (int(600), int(600))
margin = int(150)
spacing = int(50)

#start values
images_row, images_column = (1, 1)

# images_row_coords = [int]
# images_column_coords = [int]
# c = page_width - margin - w 


#calculates how many "cards" can be created on one page regarding the above settings
current_w = w
while current_w < page_width - 2*margin:
    if current_w + w + spacing < page_width - 2*margin:
        current_w = current_w + w + spacing
        images_column += 1
    else: break
      
current_h = h
while current_h < page_height - 2*margin:
    if current_h + h + spacing < page_height - 2*margin:
        current_h = current_h + h + spacing
        images_row += 1
    else: break

print("Rows: " + str(images_row) + " Columns: " + str(images_column))

page_count = 1
pdf = "final.pdf"
pages = []
firstpage = None

i = 0
cx, cy = (int(margin), int(margin))
current_row = 1
current_column = 1
border = 10
font = ImageFont.truetype("font/bold.ttf", 200)
font_small = ImageFont.truetype("font/bolditalic.ttf", 45)
fix = 3

songlist = []

#logic for creating a "card"
for track in tracks:
    song = track['track']
    title = song['name']
    title = clean_title(title)
    artists = ""
    for artist in song['artists']:        
        if artists == "":
            artists = artist['name']
        else: 
            artists = artists + ", " +  artist['name']
    year = song['album']['release_date'][:4]
    id = song['id']

    #custom fixes. some songs just deliver the wrong information. mostly the year is wrong due to wrong releases in spotify. 
    if title == "The River": 
        year = "2007"
        artists = "Good Charlotte, M. Shadows"
    if title == "That's Amore": year = "1953"
    if title == "Mr. Sandman": year = "1954"
    if title == "Johnny B. Goode": year = "1955"
    if title == "Shout, Pt. 1": title = "Shout"
    if title == "House of the Rising Sun": year = "1964"
    if title == "Careless Whisper": year = "1984"
    if title == "Great Balls Of Fire": year = "1957"
    if title == "Oh, Pretty Woman": year = "1964"
    if title == "California Dreamin'": year = "1965"
    if title == "Love Me Do": year = "1962"
    if title == "Itsy Bitsy Teenie Weenie Honolulu Strand Bikini": year = "1960"
    if title == "Ich liebe das Leben": year = "1975"
    if title == "I Get Around": year = "1964"
    if title == "Downtown": year = "1964"
    if title == "Zu spät": year = "1985"
    if title == "GOSSIP (feat. Tom Morello)":
        title = "Gossip"
        artists = "Måneskin"
    if title == "You Make Me Feel Like It’s Halloween": title = "You Make Me Feel Like It's Halloween"
    if title == "Irgendwie, irgendwo, irgendwann": year = "1984"


    _, _, wa, ha = font_small.getbbox(artists)
    _, _, wt, ht = font_small.getbbox(title)

    #create empty images
    backimage = ImageOps.expand(Image.new("RGB", (w,h), (255, 255, 255)), border=border)
    spotify_code = ImageOps.expand(Image.new("RGB", (w,h), (255, 255, 255)), border=border)

    #get spotify codes for the song
    response = requests.get("https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2FFFFFFF%2Fblack%2F"+str(w)+"%2Fspotify%3Atrack%3A" + id)
    if response.status_code == 200:
        response_image = Image.open(io.BytesIO(response.content))

        #paste spotify code on card
        spotify_code.paste(response_image, (0+border, int((h/2)-(response_image.size[1]/2))))
        #spotify_code.save(str(i)+".jpeg")

        #paste year on card
        backimage_draw = ImageDraw.Draw(backimage)
        backimage_draw.text((w/2, h/2), year, (0,0,0), font=font, anchor="mm", align="center")

        #paste title and artist on card and wrap them in multiple lines if they are too long
        current_h = 0
        write_title = []
        if font.getbbox(artists)[2] > w - 20:
            write_artists = wrap_text(artists, w, font_small)
        else: 
            write_artists = [artists]
            
        if font.getbbox(title)[2] > w - 20:
            write_title = reversed(wrap_text(title, w, font_small))
        else:
            write_title = [title]

        #top artist
        for line in write_artists:
            backimage_draw.text((w/2, current_h+ha+5), line, (0,0,0), font=font_small, anchor="mm", align="center")
            current_h += ha

        #bottom title
        current_h = h
        for line in write_title:
            if line == "": continue
            backimage_draw.text((w/2, current_h-ht-5), line, (0,0,0), font=font_small, anchor="mm", align="center")
            current_h -= ht

        #backimage.save(str(i)+".png")

        #place card onto its correct place in the page. checking rows and columns
        if current_column <= images_column:
            page_front.paste(spotify_code, (cx, cy))
            page_back.paste(backimage, (page_width-w-(border)-cx-fix, cy))
            cx += spacing + w
            current_column += 1
        else:
            if current_row <= images_row:
                current_row += 1
                cy += spacing + h
                cx = margin
                current_column = 1
                page_front.paste(spotify_code, (cx, cy))
                page_back.paste(backimage, (page_width-w-(border)-cx-fix, cy))
                cx += spacing + w
                current_column += 1
                
        print(i, " " ,"done: ", title, " by ", artists, " ", year)        
        songlist.append(year + " " + title + " by " + artists)
    else:
        print(response.status_code)

    #check if current page is full AND append completed page to final pdfs
    i += 1
    if i % (images_row * images_column) == 0:
        if page_count == 1:
            firstpage = page_front
            pages.append(page_back)
            print("First to pages")
        else:
            pages.append(page_front)
            pages.append(page_back)
            print("add page: " + str(page_count))
        page_count += 1
        page_back.save(path+"_"+str(page_count-1)+".jpg")
        page_front = Image.new('RGB', (page_width, page_height), 'white')
        page_back = Image.new('RGB', (page_width, page_height), 'white')
        cx, cy = (int(margin), int(margin))
        current_row = 1
        current_column = 1

#check if there are more than 1 page and create PDF
if firstpage is None:
    pages.append(page_back)
    page_front.save(path+pdf, "PDF", resolution=100.0, save_all=True, append_images=pages)
    page_back.save(path+"_"+str(1)+".jpg")
else:
    pages.append(page_front)
    pages.append(page_back)
    firstpage.save(path+pdf, "PDF", save_all=True, append_images=pages)
    page_back.save(path+"_"+str(page_count-1)+".jpg")

#development purpose #similar to tracklist but after songs were corrected.
with open(path+"songlist_sorted.txt", "w") as txt_file:
    for s in sorted(songlist):
        txt_file.write((str(s)) + "\n") # works with any number of elements in a lin
txt_file.close()
