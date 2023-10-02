import random,string,os,env

# Creating missing files and directory if needed
def init():
    if not (os.path.exists('./'+env.existingUrlsFileName)):
        print(env.existingUrlsFileName,": creating file.")
        open(env.existingUrlsFileName, "w")
    if not (os.path.exists('./'+env.nonexistingUrlsFileName)):
        print(env.nonexistingUrlsFileName,": creating file.")
        open(env.nonexistingUrlsFileName, "w")
    if not (os.path.isdir(env.downloadsDirectory)):
        print(env.downloadsDirectory,": creating directory")
        os.makedirs(env.downloadsDirectory)

# Generating a random URL
def RandomUrl():
    letters = string.ascii_lowercase
    number = string.digits
    return ''.join(random.choice(letters+number) for i in range(6))

# Comparing generated URL with a list
def CompareUrl(UrlList, NewUrl):
    return NewUrl in UrlList

# Getting the URL of the image
def GetImageUrl(text):
    index = text.find("https://i.imgur.com/")
    if(index == -1):
        return False
    else:
        endindex = index+31
        url = text[index:endindex]
        return url

def CheckIfFileExists(filename):
    return os.path.isfile(filename)

# Removing duplicates from a list and returning the new list without duplicates and saved in a file
def RemoveDuplicates():
    with open(env.existingUrlsFileName, 'r') as ExistingListFile:
        ExistingList = ExistingListFile.read().split("\n")
    with open(env.nonexistingUrlsFileName, 'r') as NonExistingListFile:
        NonExistingList = NonExistingListFile.read().split("\n")
    
    ExistingList = list(dict.fromkeys(ExistingList))
    NonExistingList = list(dict.fromkeys(NonExistingList))
    
    with open(env.existingUrlsFileName, 'w') as ExistingListFile:
        for url in ExistingList:
            ExistingListFile.write(url+"\n")
    with open(env.nonexistingUrlsFileName, 'w') as NonExistingListFile:
        for url in NonExistingList:
            NonExistingListFile.write(url+"\n")
    print("Duplicates removed.")
