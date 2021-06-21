from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote_plus, unquote
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import json
import xmltodict
import requests
import pandas as pd
#import urllib2

#Open API Url 생성
url = 'https://api.odcloud.kr/api/15077756/v1/vaccine-stat?serviceKey='
key = 'iJDdekz8rEiL8Jir2o9i%2BESsgdoUN5j3dfotu065tW8MlYeSuBO9eUrzHED2C1%2F%2B8bbEt%2FdzabsFy3Jfx0kPRQ%3D%3D'
# params = '&page=1&perPage=1824'
queryParams = '&' + urlencode({quote_plus('page'): '1', quote_plus('perPage'): '1824', quote_plus('returnType'): 'JSON'})
#Json 으로 저장
get_data = requests.get(url + key + unquote(queryParams))
result_data = get_data.json()
#print(result_data)
file = open('vaccin.json', "w+")
file.write(json.dumps(result_data))



# xml_queryParams = '&' + urlencode({quote_plus('page'): '1', quote_plus('perPage'): '1824', quote_plus('returnType'): 'XML'})
# get_xml_data = requests.get(url + key + unquote(xml_queryParams))
# xml_result_data = get_xml_data.text

##CSV FILE
#print(result_data['data'][0].keys())

with open('vaccin.csv', 'w', encoding='utf-8')as f:
    wr = csv.DictWriter(f, fieldnames = result_data['data'][0].keys())
    wr.writeheader()
    wr.writerows(result_data['data'])



#Craw       xml Save
url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
key = 'iJDdekz8rEiL8Jir2o9i+ESsgdoUN5j3dfotu065tW8MlYeSuBO9eUrzHED2C1/+8bbEt/dzabsFy3Jfx0kPRQ=='
queryParams = '?' + urlencode({ quote_plus('ServiceKey') : key, quote_plus('pageNo') : '1', quote_plus('numOfRows') : '1000', quote_plus('startCreateDt') : '20210101', quote_plus('endCreateDt') : '20210619' })

request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
f = open('covid.xml', 'wb')
f.write(response_body)


#XML => JSON
#CONVERTING
tojson = xmltodict.parse(response_body)
#JSON DUMPING
json_obj = json.dumps(tojson)
#SAVING
covid_file = open('covid.json', 'w+')
covid_file.write(json_obj)
f.close()


# #XML => CSV (pandas)
#tree = ET.parse('covid.xml')
df = pd.DataFrame(columns=['accDefRate', 'accExamCnt', 'accExamCompCnt', 'careCnt', 'clearCnt', 'createDt', 'deathCnt', 'decideCnt', 'examCnt', 'resutlNegCnt', 'seq', 'stateDt', 'stateTime', 'updateDt'])
xml_url = url + queryParams
data = urlopen(xml_url).read()
soup = BeautifulSoup(data, "html.parser")
k = 0
for i in soup.findAll('item'):
    df.loc[k] = [
        i.accDefRate.text,
        i.accExamCnt.text,
        i.accExamCompCnt.text,
        i.careCnt.text,
        i.clearCnt.text,
        i.createDt.text,
        i.deathCnt.text,
        i.decideCnt.text,
        i.examCnt.text,
        i.resutlNegCnt.text,
        i.seq.text,
        i.stateDt.text,
        i.stateTime.text,
        i.updateDt.text
    ]
    k +=1
df.to_csv('covid.csv', encoding='utf-8')

# cols = ['accDefRate', 'accExamCnt', 'accExamCompCnt', 'careCnt', 'clearCnt', 'createDt', 'deathCnt', 'decideCnt', 'examCnt', 'resutlNegCnt', 'seq', 'stateDt', 'stateTime', 'updateDt']
# rows = []
# response_body = urlopen(request).read()
# data = str(response_body, 'utf-8')
# tree = ET.parse('covid.xml')
# root = tree.getroot()
# for elem in root:
#     accDefRate = elem.find("accDefRate").text
#     accExamCnt = elem.find("accExamCnt").text
#     accExamCompCnt = elem.find("accExamCompCnt").text
#     careCnt = elem.find("careCnt").text
#     clearCnt = elem.find("clearCnt").text
#     createDt = elem.find("createDt").text
#     deathCnt = elem.find("deathCnt").text
#     decideCnt = elem.find("decideCnt").text
#     examCnt = elem.find("examCnt").text
#     resutlNegCnt = elem.find("resutlNegCnt").text
#     seq = elem.find("seq").text
#     stateDt = elem.find("stateDt").text
#     stateTime = elem.find("stateTime").text
#     updateDt = elem.find("updateDt").text

#     rows.append({
#         'accDefRate': accDefRate,
#         'accExamCnt': accExamCnt,
#         'accExamCompCnt': accExamCompCnt,
#         'careCnt': careCnt,
#         'clearCnt': clearCnt,
#         'createDt': createDt,
#         'deathCnt': deathCnt,
#         'decideCnt': decideCnt,
#         'examCnt': examCnt,
#         'resutlNegCnt': resutlNegCnt,
#         'seq': seq,
#         'stateDt': stateDt,
#         'stateTime': stateTime,
#         'updateDt': updateDt,
#     })
#     df = pd.DataFrane(rows, columns=cols)
#     df.to_csv('covid.csv')