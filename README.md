# PyTikTokScraper

### Requirements
You need to install `mutagen` via pip.

##

### Usage
`python3 -m pytiktokscraper --download whatthefish69`

Use `--download` to specify an username whose TikToks to download. (If using uid as input you must also pass `-uid`)

Use `--recent` alongside `--download` to only download the most recent 10 videos in the user feed.

Use `--single` to download a video with a given Id as argument (e.g. `--single 3e7da006d9234b198b554a0eb7a0b86f`)

Use `--livestream` to download an user's ongoing livestream (e.g. `--livestream whatthefish69`). This feature is untested.

Create a file called `settings.ini` in the repository folder with the following format:

```ini
[ptts]
username = johndoe
password = grapefruits
download_path = C:\path\to\download_folder
```

