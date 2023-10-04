import random,string,os
import yaml

# Load params from params.yaml
def load_yaml():
    with open("params.yaml", 'r') as stream:
        try:
            params = yaml.safe_load(stream)
            downloadsDirectory = params['downloadsDirectory']
            downloadable_urls_path = params['downloadable_urls_path']
            non_downloadable_urls_path = params['non_downloadable_urls_path']
            min_delay = params['min_delay']
            max_delay = params['max_delay']
        
        except yaml.YAMLError as exc:
            print(exc)
    return downloadsDirectory,downloadable_urls_path,non_downloadable_urls_path,min_delay,max_delay

downloadsDirectory, downloadable_urls_path, non_downloadable_urls_path, min_delay, max_delay = load_yaml()

# Creating missing files and directory if needed
def init():
    if not (os.path.exists('./'+downloadable_urls_path)):
        print(downloadable_urls_path,": creating file.")
        open(downloadable_urls_path, "w")
    if not (os.path.exists('./'+non_downloadable_urls_path)):
        print(non_downloadable_urls_path,": creating file.")
        open(non_downloadable_urls_path, "w")
    if not (os.path.isdir(downloadsDirectory)):
        print(downloadsDirectory,": creating directory")
        os.makedirs(downloadsDirectory)

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
    with open(downloadable_urls_path, 'r') as ExistingListFile:
        ExistingList = ExistingListFile.read().split("\n")
    with open(non_downloadable_urls_path, 'r') as NonExistingListFile:
        NonExistingList = NonExistingListFile.read().split("\n")
    
    ExistingList = list(dict.fromkeys(ExistingList))
    NonExistingList = list(dict.fromkeys(NonExistingList))
    
    with open(downloadable_urls_path, 'w') as ExistingListFile:
        for url in ExistingList:
            ExistingListFile.write(url+"\n")
    with open(non_downloadable_urls_path, 'w') as NonExistingListFile:
        for url in NonExistingList:
            NonExistingListFile.write(url+"\n")
    print("Duplicates removed.")


