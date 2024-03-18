# sharepoint-onedrive-download

Wrapper around wrapper for rclone to download files from shared onedrive folders with password.
Probably has some bugs

```sh
$ python3 download.py --help
Usage: download.py [OPTIONS]

Options:
  -c, --config PATH              Path to config file
  -o, --outfolder TEXT           Folder where files should end up  [required]
  -p, --password TEXT            Password for shared onedrive  [required]
  -u, --url TEXT                 Link to sharepoint/onedrive site  [required]
  -m, --multi-threaded-download  Enable multi threaded download. Please see
                                 readme for bug info
  -f, --filter-file PATH         Rclone filter file
  --help                         Show this message and exit.
```

## Examples

### Command LIne

```sh
python3 download.py -u https://x.sharepoint.com/:f:/g/personal/y/a?e=f -p supersecretpassword -o testdownload
```

### Config File

```sh
$ cat config.yml
outfolder: testdownload
password: supersecretpassword
url: https://x.sharepoint.com/:f:/g/personal/y/a?e=f
filter_file: filter-file.txt.example

$ python3 download.py --config config.yml
```

### Environment Variables

```sh
DL_URL=https://x.sharepoint.com/:f:/g/personal/y/a?e=f DL_PASSWORD=supersecretpassword DL_OUTFOLDER=testdownload python3 download.py
```

### Known Bugs

* If multi threaded download is enabled, huge files won't finish (Goes beyond 100%).
  * Disabled by default, can be enabled using the `--multi-threaded-download` flag

## Credit

Code inspired and borrowed from

* https://github.com/generalizable-neural-performer/gnr/blob/main/genebody/download_tool.py
* https://github.com/axzxc1236/pySharepointDownloader/blob/main/downloader.py
* https://github.com/Loli-Killer/python-aria-mirror-bot/blob/master/bot/custom_mirrors/onedrive_mirror.py
