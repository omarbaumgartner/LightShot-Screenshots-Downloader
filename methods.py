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
