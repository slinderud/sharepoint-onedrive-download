import requests
import re
import click
from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs
from rclone_python import rclone
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    SpinnerColumn,
    DownloadColumn,
)

def getCookiesWithPassword(link: str, password: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "lxml")
    viewstate = soup.find('input', {'id': '__VIEWSTATE'}).get('value')
    eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'}).get('value')
    linkParts = urlparse(link)
    new_url = f"https://{linkParts.hostname}/personal/{linkParts.path.split('/personal/')[1].split('/')[0]}/_layouts/15/guestaccess.aspx?share={linkParts.path.rsplit('/', 1)[1]}"
    body = {
        "txtPassword": password,
        "__EVENTVALIDATION": eventvalidation,
        "__VIEWSTATE": viewstate,
        "__VIEWSTATEENCRYPTED": ""
    }
    r = requests.post(new_url, data=body)

    params = parse_qs(urlparse(r.url).query)
    webAbsoluteUrlPattern = re.compile(r'"webAbsoluteUrl":"([^"]+)"')
    if match := webAbsoluteUrlPattern.search(r.text):
        webdavEndpoint = match.group(1) + "/" + "/".join(params["id"][0].split("/")[3:])
    return r, f"FedAuth={r.cookies.get_dict()['FedAuth']};", webdavEndpoint

@click.command("download")
@ click.option('--outfolder', '-o', required=True, help="Folder where files should end up")
@ click.option(
    '--password', '-p', required=True, help="Password for shared onedrive")
@ click.option(
    '--url', '-u', required=True, help="Link to sharepoint/onedrive site")
def main(outfolder, password, url):
    first_r, cookieString, webdavEndpoint = getCookiesWithPassword(url, password)
    fullEncodedPath = re.search("^.*?id=(.*?)&ga=1$", first_r.url).group(1)
    rootFolder = unquote(fullEncodedPath.rsplit("%2F", 1)[1])

    out = f"{outfolder}/{rootFolder}"

    pbar = Progress(
        TextColumn("[progress.description]{task.description}"),
        SpinnerColumn(),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(binary_units=True),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )

    with open("sharepoint_rclone.conf", mode="w") as f:
        f.write(f"[{rootFolder}]\n")
        f.write("type = webdav\n")
        f.write(f"url = {webdavEndpoint}\n")
        f.write("vendor = other\n")
        f.write(f"headers = Cookie,{cookieString}")

    Path(out).mkdir(parents=True, exist_ok=True)
    rclone.copy(f"{rootFolder}:", out, args=[' --config', 'sharepoint_rclone.conf'], pbar=pbar)

if __name__ == "__main__":
    main()