# youtubeAddToWatchlist
- This is a project that covers the need of whoever wants to add songs to his/her YouTube account
 
## Before executing you should
- install Python 3
- install Selenium using pip:
`C:\Users\Marialena\AppData\Local\Programs\Python\Python37-32\Scripts> .\pip install --upgrade pip`
`.\pip install selenium`
- add your youtube password in a environmental variable with the name "`YOUTUBE_PASSWORD`"
- add your youtube email address in another environmental variable with the name "`YOUTUBE_EMAIL`"
- after adding the variables make sure you will close and open again the terminal or editor you will execute the script from
- you should specify in the if statement at line 141 the conditions you want to add videos for. In my case the conditions were:
any video or entertainment company that contains a korean character
any video that doesnt contains a list of words: clip, behind the scene, performance, stage, practice, cam, instrumental, choreography, backstage, tv, preview, ep
- download [the ChromeDriver version for your operating system](http://chromedriver.chromium.org/downloads), unzip the executable, and place it in this folder

## Note
- the script runs twice each time, you can stop it the second time by pressing Ctrl + Z

## To execute
- open terminal
- navigate to folder of project    
- `python .\add_to_watchlist.py`
