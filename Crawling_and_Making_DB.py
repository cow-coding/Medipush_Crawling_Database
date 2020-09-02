# library import
import pymongo
import requests
import re
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager

"""Medicine product code save"""
f = open('med_code.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

lists = []

for line in rdr:
    lists.append(line)

f.close()
index = lists
""""""


# connect Mongodb
conn = pymongo.MongoClient('mongodb://13.124.201.28', username='root', password='mp123', authMechanism='SCRAM-SHA-1')
medipush = conn.medipush
medicine = medipush.medicine

# Variable initialize
manager = Manager()
med_data_list = manager.list()
cnt = manager.list()

# HTTPError Handling list
error_index = manager.list()

# Data crwaling function
def crawling(i):
    cnt.append(i)
    print('count : ', len(cnt))
    print('Now data number : ', index[i][0])

    # Web page data Crawling
    url = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=" + index[i][0]

    res = requests.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    med_basic = soup.select_one('div.r_sec tr')

    # HTTPError making index
    if med_basic == None:
        error_index.append(i)
        return

    # product name save
    med_dict = dict()
    med_name = med_basic.select_one('td').text
    input_med = med_name.replace('\n', ' ')
    med_dict['prodName'] = input_med.strip()

    # 병용금기 전용 유효성분 저장 리스트
    ingr_list = list()

    # product ingredient save
    if soup.select_one('#scroll_02 > h3'):
        med_ingredient = soup.select_one('#scroll_02 > h3').text
        med_ingredient = med_ingredient.replace('유효성분 : ', '')
        ingredient = med_ingredient.split(',')
        med_dict['ingredient'] = list(set(ingredient))
        ingr_list = list(set(ingredient))

    # product caution save
    ## dur info exist
    if soup.select_one('#scroll_06 > table'):

        dur_table_crawling = soup.select('#scroll_06 > table > tbody > tr > td')
        dur_table_content = list()

        for item in dur_table_crawling:
            dur_table_content.append(item.text.split('\n'))

        data_insert = False
        name = list()
        dur_list = list()

        for item in dur_table_content:
            mix = False
            dur_data_input = False
            input = dict()

            if "DUR성분(성분1/성분2..[병용성분])" in item:
                dur_ingredient = item[item.index('DUR성분(성분1/성분2..[병용성분])') + 1]

            if "DUR유형" in item:
                dur_type = item[item.index('DUR유형') + 1]

                if item[item.index('DUR유형') + 1] == '병용금기':
                    dur_data_input = True
                    data_insert = True

                    # dur_mix를 저장하는 딕셔너리 생성
                    ## 문자열 파싱 파트
                    dur_main = re.sub('\[\w*\]', '', dur_ingredient)
                    dur_mix = re.search('\[\w*\]', dur_ingredient)
                    dur_mix = dur_mix.group().replace('[', '').replace(']', '')

                    for t in ingr_list:
                        if dur_mix in t:
                            # 부분일치 문자열이 dur_mix에 있는 경우 dur_main을 넣어줘야함
                            mix = True
                            break
                        elif dur_main in t:
                            # 부분일치 문자열이 dur_main에 있는 경우 dur_mix에 넣어줘야함
                            mix = False
                            break
                        else:
                            mix = False

                    # dur_mix에 부분일치 문자열이 있는 경우
                    if mix:
                        if dur_main not in name:
                            name.append(dur_main)
                            input['ingr'] = dur_main
                            input['dur'] = '병용금기'
                        else:
                            continue
                    # dur_main에 부분일치 문자열이 있는 경우
                    else:
                        if dur_mix not in name:
                            name.append(dur_mix)
                            input['ingr'] = dur_mix
                            input['dur'] = '병용금기'
                        else:
                            continue

                elif item[item.index('DUR유형') + 1] != '분할주의':
                    data_insert = True
                    dur_data_input = True
                    input['ingr'] = dur_ingredient
                    input['dur'] = dur_type

                if dur_data_input:
                    dur_list.append(input)

        if data_insert:
            med_dict['cautionInfo'] = dur_list

    medicine.insert_one(med_dict)


if __name__ == '__main__':
    med_data_list = manager.list()
    pool = Pool(processes=10)
    pool.map(crawling, range(0, 44469, 1))
    pool.close()
    conn.close()
    print('----------------------------------------\n')
    print('                                        \n')
    print('All data search end and Make a database!\n')
    print('error product code list : ', error_index)
    print('                                        \n')
    print('----------------------------------------\n')
