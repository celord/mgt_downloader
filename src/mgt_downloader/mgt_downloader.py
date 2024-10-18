import requests
from . import constants as const
from . import util
import argparse
import curlify
import sys


def add_magnet_to_real_debrid(config, magnet_link, headers):
    url = const.REAL_DEBRID_ADD_MAGNET_URL
    payload = {'magnet': magnet_link}

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code ==201:
        torrent_info = response.json()
        torrent_id = torrent_info['id']
        print(f"Torrent added to Real Debrid with ID: {torrent_id}")
        return torrent_id
    else:
        print(f"Error adding torrent to Real Debrid: {response.status_code}, {response.text}")
        return None

def select_files_and_start_download(config, torrent_id, headers, files):
    url = const.REAL_DEBRID_SELECT_FILES_URL + "/" +torrent_id
    headers = {'Authorization' : 'Bearer ' + config[const.REAL_DEBRID_OAUTH_ACCESS_TOKEN]}
    payload = {'files': "all"}
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 204:
        print(f"Files selected for torrent {torrent_id}")
        return True
    else:
        print(f"Error selecting files for torrent {torrent_id}: {response.status_code}, {response.text}")
        return False


def get_files_id(config, torrent_id, headers):
    url = const.REAL_DEBRID_GET_FILE_IDS_URL + "/" + torrent_id
    response = requests.get(url, headers=headers)
    request = curlify.to_curl(response.request)
    torrent_info = response.json()
    files = torrent_info['files']
    print(f"Files available forn torrent:  {torrent_id}")
    for file in files:
        print(f"File ID: {file['id']}, Filename: {file['path']}, Size: {file['bytes']}")
        return files
    else:
        print(f"Error fetching file list: {response.status_code}, {response.text}")
        return []




def get_download_links(torrent_id):
    url = f'https://api.real-debrid.com/rest/1.0/torrents/info/{torrent_id}'

    response = requests.get(url)
    if response.status_code == 200:
        torrent_info = response.json()
        download_links = [file['link'] for file in torrent_info['links']]
        return download_links
    else:
        print(f"Error fetching download links: {response.status_code}, {response.text}")
        return []


def main(raw_args=None):
    parser = argparse.ArgumentParser(description='Download a torrent from Real Debrid')
    parser.add_argument('magnet_link', help='The magnet link of the torrent to download')
    args = parser.parse_args()
    config = util.get_config()
    headers = {'Authorization' : 'Bearer ' + config[const.REAL_DEBRID_OAUTH_ACCESS_TOKEN]}
    magnet_link = args.magnet_link
    torrent_id = add_magnet_to_real_debrid(config, magnet_link, headers)
    files = get_files_id(config, torrent_id, headers)
    select_files_and_start_download(config, torrent_id, headers, files)
    print('Download started')

if __name__ == '__main__':
    sys.exit(main())

