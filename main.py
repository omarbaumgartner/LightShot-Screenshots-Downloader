import requests,time,env
import methods as m

m.init()

count = 0 # Downloads counter
startingTime = int(round(time.time()))

# Opening the list of already used urls
with open(env.existingUrlsFileName, 'r') as ListFile:
    ExistingList = ListFile.read().split("\n")
# Opening the list of non-existing urls
with open(env.nonexistingUrlsFileName, 'r') as ListFile:
    NonExistingList = ListFile.read().split("\n")

# Creating session
session = requests.Session()
# Added a User-Agent otherwise it would'nt be retrieved
session.headers.update(
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    

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
    content = session.get('https://prnt.sc/'+RandomUrl)
    
    # Retrieving the portion of URL which defines the screenshot
    ImageUrl = m.GetImageUrl(content.text)
    
    # Return false if the portion isn't found
    if(ImageUrl == False):
        NonExistingList.append(ImageUrl)
        # Adding the useless URL in a list.
        with open(env.nonexistingUrlsFileName, 'a') as nonExistingListFile:
            nonExistingListFile.write(RandomUrl+"\n")
    else:
        ExistingList.append(ImageUrl)
        # Adding the already used URL in a list.
        with open(env.existingUrlsFileName, 'a') as ExistingListFile:
            filename = ImageUrl.split('/')[-1]
            # Getting image
            r = requests.get(ImageUrl, allow_redirects=True)
            # Downloading file into directory
            open(env.downloadsDirectory+'/'+filename, 'wb').write(r.content)
            ExistingListFile.write(RandomUrl+"\n")
            count = count+1
            actualTime = int(round(time.time()))
            # How much screenshots per second you're downloading
            ratio = count / (actualTime-startingTime)
            print("Speed : ", ratio, "img/s")
            print("Downloaded (", count, ")")
