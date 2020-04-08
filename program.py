# Don't forget to install the modules below
import requests
import methods as m
import time

# Downloads counter
count = 0
startingTime = int(round(time.time()))
# Opening the list of paths of existing and already downloaded screenshots
with open('existinglist.txt', 'r') as ListFile:
    UrlList = ListFile.read().split("\n")
# Opening the list of paths of non-existing screenshots
with open('notyetlist.txt', 'r') as ListFile:
    NotYetUrlList = ListFile.read().split("\n")

while(True):
    # LightShot url has 6 caracters ( a-z and 0-9 )
    print("Generating a random url..")
    RandomUrl = m.RandomUrl()
    ExistingPathComparisonBool = m.CompareUrl(UrlList, RandomUrl)
    NonExistingPathComparisonBool = m.CompareUrl(NotYetUrlList, RandomUrl)
    while(ExistingPathComparisonBool == True & NonExistingPathComparisonBool == True):
        RandomUrl = m.RandomUrl()
        ExistingPathComparisonBool = m.CompareUrl(UrlList, RandomUrl)
        NonExistingPathComparisonBool = m.CompareUrl(NotYetUrlList, RandomUrl)
    # Sending a request to LightShow to retrieve its HTML file.
    # Added a User-Agent otherwise it would'nt be retrieved
    session = requests.Session()
    session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})

    content = session.get('https://prnt.sc/'+RandomUrl)
    # Retrieving the portion of URL which defines the screenshot
    ImageUrl = m.GetImageUrl(content.text)
    # Return false if the portion isn't found
    if(ImageUrl == False):
        print("Url does not exist..")
        NotYetUrlList.append(ImageUrl)
        # Adding the useless URL in a list.
        with open('notyetlist.txt', 'a') as the_file:
            the_file.write(RandomUrl+"\n")
    else:
        UrlList.append(ImageUrl)
        # Adding the already used URL in a list.
        with open('existinglist.txt', 'a') as the_file:
            the_file.write(RandomUrl+"\n")
            filename = ImageUrl.split('/')[-1]
            # Getting image
            r = requests.get(ImageUrl, allow_redirects=True)
            # Downloading
            open('Downloaded/'+filename, 'wb').write(r.content)
            count = count+1
            actualTime = int(round(time.time()))
            # How much screenshots/s you are downloading
            ratio = count / (actualTime-startingTime)
            print("Speed : ", ratio, "img/s")
            print("Downloaded (", count, ")")
