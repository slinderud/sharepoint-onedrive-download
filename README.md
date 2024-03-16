# sharepoint-onedrive-download

Wrapper around wrapper for rclone to download files from shared onedrive folders with password.
Probably has some bugs

```sh
python3 download.py --help
Usage: download.py [OPTIONS]

Options:
  -o, --outFolder TEXT  Folder where files should end up  [required]
  -p, --password TEXT   Password for shared onedrive  [required]
  -u, --url TEXT        Link to sharepoint/onedrive site  [required]
  --help                Show this message and exit.
```

```sh
python3 download.py -u https://x.sharepoint.com/:f:/g/personal/y/a?e=f -p supersecretpassword -o testdownload
```

Code inspired and borrowed from
* https://github.com/generalizable-neural-performer/gnr/blob/main/genebody/download_tool.py
* https://github.com/axzxc1236/pySharepointDownloader/blob/main/downloader.py
* https://github.com/Loli-Killer/python-aria-mirror-bot/blob/master/bot/custom_mirrors/onedrive_mirror.py
