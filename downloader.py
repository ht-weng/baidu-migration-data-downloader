# Note that Baidu only provides data for 2020

# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
from datetime import date as dtdate
import json
import time
import csv
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Read dictionaries
province_name = {}
province_code = {}
city_name = {}
city_code = {}

f_pn = open('dicts/province_name.csv', 'r')
reader_pn = csv.reader(f_pn)
for row in reader_pn:
    province_name[row[0]] = row[1]

f_pc = open('dicts/province_code.csv', 'r')
reader_pc = csv.reader(f_pc)
for row in reader_pc:
    province_code[row[0]] = row[1]
    
f_cn = open('dicts/city_name.csv', 'r')
reader_cn = csv.reader(f_cn)
for row in reader_cn:
    city_name[row[0]] = row[1]
    
f_cc = open('dicts/city_code.csv', 'r')
reader_cc = csv.reader(f_cc)
for row in reader_cc:
    city_code[row[0]] = row[1]

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):

    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Core function for downloading data
# Option: 0: city rank, 1: province rank, 2: history curve, 3: internal flow history
def downloader(option, region, rtype='city', direction='in', startdate=0, enddate=0):
    if rtype == 'city' and region in city_code.keys():
        rid = city_code[region]
        region_name = city_name[region]
    elif rtype == 'province' and region in province_code.keys():
        rid = province_code[region]
        region_name = province_name[region]
    else:
        print('ERROR: Invalid Region Name!')
        return
    
    if startdate == 0:
        startdate = 20200101
    if enddate == 0:
        enddate = dtdate.today().strftime('%Y%m%d')
    
    if option in (0, 1, 3):
        start = datetime.strptime(str(startdate), '%Y%m%d')
        end = datetime.strptime(str(enddate), '%Y%m%d')
        date_list = [int((start + timedelta(days=x)).strftime('%Y%m%d')) for x in range(0, (end-start).days-1)]
    
    if option == 2:
        # history curve
        url = f'http://huiyan.baidu.com/migration/historycurve.jsonp?dt={rtype}&id={rid}&type=move_{direction}'
        print('history curve: ', region_name, '-', direction)
        
        # response = requests.get(url, timeout = 60)
        response = requests_retry_session().get(url, timeout = 60)
        # time.sleep(1)
        r = response.text[3:-1]
        data_dict = json.loads(r)
        if data_dict['errmsg'] == 'SUCCESS':
            data_subdict = data_dict['data']['list']
            # time.sleep(1)
            if not data_subdict is None:
                history_date = list(data_subdict.keys())
                history_date = [int(x) for x in history_date]
                values = list(data_subdict.values())
                
                df = pd.DataFrame({'Date': history_date, 'Value': values})
                
                if direction == 'in':
                    df.to_csv('data/history/'+str(rid)+'-'+'Inbound.csv', index=False)
                elif direction == 'out':
                    df.to_csv('data/history/'+str(rid)+'-'+'Outbound.csv', index=False)
        
    elif option == 3:
        # internal flow history
        # Internal flow history query will return all data at once. So only send with the end date.
        url = f'http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt={rtype}&id={rid}&&date={date_list[-1]}'
        print('internal flow history: ', region_name)
        
        # response = requests.get(url, timeout = 60)
        response = requests_retry_session().get(url, timeout = 60)
        # time.sleep(1)
        r = response.text[3:-1]
        data_dict = json.loads(r)
        if data_dict['errmsg'] == 'SUCCESS':
            data_subdict = data_dict['data']['list']
            # time.sleep(1)
            if not data_subdict is None:
                history_date = list(data_subdict.keys())
                history_date = [int(x) for x in history_date]
                values = list(data_subdict.values())
                
                df = pd.DataFrame({'Date': history_date, 'Value': values})
                df.to_csv('data/internal/'+str(rid)+'.csv', index=False)
        
    else:
        # list to store dataframes of downloaded data
        df_list = []
        for date in date_list:
            if option == 0:
                # city rank
                url = f'http://huiyan.baidu.com/migration/cityrank.jsonp?dt={rtype}&id={rid}&type=move_{direction}&date={date}'
                print('city rank: ', region_name, '-', direction, '-', date)
            elif option == 1:
                # province rank
                url = f'http://huiyan.baidu.com/migration/provincerank.jsonp?dt={rtype}&id={rid}&type=move_{direction}&date={date}'
                print('province rank: ', region_name, '-', direction, '-', date)
            else:
                print('ERROR: Invalid Option!')
                return

            # response = requests.get(url, timeout = 60)
            response = requests_retry_session().get(url, timeout = 60)
            # time.sleep(1)
            r = response.text[3:-1]
            data_dict = json.loads(r)
            if data_dict['errmsg'] == 'SUCCESS':
                data_list = data_dict['data']['list']
                # time.sleep(1)
                region_codes = []
                # regions = []
                values = []
                
                for i in range (len(data_list)):
                    if option == 0:
                        region_chn = data_list[i]['city_name']
                        code = city_code[region_chn]
                        # region_eng = city_name[region_chn]
                    elif option == 1:
                        region_chn = data_list[i]['province_name']
                        code = province_code[region_chn]
                        # region_eng = province_name[region_chn]
                    value = data_list[i]['value']
                    
                    region_codes.append(code)
                    # regions.append(region_eng)
                    values.append(value)
                
                df = pd.DataFrame({'Code': region_codes, date: values})
                df_list.append(df)
            else:
                print('ERROR: ', data_dict['errmsg'])
    
        if len(df_list) > 1:
            df_all = pd.merge(df_list[0], df_list[1], how='outer', on='Code')
            df_all.fillna(0.0, inplace=True)
            for i in range(2, len(df_list)):
                df_all = pd.merge(df_all, df_list[i], how='outer', on='Code')
                df_all.fillna(0.0, inplace=True)
        else:
            df_all = df_list[0]

        if option == 0:
            if direction == 'in':
                df_all.to_csv('data/city/'+str(rid)+'-'+'Inbound.csv', index=False)
            elif direction == 'out':
                df_all.to_csv('data/city/'+str(rid)+'-'+'Outbound.csv', index=False)
        elif option == 1:
            if direction == 'in':
                df_all.to_csv('data/province/'+str(rid)+'-'+'Inbound.csv', index=False)
            elif direction == 'out':
                df_all.to_csv('data/province/'+str(rid)+'-'+'Outbound.csv', index=False)


def main():
    # downloader(1, '北京市', 'province', 'in', 20200101, 20200105)
    # downloader(0, '北京市', 'city', 'in', 20200101, 20200105)
    # downloader(0, '北京市', 'city', 'out', 20200301, 20200324)
    # downloader(3, '香港特别行政区', 'city')
    # downloader(3, '澳门特别行政区', 'city')
    
    # # Download data for provinces' history curves
    # for province in province_code.keys():
    #     downloader(2, province, 'province', 'in')
    #     downloader(2, province, 'province', 'out')
    #     print(province, ' Done')
    
    # # Download data for cities' history curves
    # for city in city_code.keys():
    #     if not city == '台湾省':
    #         downloader(2, city, 'city', 'in')
    #         downloader(2, city, 'city', 'out')
    #         print(city, ' Done')

    # # Download data for cities' internal flows
    # for city in city_code.keys():
    #     if not city == '台湾省':
    #         downloader(3, city, 'city')
    #         print(city, ' Done')
    
    # # Download data for all provinces
    # for province in province_code.keys():
    #     downloader(1, province, 'province', 'in')
    #     downloader(1, province, 'province', 'out')
    #     print(province, ' Done')
    
    # Download data for all cities
    for city in city_code.keys():
        downloader(0, city, 'city', 'in')
        downloader(0, city, 'city', 'out')
        print(city, ' Done')

    print('Download All Complete!')
    
if __name__ == "__main__":
    main()

    
