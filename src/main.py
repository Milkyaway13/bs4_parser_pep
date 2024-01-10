import logging
import re
import requests_cache

from urllib.parse import urljoin
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, EXPECTED_STATUS, LXML, MAIN_DOC_URL,
                       PATTERN_DOWNLOAD, PATTERN_LATEST_VERSION, PEP_DOC_URL)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features="lxml")

    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})

    sections_by_python = div_with_ul.find_all(
        "li", attrs={"class": "toctree-l1"}
    )

    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        version_link = urljoin(whats_new_url, version_a_tag["href"])
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, "lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    results = [("Ссылка на документацию", "Версия", "Статус")]
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, "lxml")
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    print(ul_tags)
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Ничего не нашлось")

    results = []
    pattern = PATTERN_LATEST_VERSION

    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, "lxml")
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag, "a", {"href": re.compile(PATTERN_DOWNLOAD)}
    )
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
    filename = archive_url.split("/")[-1]

    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")

    with open(archive_path, "wb") as file:
        file.write(response.content)


def pep(session):
    response = get_response(session, PEP_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features=LXML)
    section_tag = find_tag(soup, "section", attrs={"id": "numerical-index"})
    tbody_tag = find_tag(section_tag, "tbody")
    tr_tags = tbody_tag.find_all("tr")

    dict_for_result = {
        "Accepted": 0,
        "Active": 0,
        "Deferred": 0,
        "Draft": 0,
        "Final": 0,
        "Provisional": 0,
        "Rejected": 0,
        "Superseded": 0,
        "Withdrawn": 0,
        "Total": 0,
    }

    for tr in tqdm(tr_tags):
        status_in_table = EXPECTED_STATUS[find_tag(tr, "abbr").text[1:]]
        pep_link = find_tag(tr, "a")["href"]
        pep_page = urljoin(PEP_DOC_URL, pep_link)
        response = session.get(pep_page)
        soup = BeautifulSoup(response.text, features=LXML)
        dl_tag = find_tag(soup, "dl")
        pre_status = dl_tag.find(string="Status")
        status_in_pep_page = pre_status.find_next("dd").text

        if status_in_pep_page not in status_in_table:
            logging.info(
                f"{pep_page}\n"
                f"Статус в карточке: {status_in_pep_page}\n"
                f"Ожидаемые статусы: {status_in_table}\n"
            )
        if status_in_pep_page not in dict_for_result:
            continue
        dict_for_result[status_in_pep_page] += 1
        dict_for_result["Total"] += 1

    results = [("Статус", "Количество")]
    for status, quantity in dict_for_result.items():
        results.append((status, quantity))

    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)
    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
