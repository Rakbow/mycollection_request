import os
from datetime import datetime, timedelta
import random
import time

import requests  # 导库
from bs4 import BeautifulSoup


def get_random_date_str():
    # 指定时间范围
    year = random.randint(2021, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    start_time = datetime(year, month, day)
    end_time = start_time + timedelta(days=random.randint(1, 365))

    # 生成随机时间戳
    time_diff = end_time - start_time
    random_time = start_time + timedelta(seconds=random.randint(0, int(time_diff.total_seconds())))

    # 将时间戳转换为指定格式的时间字符串
    time_string = random_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return time_string


# 获取html页面文本
def get_html_text(url):
    param = {
        'Connection': 'close',
        'Content-Encoding': 'gzip',
        'Content-Type': 'text/html',
        'Server': 'nginx',
        'Transfer-Encoding': 'chunked',
        'Vary': 'Accept-Encoding'
    }
    header = {'Content-Type': 'text/html; charset=utf-8'}
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]
    header['User-Agent'] = random.choice(user_agent_list)
    param['Date'] = get_random_date_str()
    proxies = {
        'http': 'localhost:7890',
        'https': 'localhost:7890'
    }
    r = requests.get(url, params=param, headers=header, timeout=30)
    r.raise_for_status()  # 如果状态不是200，引发HTTPError异常
    r.encoding = r.apparent_encoding  # 因为apparent更准确
    return r.text
