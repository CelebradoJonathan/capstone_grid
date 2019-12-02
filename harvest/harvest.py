import requests
from requests import get
import re
import configparser
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import harvest_database as db

config = configparser.ConfigParser()
conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
config.read(conf_dir)
password = config['args']['password']
hostname = config['args']['hostname']
username = config['args']['username']
dbname = config['args']['dbname_harvest']
base_url = config['args']['base_url']


def parse_link(link):
    url = link
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, 'lxml')
    return soup


def download_file(url, filename):
    with open("{}{}{}{}{}".format(os.path.abspath(os.path.dirname(__name__)),
                                  os.sep, "downloads", os.sep, filename), "wb") as file:
        response = get(url)
        file.write(response.content)


def get_all_downloadable(download_page_link):
    soup = parse_link(download_page_link)
    download_links = soup.find_all("a", {"class": "downloadline"})
    acceptable_ext = ["exe", "zip"]
    downloadable_files = []
    for file in download_links:
        file_link = file.get("href")
        if file_link.split(".")[-1] in acceptable_ext:
            download_link = urljoin(download_page_link, file_link)
            downloadable_files.append(download_link)
            download_file(download_link, download_link.rsplit("/", 1)[-1])
    return downloadable_files


def check_version(download_page_link):
    name_version = get_details(download_page_link)
    if db.select_details(username, password, hostname, dbname, name_version):
        db.insert_details(username, password, hostname, dbname, name_version)
        get_all_downloadable(download_page_link)
        return True
    else:
        return False


def get_details(download_page_link):
    soup = parse_link(download_page_link)
    version_regex = "v[0-9]*\.[0-9]*"
    details = soup.find(text=re.compile(version_regex))
    name_version = details.split("-")[0]
    index = re.search(version_regex, name_version)
    name = name_version[0:index.start()].replace("\n", "")
    version = name_version[index.start():].replace("\n", "")
    return {"name": name, "version": version}


def check_translations(translations):
    if db.select_translations(username, password, hostname, dbname, translations):
        download_link = translations['language']
        version = translations['version']
        download_file(download_link, version + download_link.rsplit("/", 1)[-1])
        db.insert_translations(username, password, hostname, dbname, translations)


def get_translations(download_page_link):
    different_links = ["http://54.174.36.110/utils/internet_explorer_cookies_view.html"]
    if download_page_link not in different_links:
        soup = parse_link(download_page_link)
        identifier = soup.find_all("tr", class_="utiltableheader")[-1]
        table = identifier.find_parent("table")
        row = table.find_all("tr")[1:]  # [1:] to disregard the table header
        translations = []
        for item in row:
            language = item.find_all("td")[0].find("a").get("href")
            version = item.find_all("td")[-1].text.replace("\n", "")
            translation_details = {"language": urljoin(download_page_link, language),
                                   "version": version}
            check_translations(translation_details)
            translations.append(translation_details)
        return translations


def get_links():
    soup = parse_link(base_url)
    unordered_list = soup.find("ul")
    index_links = unordered_list.find_all("a", href=True)
    for link in index_links:
        href = link.get("href")
        if "http" not in href and db.select_links(username, password, hostname, dbname, href):
            db.insert_links(username, password, hostname, dbname, href)  # checker of link duplicates

    return db.select_all_links(username, password, hostname, dbname)


def upload_to_api(url, filename):
    file = {'file': open(filename, 'rb')}
    response = requests.post(url, files=file)


def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]


def get_downloaded_files():
    url = "http://127.0.0.1:5000/filelog/"
    path = "./downloads"
    files = listdir_fullpath(path)
    for file in files:
        upload_to_api(url, file)
    return files


def main():
    for pages in get_links():
        download_page_link = urljoin(base_url, pages)
        check_version(download_page_link)
        get_translations(download_page_link)

    get_downloaded_files()
    # print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # print(os.path.abspath(os.path.dirname(__file__)))


if __name__ == '__main__':
    main()
