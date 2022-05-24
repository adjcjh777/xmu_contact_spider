import chardet
from bs4 import BeautifulSoup as bs
from myre import *
import requests as rq


def get_response(url):
    try:
        '''以get方式获取反馈，等待1秒'''
        response = rq.request(url=url, method='get', timeout=1)
        '''Raises HTTPError, if one occurred'''
        response.raise_for_status()
        '''根据给定字节返回编码'''
        response.encoding = response.apparent_encoding
        if not response ==  None:
            return bs(response.content, 'lxml')
        return response

    except:
        print(f'{url} have no content,go next')
        return None


'''
获取url前缀
'''


def get_ori_url(url):
    re_pattern = r'(?<=://)[a-zA-Z\.0-9]+(?=\/)'
    ori_url = re.findall(re_pattern, url, re.U)
    if ori_url:
        return ori_url[0]
    return None


def get_info(page):
    """
    通过字符串找到其中的联系人和联系方式
    :param page: requests.response 的对象
    :return: tuple(org,tel_list)
    """

    content = str(page)
    '''
    从content中找到tel和org
    '''
    org = find_org(content)
    tel_list = find_tel(content)
    tel_list = [tel.replace(u'\xa0', u'') for tel in tel_list]
    return org, tel_list


def get_url(soup, url):
    try:
        oriurl = get_ori_url(url)
        if oriurl == None:
            return []
        oriurl = 'https://' + oriurl + '/'
        '''
        返回所有标签名为'a'的tag
        '''
        tags = soup.select("a")
        ans = set()
        for a in tags:
            if not a.get('href') == None:
                context = str(a['href'])
                if context.endswith('.htm') and not context.startswith('http'):
                    ans.add(oriurl + a['href'])
                elif (context.__contains__('xmu.edu.cn') and (
                        context.endswith('html') or context.endswith('htm'))) or context.endswith('xmu.edu.cn'):
                    ans.add(a['href'])
        return ans
    except KeyError as ke:
        print(f'{url} do not has key {ke}')
        return None
