import csv
import os

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


def get_hsk_words(letter_link):
    """
    필수 중국 문자 dic_link.csv 로부터 받은 주소를 가지고
    Chrome crawling을 실행, hsk 단어에 대한 'row'데이터를 리턴,
    Attribute Error가 발생할 때, 성공할 때까지 재시도.
    NoneType가 될 때도 성공할 때까지 재시도
    :param letter_link: dic_link.csv 로부터 받은 주소
    :return: row 데이터
    """
    # driver = webdriver.Chrome("D:/dev/chromedriver.exe")  # 집에서 chromedriver 경로
    driver = webdriver.Chrome("C:/Users/user/Downloads/chromedriver.exe")  # 학원에서 chromedriver 경로
    url = f'https://zh.dict.naver.com/{letter_link}'
    driver.get(url)
    driver.minimize_window()
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    driver.close()

    for x in range(5):
        try:
            chr_container = soup.find('div', id='container').find('div', class_='section_hsk')
            print(type(chr_container))
        except AttributeError:
            pass
            print('error?')

    if type(chr_container) == type(None):
        return 0
    else:
        chr_rows = chr_container.find_all('div', class_='row')
        # print(f'chr_rows:{chr_rows}')
        return chr_rows


def get_links_list(letter, crawl_data):
    """
    크롤링해 받아온 데이터가 find_all 이므로 for 구문을 사용해야 함
    :param letter: 딕셔너리의 'key'가 될 글자
    :param crawl_data: 크롤링 데이터
    :return: 문자 한개에 대한 hsk 단어의 딕셔너리를 리턴.
            ex)  {'星': ['hsk 1급 단어',"#/entry/zhko/c202b65ab2b04646bd90bd7bad00aea2",
                        'hsk 5급 단어',"#/entry/zhko/57b6d821b45c4b60b89742b2f799e439",
                        'hsk 6급 단어', "#/entry/zhko/22f9a79bacf24628af6ccfd37cac70e1",
                                        "#/entry/zhko/eaade97be8ac4114a8b6ef3d63975f39"] }
    """
    individual_data = {letter: []}  # dict 선언
    for titles in crawl_data:
        hsk_level = titles.find('div', class_='category')
        hsk_words_url = titles.find('a', class_='link')
        # print('hsk_level', hsk_level)
        # print('hsk_words_url', hsk_words_url)
        # 'x급'이라는 말이 있을 경우, 맨 앞에 붙여준다.
        if type(hsk_level) == type(None):
            pass
        else:
            individual_data[letter].append(hsk_level.text)  # hsk_level의 text부분만
        individual_data[letter].append(hsk_words_url['href'])  # hsk_words_url의 'href'부분만

    return individual_data


def save_dict_csv(data, name):
    data_frame = pd.DataFrame(data.items())  # import pandas as pd
    data_frame.to_csv(name, encoding='utf-8')


def my_csv_reader(fn: str, header=True, encoding='utf-8') -> list:
    """
    csv 파일의 데이터를 2차원 행렬 형태로 리턴

    :param fn: 읽을 csv 파일 이름(예: data\\exam.csv)
    :param header: csv 파일의 헤더 존재 여부
    :param encoding: 파일 인코딩
    :return: csv 파일에서 헤더는 제외한 데이터들로 이루어진 2차원 리스트
    """
    data = []  # 빈 리스트를 만든다.
    with open(fn, mode='r', encoding=encoding) as f:
        if header:  # csv 파일에 컬럼 이름들이 헤더에 있으면
            f.readline()  # 한 줄을 읽고 지나간다.
        for line in f:  # 파일 끝까지 한 줄씩 읽어서
            # 읽은 줄의 앞/뒤 공백문자를 제거하고(strip),
            # 문자열을 쉼표(,)로 분리(split)해서 문자열 리스트를 만들고,
            # 리스트 data에 추가한다.
            data.append(line.strip().split(','))

    return data


# 실행부
if __name__ == '__main__':
    # input_file = os.path.join('dic_link.csv')
    # input_file = os.path.join('dic_link2.csv')  # Pycharm 에러로 다시 시작
    # input_file = os.path.join('dic_link3.csv')  # 분할실행
    input_file = os.path.join('../csv/dic_link4.csv')  # 세번째 실행중 에러
    chn_words_link = my_csv_reader(input_file)  # input_file로부터 주소를 받아온다

    # chn_hsk_link = []
    chn_hsk_link = {}

    for row in chn_words_link:  # 주소 list를 순서대로 실행
        get_list = get_hsk_words(row[2])
        print(row[1])
        if get_list == 0:
            pass
        else:
            links_list = get_links_list(row[1], get_list)
            print(links_list)
            for key, value in links_list.items():
                chn_hsk_link[key] = value  # return 받은 딕셔너리를 리스트에 추가
            # print(chn_hsk_link)
            # 저장
            # save_dict_csv(chn_hsk_link, 'hsk_words_link1.csv') Pycharm 에러로 연결해서 재시작
            # save_dict_csv(chn_hsk_link, 'hsk_words_link3.csv') 분할실행
            # save_dict_csv(chn_hsk_link, '../csv/hsk_words_link4.csv')

"""
error?
Traceback (most recent call last):
  File "C:/Users/LVSTA/Desktop/GitHub/lab-python/(1)web_crawl_self/hsk_words.py", line 87, in <module>
    get_list = get_hsk_words(row[2])
  File "C:/Users/LVSTA/Desktop/GitHub/lab-python/(1)web_crawl_self/hsk_words.py", line 37, in get_hsk_words
    if type(chr_container) == type(None):
UnboundLocalError: local variable 'chr_container' referenced before assignment

+ 디버깅에 대해 알아보기
"""
