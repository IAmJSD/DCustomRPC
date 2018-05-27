[![Build Status](https://travis-ci.org/JakeMakesStuff/DCustomRPC.svg?branch=master)](https://travis-ci.org/JakeMakesStuff/DCustomRPC)

# DCustomRPC: The Rewrite!

DCustomRPC is a custom rich presence client that you (you right there, yes you) can customize.

![intro_img](https://i.imgur.com/8Pf5HjT.png)

## Setting up the config:
The config should be fairly easy to setup:
1. Firstly go to Discord Developers (https://discordapp.com/developers/applications/) and sign in.
2. From here, click the "New App" button and enter a "App Name". This will show as what you are playing. "App Description" and "App Icon" do not matter for rich presence.
3. After this, you should be on the application page. Scroll down and click "Enable Rich Presence" and then "Save Changes".
4. After you have done this, you can copy the "Client ID" (under "App Details") and replace the client_id already in the config file.
5. To setup the game list, we will need to seperate each of the games by a "-" with the spacing from the config for the dashes and the remaining keys. Each game can contain the following:
    - `details` - This is the shorter description for the game:

        ![details](https://i.imgur.com/9Z7OdfI.png)
    - `state` - This is the longer description for the game:

        ![state](https://i.imgur.com/i1YbCfd.png)
    - `large_image` - The image key for the large image on the game. In order to attach your image to a key, open up your Discord Developers page for your app and scroll down to "Rich Presence Assets". From here, since we want a large image, we upload the image, enter the key (which we will write in the config) and select "Large". Then make sure to click "Upload Asset" and "Save Changes". After we add to the config, this will look like this:

        ![lg_image](https://i.imgur.com/KbQdc61.png)
    - `large_text` - This will be the text for when you hover over the large image:

        ![lg_text](https://i.imgur.com/nNRHtxo.png)
    - `small_image` - The image key for the small image on the game. In order to attach your image to a key, open up your Discord Developers page for your app and scroll down to "Rich Presence Assets". From here, since we want a small image, we upload the image, enter the key (which we will write in the config) and select "Small". Then make sure to click "Upload Asset" and "Save Changes". After we add to the config, this will look like this:

        ![sm_image](https://i.imgur.com/wjo0Nkx.png)
    - `small_text` - This will be the text for when you hover over the small image:

        ![sm_text](https://i.imgur.com/EApOnTl.png)

## Setting up DCustomRPC:
DCustomRPC requires Python 3.6+. If you have anything older installed, you will need to install Python 3.6+ and make sure it is added to the PATH. From here, you can run `py -m pip install -r requirements.txt` (the `py` bit might change to `python3.5`/`python3.6`, try that if you can't get that to work).

On Windows to set this to start on boot, simply take the `dcustomrpc.pyw`, right click it, hover over "Send to" then click "Desktop (create shortcut)". Then cut the icon from your desktop, go to `shell:startup` in Windows Explorer and paste it in there.
