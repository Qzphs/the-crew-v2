Task generator GUI for playing [The Crew](https://boardgamegeek.com/boardgame/284083/the-crew-the-quest-for-planet-nine)
in person.

## Setup

You will need [Python](https://www.python.org/downloads/) installed.

On the GitHub page, click the green **Code** button, then click
**Download ZIP**. Unzip this on your computer.

The folder should contain a file called **main.py**. Open it using **IDLE**
(this is Python's code editor) and select **Run > Run Module**.


## Player Icons

If you want to add your own player icons, you can add them directly to the
**players** folder. The code automatically looks for any PNG files in that
folder. All images need to be 128x128 or it will look weird in the GUI.

I normally grab people's profile pictures from Discord. If you want to do this:

1. Open Discord in browser (not desktop app).
2. Inspect element on user's profile picture.
3. Find the link to the image. It should look something like this: `https://cdn.discordapp.com/avatars/266998099954630656/502a37508d49f545fe4eb871fb2c5a0a.webp?size=128`
4. Open that link in another browser tab (should see the avatar appear on screen).
5. Change the ending to `.png?size=128`.
6. Save image.
