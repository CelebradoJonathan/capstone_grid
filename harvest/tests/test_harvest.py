from ..harvest import *
from ..harvest_database import *


def test_establish_connection():
    connection = establish_connection("postgres", "pgijtsaMS", "localhost", "harvestdb", "5432")
    assert connection


def test_parse_link():
    soup = parse_link("http://54.174.36.110/")
    assert soup


def test_get_all_downloadable():
    download_links = get_all_downloadable("http://54.174.36.110/utils/web_browser_password.html")
    assert isinstance(download_links, list)
    assert download_links


def test_check_version():
    version = check_version("http://54.174.36.110/utils/web_browser_password.html")
    assert isinstance(version, bool)


def test_get_translations():
    translations = get_translations("http://54.174.36.110/utils/web_browser_password.html")
    assert isinstance(translations, list)
    assert len(translations) == 37


def test_get_links():
    links = get_links()
    assert isinstance(links, list)


def test_listdir_fullpath():
    files = listdir_fullpath("../downloads")
    assert isinstance(files, list)


def test_get_downloaded_files():
    files = get_downloaded_files()
    assert isinstance(files, list)