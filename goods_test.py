import os
import re

from bs4 import BeautifulSoup

import request_tool as tool
from item_detail_tool import get_item_detail


def get_all_goods_item():
    base_url = 'https://myfigurecollection.net/?_tb=item&tags%5B%5D=higurashi_no_naku_koro_ni_series&rootId=1&page={}'

    page_1_html_text = tool.get_html_text(base_url.format(1))
    page_1_soup = BeautifulSoup(page_1_html_text, 'html.parser')
    title = page_1_soup.title.string
    match = re.search(r'Page \d+ of (\d+)', title)
    total_page_size = match.group(1)
    item_idx = 1
    for i in range(1, int(total_page_size) + 1):
        current_url = base_url.format(i)
        # time.sleep(random.randint(1, 4))
        html_text = tool.get_html_text(current_url)

        soup = BeautifulSoup(html_text, 'html.parser')
        # 找到所有class为item-icon的span标签
        item_icons = soup.find_all('span', class_='item-icon')
        # 遍历每个span标签，提取文本内容、a元素的href值、img元素的src值和alt值，并保存到字典中
        for idx, span in enumerate(item_icons, start=1):
            a_href = span.find('a')['href']  # 提取a元素的href值
            item_id = re.search(r'/item/(\d+)', a_href).group(1)
            get_item_html_by_item_id(item_idx, item_id)
            item_idx = item_idx + 1


def get_goods_html_text_by_keyword(key_word: str, category_id: int):
    url_key_word = key_word.replace(' ', '+')
    base_url = 'https://myfigurecollection.net/?_tb=entry&keywords={}&categoryId={}&page={}'
    first_page_html_text = tool.get_html_text(base_url.format(url_key_word, category_id, 1))
    first_page_soup = BeautifulSoup(first_page_html_text, 'html.parser')
    title = first_page_soup.title.string
    match = re.search(r'Page \d+ of (\d+)', title)
    total_page_size = int(match.group(1))
    for i in range(1, total_page_size + 1):
        current_url = base_url.format(url_key_word, category_id, i)
        html_text = tool.get_html_text(current_url)
        soup = BeautifulSoup(html_text, 'html.parser')
        search_results = soup.find_all('div', class_='result')
        for idx, result in enumerate(search_results, start=1):
            # 获取entry_id
            a = result.find('div', class_='stamp entry-stamp').find('a', class_='tbx-tooltip')
            entry_id = re.search(r'/entry/(\d+)', a['href']).group(1)
            entry_name = a.find('img')['alt']
            print('>>>>>>>>>>>>>>cur_entry id: {} name: {}'.format(entry_id, entry_name))
            get_item_html_by_entry(entry_id)


def get_item_html_by_entry(entry_id: int):
    base_url = 'https://myfigurecollection.net/?orEntries%5B%5D={}page={}&_tb=item&rootId=1'

    page_1_html_text = tool.get_html_text(base_url.format(entry_id, 1))
    page_1_soup = BeautifulSoup(page_1_html_text, 'html.parser')
    title = page_1_soup.title.string
    match = re.search(r'Page \d+ of (\d+)', title)
    total_page_size = match.group(1)
    item_idx = 1
    for i in range(1, int(total_page_size) + 1):
        current_url = base_url.format(entry_id, i)
        # time.sleep(random.randint(1, 4))
        html_text = tool.get_html_text(current_url)

        soup = BeautifulSoup(html_text, 'html.parser')
        # 找到所有class为item-icon的span标签
        item_icons = soup.find_all('span', class_='item-icon')
        # 遍历每个span标签，提取文本内容、a元素的href值、img元素的src值和alt值，并保存到字典中
        for idx, span in enumerate(item_icons, start=1):
            a_href = span.find('a')['href']  # 提取a元素的href值
            item_id = re.search(r'/item/(\d+)', a_href).group(1)
            item_name = span.find('img')['alt']
            get_item_html_by_item_id(item_idx, item_id)
            item_idx = item_idx + 1


def get_item_html_by_item_id(item_idx: int, item_id: int):
    file_path = './item_html/{}.html'.format(item_id)
    item_url = 'https://myfigurecollection.net/item/{}'.format(item_id)
    if os.path.exists(file_path):
        print('>>>file is exist item_id: {}'.format(item_id))
    else:
        item_html_text = tool.get_html_text(item_url)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(item_html_text)
        print('=========idx: {} item_id: {}========='.format(item_idx, item_id))


# get_goods_html_text_by_keyword('Higurashi no Naku Koro ni', 6)
# get_item_html_by_entry(69)
# get_all_goods_item()
# get_item_html_by_item_id(1, 299087)

get_item_detail(24539)
