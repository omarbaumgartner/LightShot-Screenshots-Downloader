import random
import string


def RandomUrl():
    letters = string.ascii_lowercase
    number = string.digits
    return ''.join(random.choice(letters+number) for i in range(6))


def CompareUrl(UrlList, NewUrl):
    return NewUrl in UrlList


def GetImageUrl(text):
    index = text.find("https://i.imgur.com/")
    if(index == -1):
        return False
    else:
        endindex = index+31
        url = text[index:endindex]
        return url
