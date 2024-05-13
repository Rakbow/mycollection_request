import csv
import random
import re
import time

from bs4 import BeautifulSoup

import request_tool as tool


def get_all_goods():
    result_dict = {}
    base_url = 'https://myfigurecollection.net/?tab=search&rootId=1&excludeContentLevel=0&tags%5B%5D' \
               '=higurashi_no_naku_koro_ni_series&domainId=-1&noReleaseDate=0&releaseTypeId=0&ratingId=0&isCastoff=0' \
               '&hasBootleg=0&tagId=0&clubId=0&excludeClubId=0&listId=0&isDraft=0&year=2024&month=5&acc=0&separator=0' \
               '&sort=insert&output=2&current=categoryId&order=desc&_tb=item&page={}'

    page_1_html_text = tool.get_html_text(base_url.format(1))
    page_1_soup = BeautifulSoup(page_1_html_text, 'html.parser')
    title = page_1_soup.title.string
    match = re.search(r'Page \d+ of (\d+)', title)
    total_page_size = match.group(1)

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
            item_img_url = span.find('img')['src']  # 提取img元素的src值
            item_name = span.find('img')['alt']  # 提取img元素的alt值
            cur_idx = (i - 1) * 80 + idx
            result_dict[cur_idx] = {'id': item_id, 'img': item_img_url, 'name': item_name}
            print('=========cur_page: {} cur_idx: {} item_id: {}========='.format(i, cur_idx, item_id))
    with open('./goods_dict/goods_higurashi.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['id', 'img', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for idx in result_dict:
            writer.writerow(result_dict[idx])


def get_goods_html_text(entry_id: int):
    result_dict = {}
    base_url = 'https://myfigurecollection.net/?orEntries%5B%5D={}page={}&_tb=item&rootId=1'

    page_1_html_text = tool.get_html_text(base_url.format(entry_id, 1))
    page_1_soup = BeautifulSoup(page_1_html_text, 'html.parser')
    title = page_1_soup.title.string
    match = re.search(r'Page \d+ of (\d+)', title)
    total_page_size = match.group(1)

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
            item_img_url = span.find('img')['src']  # 提取img元素的src值
            item_name = span.find('img')['alt']  # 提取img元素的alt值
            cur_idx = (i - 1) * 80 + idx
            result_dict[cur_idx] = {'id': item_id, 'img': item_img_url, 'name': item_name}
            print('=========cur_page: {} cur_idx: {} item_id: {}========='.format(i, cur_idx, item_id))
    write_dict_to_csv(entry_id, result_dict)


def write_dict_to_csv(entry: int, _dict: dict):
    with open('./goods_dict/goods_entry_{}.csv'.format(entry), 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['id', 'img', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for idx in _dict:
            writer.writerow(_dict[idx])


# get_goods_html_text(299775)
get_all_goods()
