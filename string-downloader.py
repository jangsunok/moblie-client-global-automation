# -*- coding: utf-8 -*-
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from xml.etree.ElementTree import ElementTree, Element, SubElement, dump

''' 
pip install gspread oauth2client
     
'''

GDOC_ID = 'GDOC_ID'  # 구글 스프레드시트 독 아이디
JSON_KEY_PATH = 'google-sheets-api.json'  # 구글 키 저장 경로
VALUES_PATH = '../app/src/main/res_down'  # 저장될 별도의 리소스 폴더
SUPPORTED_LANUAGE = ['ko', 'en', 'ja']
DEFAULT_LANGUAGE = 'en'


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def get_gdoc_information_android():
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
        resources = Element("resources")
        for record in all_records:
            if record[language] != "":
                SubElement(resources, "string", name=record[u'android_key']).text = record[language]

        if language == DEFAULT_LANGUAGE:
            PATH = os.path.join(VALUES_PATH, "values")
        else:
            PATH = os.path.join(VALUES_PATH, "values-" + language)

        if not os.path.exists(PATH):
            os.makedirs(PATH)

        indent(resources)
        ElementTree(resources).write(os.path.join(PATH, "strings.xml"), encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    get_gdoc_information_android()
