# LightShot-screenshots-downloader
A python program that retrieves screenshots that LightShot users had done
1. Install dependencies
2. Run program.py
LightShot is a website that lets users do screenshots and upload it on their platform to make it easier to share them.
Links have this structure : https://prnt.sc/ar3341 , so basically https://prnt.sc/[6 characters of letters and numbers]
The program will : 
1. generate a random combinaison
2. check if the link actually exists
3. If it does, it will be written in the existinglist.txt, if not, it would go to nonexistinglist.txt
This will avoid to use an already generated combination.
4. When the screenshot exists, it will donwload it into a specific folder.
