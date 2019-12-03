import requests
from requests import get
import re
import configparser
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import harvest_database as db
import logging.config
import yaml

config = configparser.ConfigParser()
conf_dir = os.path.join(os.path.dirname(__file__), 'conf.ini')
config.read(conf_dir)
password = config['args']['password']
hostname = config['args']['hostname']
username = config['args']['username']
dbname = config['args']['dbname_harvest']
port = config['args']['port']
base_url = config['args']['base_url']


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration from a yaml file.
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)

    else:
        logging.basicConfig(level=default_level)


def parse_link(link):
    resource = requests.get(link)
    soup = BeautifulSoup(resource.text, 'lxml')
    return soup


def download_file(url, filename):
    with open("{}{}{}{}{}".format(os.path.abspath(os.path.dirname(__name__)),
                                  os.sep, "downloads", os.sep, filename), "wb") as file:
        response = get(url)
        file.write(response.content)
        logger.info("Downloaded {}".format(filename))


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
    if db.select_details(username, password, hostname, dbname, port, name_version):
        db.insert_details(username, password, hostname, dbname, port, name_version)
        logger.info("Inserted app {} with version {} to db".format(name_version["name"], name_version["version"]))
        get_all_downloadable(download_page_link)
        return True
    else:
        return False


def get_details(download_page_link):
    soup = parse_link(download_page_link)
    version_regex = r"v[0-9]*\.[0-9]*"
    details = soup.find(text=re.compile(version_regex))
    name_version = details.split("-")[0]
    index = re.search(version_regex, name_version)
    name = name_version[0:index.start()].replace("\n", "")
    version = name_version[index.start():].replace("\n", "")
    return {"name": name, "version": version}


def check_translations(translations):
    if db.select_translations(username, password, hostname, dbname, port, translations):
        download_link = translations['language']
        version = translations['version']
        download_file(download_link, version + download_link.rsplit("/", 1)[-1])
        db.insert_translations(username, password, hostname, dbname, port, translations)
        logger.info("Inserted {} to db".format(translations))


def get_translations(download_page_link):
    different_links = ["http://54.174.36.110/utils/"
                       "internet_explorer_cookies_view.html"]
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
        if "http" not in href and db.select_links(username, password, hostname, dbname, port, href):
            db.insert_links(username, password, hostname, dbname, port, href)  # checker of link duplicates
            logger.info("Inserted {} to db".format(href))
    return db.select_all_links(username, password, hostname, dbname, port)


def upload_to_api(url, filename):
    file = {'file': open(filename, 'rb')}
    response = requests.post(url, files=file)
    logger.info("Uploaded {} to {}".format(filename, url))
    return response.status_code


def listdir_fullpath(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory)]


def get_downloaded_files():
    url = "http://apicon:8000/filelog/"
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


if __name__ == '__main__':
    setup_logging()
    logger = logging.getLogger(__name__)
    main()

