import os
import re
from typing import List, Type

from bs4 import BeautifulSoup

import request_tool as tool
from source_data import ItemDetail, Entry, ItemImage


def open_text(item_id: int):
    # 指定目录
    dir_path = './higurashi_goods_item_html'
    # # 指定文件名和扩展名
    file_name = '{}.html'.format(item_id)

    # 遍历目录下所有文件名
    for filename in os.listdir(dir_path):
        # 判断是否是指定文件名和扩展名的文件
        if filename.startswith(file_name):
            # 打开文件并读取内容
            with open(os.path.join(dir_path, filename), 'r', encoding='utf-8') as f:
                file_content = f.read()
    return file_content


def get_item_detail(item_id: int):
    # url = 'https://myfigurecollection.net/item/{}'.format(item_id)
    # html_text = tool.get_html_text(url)
    html_text = open_text(item_id)
    soup = BeautifulSoup(html_text, 'html.parser')
    data_fields = soup.find_all('div', class_='data-field')
    item_name = soup.find('div', class_='content-headline').find('h1', class_='title').text
    item_thumb = soup.find('div', class_='content-icon').find('img', class_='thumbnail')['src']
    main_image = \
        soup.find('div', class_='item-picture').find('div', class_='tbx-pswp').find('a', class_='main').find('img')[
            'src']
    item = ItemDetail()
    item.name = item_name
    item.images.append(ItemImage(0, handle_my_collection_image_url(item_thumb)))
    item.images.append(ItemImage(100, handle_my_collection_image_url(main_image)))
    item.images = item.images + get_item_images(item_id)
    for idx, data_field in enumerate(data_fields, start=1):
        data_label_attr = data_field.find('div', class_='data-label')
        if data_label_attr is None:
            continue
        data_label = data_label_attr.string
        data_value = data_field.find('div', class_='data-value')
        data_value_value = data_value.find_all('a')

        if data_label == 'Category':
            item.category = data_value.find('a').text
        if data_label == 'Classifications':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                item.classifications.append(Entry(int(entry_id), entry_name, entry_name_en, ''))
        if data_label == 'Origin':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                item.origins.append(Entry(int(entry_id), entry_name, entry_name_en, ''))
        if data_label == 'Characters':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                item.characters.append(Entry(int(entry_id), entry_name, entry_name_en, ''))
        if data_label == 'Company':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                entry_role = re.search(r'As (\w+)', m.find('small').text).group(1)
                item.companies.append(Entry(int(entry_id), entry_name, entry_name_en, entry_role))
        if data_label == 'Material':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                item.materials.append(Entry(int(entry_id), entry_name, entry_name_en, ''))
        if data_label == 'Artist':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                entry_role = re.search(r'As (\w+)', m.find('small').text).group(1)
                item.artists.append(Entry(int(entry_id), entry_name, entry_name_en, entry_role))
        if data_label == 'Event':
            for m in data_value_value:
                entry_id = re.search(r'/entry/(\d+)', m['href']).group(1)
                entry_name = m.find('span')['switch']
                entry_name_en = m.find('span').text
                entry_role = re.search(r'As (\w+)', m.find('small').text).group(1)
                item.events.append(Entry(int(entry_id), entry_name, entry_name_en, entry_role))
        if data_label == 'Releases':
            item.releaseDetail = data_value.text
            # releaseDate = data_value.find('a', class_='time')
            # small_elements = [small for small in data_value.find_all('small') if 'As ' in small.get_text()]
            # releaseType = small_elements[0].find('em').text
            # _dict['releaseDate'] = releaseDate.text
            # _dict['releaseType'] = releaseType
            #
            # tmp_attr = data_value.find('a', class_='tbx-window')
            # if is_ean13(tmp_attr.text):
            #     _dict['ean13'] = data_value.find('a', class_='tbx-window').text
            # if contains_digits_spaces_commas(data_value.get_text()):
            #     _dict['price'] = data_value.get_text()
        if data_label == 'Dimensions':
            div_element = soup.find('div', class_='data-value')
            item.dimensions = div_element.get_text(strip=True)

    return item


def get_item_images(item_id: int):
    images: list[ItemImage] = []
    item_images_url = 'https://myfigurecollection.net/?_tb=picture&itemId={}&page={}'
    first_item_images_url = item_images_url.format(item_id, 1)
    first_html_text = tool.get_html_text(first_item_images_url)
    soup = BeautifulSoup(first_html_text, 'html.parser')
    title = soup.title.string
    total_page = get_total_page_size_by_html_title(title)

    for i in range(1, total_page + 1):
        if i == 1:
            html_text = first_html_text
        else:
            html_text = tool.get_html_text(item_images_url.format(item_id, i))
        soup = BeautifulSoup(html_text, 'html.parser')
        image_span = soup.find_all('span', class_='picture-icon tbx-tooltip')
        for idx, span in enumerate(image_span, start=1):
            tmp_span = span.find('a').find('span', class_='viewport')
            image_url = get_item_image_url(tmp_span['style'])
            image_type = get_item_image_type(span.find('a')['class'][0])
            images.append(ItemImage(image_type, handle_my_collection_image_url(image_url)))
    return images


def is_ean13(code):
    pattern = re.compile(r'^\d{13}$')
    return bool(pattern.match(code))


def contains_digits_spaces_commas(text):
    pattern = re.compile(r'[0-9\s,]')
    return bool(pattern.search(text))


def handle_my_collection_image_url(url: str):
    return url.replace('https://static.myfigurecollection.net', '')


def get_item_image_url(input_str: str):
    return re.compile(r"url\((.*?)\)").findall(input_str)[0].replace('/thumbnails', '')


def get_item_image_type(input_str: str):
    return re.search(r'picture-category-(\d+)', input_str).group(1)


def get_total_page_size_by_html_title(title: str):
    match = re.search(r'Page \d+ of (\d+)', title)
    return int(match.group(1))
