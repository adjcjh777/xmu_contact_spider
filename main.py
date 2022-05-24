import queue
import threading
import spider
from bloom import *
import pandas as pd
cnt = 0  # 统计网址个数
url_filter = init_static_bloom(500000)  # 过滤已经出现过的url
start_url = 'https://www.xmu.edu.cn/'  # 从厦大主页开始搜索
visit_queue = [start_url]  # 队列储存所有访问的网址
url_list = [start_url]  # 初始化访问过的url
tel_dict = {}  # 初始化联系方式字典


# 初始化所有储存信息的队列
def initialize_msg_queue():
    url_queue = queue.Queue()
    html_queue = queue.Queue()
    url_queue.put(start_url)  # 开始的网页入队
    return url_queue, html_queue


def crawling(url_queue: queue.Queue, html_queue: queue.Queue):
    while True:
        url = url_queue.get()
        # 观察线程状态
        global cnt
        print(threading.current_thread().name, f"Crawling NO.{cnt} website :{url}")
        cnt += 1
        page = spider.get_response(url)
        html_queue.put((page, url))
        if url_queue.empty():
            break


'''解析html'''


def parse_htmL(url_queue: queue.Queue, html_queue: queue.Queue):
    try:
        while True:
            page, url = html_queue.get()
            if not page == None:
                temp_url_list = spider.get_url(page, url)
                org, temp_tel_list = spider.get_info(page)
            else:
                temp_url_list = []
                org, temp_tel_list = None, []
            '''
            保存当前的联系方式到list
            '''
            if len(temp_tel_list) > 0:
                save_current(org, temp_tel_list)
                print(org, temp_tel_list)

            for url in temp_url_list:
                if url not in url_filter:
                    url_filter.add(url)
                    url_queue.put(url)
                    url_list.append(url)


    except IndexError as e:
        print(e)
    finally:
        return

    # 将联系人和联系方式配对组织起来


def save_current(org, temp_tel_list):
    if org in tel_dict.keys():
        tel_dict[org] = tel_dict[org] | set(temp_tel_list)
    else:
        tel_dict[org] = set(temp_tel_list)


'''
多线程创建启动 参考http://m.biancheng.net/python_spider/multithreading.html
'''


def threads(url_queue, html_queue, thread_num=100):
    thread_list = []  # 新建线程列表
    # 开始爬取线程
    for i in range(thread_num):
        t = threading.Thread(target=crawling(url_queue,html_queue), args=[url_queue, html_queue], name=f'Crawling No.{i + 1}')
        thread_list.append(t)
        t.start()
    # 开始解析线程
    for i in range(thread_num):
        t = threading.Thread(target=parse_htmL(url_queue,html_queue), args=[url_queue, html_queue], name=f'Parse No.{i + 1}')
        thread_list.append(t)
        t.start()
    return thread_list


def save_all(path='result.csv'):
    """
    :param path: result.csv
    :return: None
    """
    print("Succeed. Save all the data.")
    tel_dict.update((key, str(val)) for key, val in tel_dict.items())
    df = pd.DataFrame(list(tel_dict.items()))  # pandas将字典中的内容转换为csv存储
    df.to_csv(path_or_buf=path, encoding='utf8')
    print(df)


def main():
    url_queue, html_queue = initialize_msg_queue()  # 初始化赋值队列
    thread_list = threads(url_queue=url_queue, html_queue=html_queue)
    # 阻塞等待回收线程
    for i in thread_list:
        i.join()
    save_all()


if __name__ == '__main__':
    main()
