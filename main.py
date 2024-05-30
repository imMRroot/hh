#!venv/bin/python
# Created by lexkosha at 26.05.2024
import random
import time

import playwright
from bs4 import BeautifulSoup
from loguru import logger
from playwright.sync_api import sync_playwright


def create_soup_obj(html_doc):
    """Создает объект bs4"""
    soup = BeautifulSoup(html_doc, 'lxml')
    return soup


class YaParserMap:
    # base_url: str = 'https://yandex.ru/maps/14/tver/chain/pyatyorochka/6003206/?ll=35.890582%2C56.855086&sll=35.890582%2C56.854725&sspn=0.242214%2C0.045331&z=12'
    base_url: str = 'https://yandex.ru/maps/14/tver/?ll=35.911851%2C56.859561&z=12'
    url_tver = 'https://yandex.ru/maps/14/tver/?ll=35.911851%2C56.859561&z=12'

    @classmethod
    def __gen_timeout(cls, item: bool):
        """Генерирует случайное число в диапазоне max от 000 до 30000, min 2000 до 5000. return float"""
        if item:
            return float(random.randrange(2000, 5000))

        return float(random.randrange(5000, 30000))

    @classmethod
    def __sidebar_scroll_duration(cls, page: playwright):
        """Вернет True если 1 значение '490px' прекратило увеличиваться в translate3d(0px, 490px, 0px)"""
        checks_value = page.locator('.scroll__scrollbar-thumb')

    @classmethod
    def __arrow_down(cls, page: playwright):
        """Скролит сайдбар в низ до последнего элемента"""
        timeout = cls.__gen_timeout(True)
        for _ in range(30):  # TODO: Подумать о автоматическом кол-во итераций рассмотреть page.wait_for_selector
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.wait_for_timeout(timeout)
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")
            page.locator("body").press("ArrowDown")

    @logger.catch
    def page_maps_pars(self):
        """Взять данные со страницы"""
        timeout = self.__gen_timeout(True)

        with sync_playwright() as pw:
            browser = pw.chromium.launch(
                headless=False,
                slow_mo=100,
                devtools=False,
                downloads_path='dw/',
                handle_sighup=True,

            )

            context = browser.new_context()
            # playwright_spy.load_sync(context) не использовать, часто кидает на clout
            page = context.new_page()

            page.goto(self.base_url)
            page.wait_for_timeout(timeout)
            page.get_by_placeholder("Поиск мест и адресов").click()
            page.wait_for_timeout(3300.0)
            page.get_by_placeholder("Поиск мест и адресов").fill("пятерочка", timeout=timeout)
            page.get_by_placeholder("Поиск мест и адресов").press("Enter")

            page.wait_for_timeout(timeout)

            page.locator(".sidebar-view__panel").first.click()

            page.wait_for_timeout(timeout)

            self.__arrow_down(page)
            elem = page.query_selector(".sidebar-view__panel")

            tag_li = elem.query_selector('.search-list-view__list')
            page.pause()


            with open('page_ya.html', 'a', encoding='UTF-8') as f:
                f.writelines(tag_li.input_value())

        # waite_elem = page.wait_for_selector(f':text("Добавьте организацию или объект, если не нашли их на карт")')

        # page.locator("body").press("ArrowDown")
        # page.get_by_text("Добавьте организацию или объект, если не нашли их на карте").click()
        #

        # with open('page_ya.html', 'a', encoding='UTF-8') as f:
        #     f.write(page.content())

        print('ok')
        time.sleep(4)


def main():
    inst = YaParserMap()
    inst.page_maps_pars()


if __name__ == '__main__':
    main()
    time.sleep(10)

