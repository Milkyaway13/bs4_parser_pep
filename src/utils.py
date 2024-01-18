import logging

from bs4 import BeautifulSoup
from requests import RequestException
from exceptions import ParserFindTagException
from constants import ENCODING_CONST


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = ENCODING_CONST
        return response
    except RequestException:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )


def find_tag(get_response, tag, attrs=None):
    searched_tag = get_response.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f"Не найден тег {tag} {attrs}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def make_soup(session, url):
    try:
        response = session.get(url)
        response.encoding = ENCODING_CONST
        return BeautifulSoup(response.text, features="lxml")
    except RequestException:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )
