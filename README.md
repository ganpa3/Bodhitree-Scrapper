# Bodhitree-Scrapper
A simple script to notify about pending quizzes and download Bodhitree videos!

This script uses Chrome version 88. If you have some other version, then download it's driver from the below link and place it in the assets folder.
https://sites.google.com/a/chromium.org/chromedriver/downloads

If you want to use any other browser, download the driver from the below links.

- **Safari** : Safari’s executable is located at /usr/bin/safaridriver
- **Firefox** : https://github.com/mozilla/geckodriver/releases
- **Opera** : https://github.com/operasoftware/operachromiumdriver/
- **Edge** : https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
- **Internet Explorer** : Really?

# Usage
Selenium is required for the script to run. You can install it with ```pip install selenium```

NOTE: Actual number of quizzes keep changing, so the output isn't 100% accurate all the time. You can keep track of the "balanced" dictionary in the bt-scrapper.py file of this repo to see the changes.

Clone the repo.
```sh
git clone https://github.com/ganpa3/Bodhitree-Scrapper.git
```

Provide your credentials in the bt-scrapper.py file.

Use the command below to run program.

```
python bt-scrapper.py 
```

To download a Bodhitree video, use the command
```
python btv.py *url*
```
