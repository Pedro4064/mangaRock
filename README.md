# mangaRock 

* A quick module to get the name of all your favorited manga in [mangaRock](https://mangarock.com) and save it to a file.


#### Quick Examples 

```python
from manga import mangaRock

manga  = mangaRock(driverPath = 'path/to/webdriver', username = 'username@gmail.com', password = 'yourPassword')
manga.getFavorites(importFavorites = True)
```
- `driverPath` is the path to the chrome webdriver on your machine;<br/>
- `username` and `password` are the ones for the mangarock website;<br/>
- In the `manga.getFavorites()` there is the option to import`(importFavorites = True)` to the web the favorite mangas from you other devices. To do so:<br/>
  `On iOS: Open More → Import & Export Data For Web`<br/>
  `On Android: Open More → Import & Export Data For Web`<br/>
#### Python
* Python3 or greater;<br/> 
* It uses os, time, and selenium webdriver.<br/> 
  
  - To download them you can use:<br/> 
     `python3.X -m pip install -r /path/to/requirements.txt`

#### Chrome Driver

  * You also need to download [chromedriver](http://chromedriver.chromium.org/downloads) to use with selenium module.<br/> 
  * If you are on the raspberry pi, follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/). <br/> 