# -*- coding: utf-8 -*-
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from xml.etree.ElementTree import ElementTree, Element, SubElement, dump

GDOC_ID = 'GDOC_ID'  # 구글 스프레드시트 독 아이디
JSON_KEY_PATH = 'google-sheets-api.json'  # 구글 키 저장 경로
VALUES_PATH = '../app/src/main/res_down'  # 저장될 별도의 리소스 폴더
SUPPORTED_LANGUAGE = ['ko', 'en', 'ja']
DEFAULT_LANGUAGE = 'en'

''' 
pip install gspread oauth2client
     
'''

def get_gdoc_information_ios():
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_PATH, scope)
    # test 현재경로
    # VALUES_PATH = os.getcwd()
    # 구글 로그인
    gc = gspread.authorize(credentials)
    # 시트오픈
    sh = gc.open_by_key(GDOC_ID)
    # Select worksheet by index. Worksheet indexes start from zero
    worksheet = sh.sheet1

    # 폴더가 없으면 만들어준다
    if not os.path.exists(VALUES_PATH):
        os.makedirs(VALUES_PATH)

    all_records = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')

    for language in SUPPORTED_LANGUAGE:
        if language == DEFAULT_LANGUAGE:
            output_path = VALUES_PATH + "/" + "Base.lproj"
        else:
            output_path = VALUES_PATH + "/" + language + ".lproj"

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file = output_path + "/Localizable.strings"

        output_stream = open(output_file, "w")
        for record in all_records:
            if record[language] != "":
                string = record[u'ios_key'] + u"=" + record[language] + ";\n"
                output_stream.write(string.encode('utf-8'))
        output_stream.close()


if __name__ == '__main__':
    get_gdoc_information_ios()
