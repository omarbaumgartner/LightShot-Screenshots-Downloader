import requests,time
import methods as m
import socket
from urllib3.connection import HTTPConnection
from random import randint
from time import sleep

downloadsDirectory, downloadable_urls_path, non_downloadable_urls_path, min_delay, max_delay = m.load_yaml()

m.init()

# ... Making the program resilient ( Avoid interruption of the program )
# # Avoid error : Connection reset by peer
# HTTPConnection.default_socket_options = (
#     HTTPConnection.default_socket_options + [
#         (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
#         (socket.SOL_TCP, socket.TCP_KEEPIDLE, 45),
#         (socket.SOL_TCP, socket.TCP_KEEPINTVL, 10),
#         (socket.SOL_TCP, socket.TCP_KEEPCNT, 6)
#     ]
# )

# Creating session
session = requests.Session()
# Added a User-Agent otherwise it would'nt be retrieved
session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})

startingTime = int(round(time.time()))

# Opening the list of already used urls
with open(downloadable_urls_path, 'r') as ListFile:
    ExistingList = ListFile.read().split("\n")
# Opening the list of non-existing urls
with open(non_downloadable_urls_path, 'r') as ListFile:
    NonExistingList = ListFile.read().split("\n")


def main():
    count = 0 # Downloads counter
    while(True):
        # LightShot url has 6 caracters ( a-z and 0-9 )
        RandomUrl = m.RandomUrl()
        # Checking if generated URL is already known
        ExistingPathComparisonBool = m.CompareUrl(ExistingList, RandomUrl)
        NonExistingPathComparisonBool = m.CompareUrl(NonExistingList, RandomUrl)
        # If it's already known, we generate a new URL
        while(ExistingPathComparisonBool == True & NonExistingPathComparisonBool == True):
            RandomUrl = m.RandomUrl()
            ExistingPathComparisonBool = m.CompareUrl(ExistingList, RandomUrl)
            NonExistingPathComparisonBool = m.CompareUrl(NonExistingList, RandomUrl)
        
        # Sending an HTML GET Request to LightShow's website to retrieve its HTML page.
        url = 'https://prnt.sc/'+RandomUrl
        content = session.get(url)
        # Retrieving the portion of URL which defines the screenshot
        ImageUrl = m.GetImageUrl(content.text)
        # Return false if the portion isn't found
        if(filename == False):
            print(RandomUrl,"not existing")
            NonExistingList.append(ImageUrl)
            # Adding the useless URL in a list.
            with open(non_downloadable_urls_path, 'a') as nonExistingListFile:
                nonExistingListFile.write(RandomUrl+"\n")
        else:
            ExistingList.append(ImageUrl)
            # Adding the already used URL in a list.
            with open(downloadable_urls_path, 'a') as ExistingListFile:
                filename = ImageUrl.split('/')[-1]
                
                # Download image --------
                
                # Getting image
                r = requests.get(ImageUrl, allow_redirects=True)
                
                #  Downloading file into directory
                open(downloadsDirectory+'/'+filename, 'wb').write(r.content)
                
                """
                TODO : 
                - Make the program only fetch correct urls without downloading them
                - Add a method to directly download the images from the existinglist ( and download only the images that are not already in the directory ) 
                - make ExistingList hosted online ( via google drive api ) to have only one single list ( even if using different machines ) 
                """
                # -------

                ExistingListFile.write(RandomUrl+"\n")
                count = count+1
                #actualTime = int(round(time.time()))
                # How much screenshots per second you're downloading
                #ratio = count / (actualTime-startingTime)
                #print("Speed : ", ratio, "img/s")
                print("Downloaded (", count, ")")        
        sleep(randint(min_delay, max_delay))

def CheckExistingFiles():
    # Checking if the list of files in existingList.txt are existing in Downloads directory
    with open(downloadable_urls_path, 'r') as ListFile:
        ExistingList = ListFile.read().split("\n")
    for url in ExistingList:
        filename = url
        # check if url.* exists in directory
        if m.CheckIfFileExists(downloadsDirectory+'/'+filename) == False:
            print("File",filename,"not in directory")
            url = 'https://prnt.sc/'+url
            filename = download_image(url)
            sleep(randint(min_delay, max_delay))
        else:
            print("File",filename," in directory")

def download_image(url):
    content = session.get(url)
            # Retrieving the portion of URL which defines the screenshot
    ImageUrl = m.GetImageUrl(content.text)
            # Return false if the portion isn't found
    if(ImageUrl == False):
        print(url," URL not existing")
        return False
    else:
                # Getting image
        r = requests.get(ImageUrl, allow_redirects=True)
                #  Downloading file into directory
        filename = ImageUrl.split('/')[-1]
        open(downloadsDirectory+'/'+filename, 'wb').write(r.content)
        print("Downloaded")
        return filename


def save_url(url):
    with open(downloadable_urls_path, 'a') as ExistingListFile:
        ExistingListFile.write(url+"\n")

def save_nonexisting_url(url):
    with open(non_downloadable_urls_path, 'a') as nonExistingListFile:
        nonExistingListFile.write(url+"\n")


if __name__ == "__main__":
    # Remove duplicates in existingList.txt and nonexistingList.txt
    m.RemoveDuplicates()
    # Checking if the list of files in existingList.txt are existing in Downloads directory
    CheckExistingFiles()

    main()