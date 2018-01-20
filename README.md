# DCustomRPC
DCustomRPC is a custom rich presence client that you (you right there, yes you) can customise. The only recommendation is that you know JSON.

![img1](https://i.imgur.com/5WjagYc.png)

## How do I configure this?
Simple! Open up `config.json` in a text editor and you will notice my configuration is there for an example. Simply go to https://discordapp.com/developers/applications/me, login and make a application with the name you want to show as the name of the game your are playing. Once you have done that, enable rich presence on the applcation by clicking `Enable Rich Presence` and then copy the application ID into the `application_id` field in the config.

Next you can adjust how many seconds before it updates to another activity by changing the `change_interval` in the configuration.

The next bit is the exciting part! Changing the list of games (`game_list`). It is a array of JSON, for which you can use the following values:

- `details` - The second thing that shows after the status.
- `state` - The description of the status.
- `largeImageKey` - The key for your large image. You can add images on the Discord Developers page under "Rich Presence Assets" and then the name is your key.
- `largeImageText` - The text when you hover over the large image.
- `smallImageKey` - The image that is under the large image. There is a good chance you do not want this second image, but you can add it if you want to. You can add the asset the same way as the large image.
- `smallImageText` - The text when you hover over the small image.

## I am done configuring. How do I set this thing up?
1. Install node.js
2. Run `npm i` in the folder you have this application in.
3. Run `node app.js`.

If you want it to start in the background, you can do the following:

1. Run `npm i pm2 -g` as administrator.
2. Type `pm2 start app.js --name="DCustomRPC"`.

Even though I have not tested, you can probably also make some sort of shortcut to a batch file running that to make it start on boot.
