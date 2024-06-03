#!venv/bin/python
# Created by lexkosha at 26.05.2024
import random
import time

from playwright.sync_api import sync_playwright, Page


class YaParserMap:
    # base_url: str = 'https://yandex.ru/maps/14/tver/chain/pyatyorochka/6003206/?ll=35.890582%2C56.855086&sll=35.890582%2C56.854725&sspn=0.242214%2C0.045331&z=12'
    base_url: str = 'https://yandex.ru/maps/14/tver/?ll=35.911851%2C56.859561&z=12'
    url_tver = 'https://yandex.ru/maps/14/tver/?ll=35.911851%2C56.859561&z=12'
    wait_text: str = "Добавьте организацию или объект, если не нашли их на карте."
    data: list = []

    def creates_a_sheet_with_dicts(self, page: Page):
        """Соберет данные из ul.search-list-view__list """
        search_elem = page.query_selector('ul')
        print(search_elem.text_content())
        elements = search_elem.query_selector_all('li.search-snippet-view')

        for element in elements:
            self.data.append(
                {
                    'coor': element.get_attribute('data-coordinates'),
                    'title': element.query_selector('.search-business-snippet-view__title').text_content(),
                    'working': element.query_selector('.business-working-status-view').text_content(),
                    'address': element.query_selector('.search-business-snippet-view__address').text_content(),

                }

            )
        print(self.data)
        return self.data

    @classmethod
    def __gen_timeout(cls, item: bool):
        """Генерирует случайное число в диапазоне max от 000 до 30000, min 2000 до 5000. return float"""
        if item:
            return float(random.randrange(2000, 3000))

        return float(random.randrange(5000, 30000))

    @classmethod
    def __arrow_down(cls, page: Page):
        """Скролит сайдбар в низ до последнего элемента"""
        timeout = cls.__gen_timeout(True)

        page.locator(".sidebar-view__panel").first.click()
        txt = page.locator('.scroll__content')

        while True:
            print('запускаем цикл строка 59 \n')


            if txt.get_by_text(cls.wait_text, exact=False)  == 'undefined':

                page.locator("body").press("ArrowDown", timeout=100.0)
            else:
                print('условие')

                break

    def page_maps_pars(self):
        """Взять данные со страницы"""
        timeout = self.__gen_timeout(True)

        with (sync_playwright() as pw):
            browser = pw.chromium.launch(
                headless=False,
                slow_mo=100,
                devtools=False,
                downloads_path='dw/',
                handle_sighup=True,

            )

            context = browser.new_context(
                locale='ru-RU',
                timezone_id='Europe/Moscow',
                geolocation={"longitude": 35.911851, "latitude": 56.859561},
                permissions=["geolocation"]
            )
            # playwright_spy.load_sync(context) не использовать, часто кидает на clout

            page = context.new_page()

            page.goto(self.base_url)
            page.wait_for_timeout(timeout)
            page.get_by_placeholder('Поиск мест и адресов').type(
                text='пятёрочка',
                delay=200.9)
            page.wait_for_timeout(timeout)
            page.get_by_placeholder('Поиск мест и адресов').press(
                "Enter",
                delay=100.0)
            page.wait_for_timeout(timeout)

            self.__arrow_down(page)
            self.creates_a_sheet_with_dicts(page)

        print('ok')
        time.sleep(4)


def main():
    inst = YaParserMap()
    inst.page_maps_pars()


if __name__ == '__main__':
    main()
    time.sleep(10)
