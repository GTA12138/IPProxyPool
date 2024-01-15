# coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
import  time
import threading
import  flask
from flask_server import start_proxy_server


def get_useful_proxies():
    use_proxy_list = []

    # 爬取代理信息
    for i in range(1, 8):
        url = "http://www.ip3366.net/free/?stype=1&page={}".format(i)
        response = requests.get(url)
        html_content = response.content.decode('gbk')
        soup = BeautifulSoup(html_content, 'html.parser')

        ip_pattern = re.compile(r'<td>([\d.]+)</td>')
        ip_value = []
        ip_list = ip_pattern.findall(str(soup))
        for ip in ip_list:
            if 5 < len(ip) <= 17:
                ip_value.append(ip)

        port_pattern = re.compile(r'<td>(\d+)</td>')
        port_value = []
        port_list = port_pattern.findall(str(soup))
        if len(port_list) >= 4:
            port_value.extend(port_list)

        for ip, port in zip(ip_value, port_value):
            proxy_ip = 'http://{}:{}'.format(ip, port)
            use_proxy_list.append(proxy_ip)

    print("共爬取到", len(use_proxy_list), "个代理")
    return use_proxy_list


def check_proxy(proxy):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    proxies = {'http': proxy}
    try:
        test = requests.get('http://www.baidu.com', headers=headers, proxies=proxies, timeout=10)
        if test.status_code == 200:
            print(f'{proxy} is ok')
            return proxy
    except:
        print(f'{proxy} is not working')


def get_valid_proxies(proxy_list):
    can_use_list = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_proxy, proxy) for proxy in proxy_list]
        for future in futures:
            result = future.result()
            if result:
                can_use_list.append(result)

    print("共有", len(can_use_list), "个代理可用")
    return can_use_list

def start_flask_server(proxies):
    time.sleep(2)
    threading.Thread(target=start_proxy_server, args=(proxies,)).start()

if __name__ == '__main__':
    use_proxy_list = get_useful_proxies()
    can_use_list = get_valid_proxies(use_proxy_list)

    print("可以用的代理数量为:", len(can_use_list))
    print("可用代理列表：", can_use_list)

    start_flask_server(can_use_list)








