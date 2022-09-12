from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views import View

from .models import *
from capstoneApp.serializers import UserinfoSerializer, Item_ListSerializer
from ml import predict_0704

import numpy as np
import subprocess
import json
import pandas as pd
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
import pymysql.cursors


def index():
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print(data)
        if userinfo.objects.filter(userid=data['userid']).exists():
            obj = userinfo.objects.get(userid=data['userid'])
            if obj.password == data['password']:
                return JsonResponse({'code': '0000', 'msg': '로그인 성공'}, status=200)
            else:
                return JsonResponse({'code': '0001', 'msg': '비밀번호 불일치'}, status=200)
        else:
            return JsonResponse({'code': '0002', 'msg': '아이디가 존재하지 않음'}, status=200)
    else:
        return JsonResponse({'code': '0003', 'msg': '통신이 원할하지않습니다.'}, status=500)


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        if userinfo.objects.filter(userid=data['userid']).exists():
            return JsonResponse({'code': '0000', 'msg': '이미 등록된 아이디가 있습니다.'}, status=200)
        elif len(data['password']) < 6:
            return JsonResponse({'code': '0001', 'msg': '비밀번호를 6자 이상으로 설정해주세요.'}, status=200)
        else:
            serializer = UserinfoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'code': '0002', 'msg': '회원가입에 성공하였습니다.'}, status=200)
    else:
        return JsonResponse({'code': '1231', 'msg': '포스트로 보낵라...'}, status=500)


@csrf_exempt
def textrunning(request):
    if request.method == 'POST':
        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
            database="capstoneapi",
            charset='utf8'
        )
        curs = conn.cursor()  # 오브젝트 가져오기
        # test.json 넣을 시 ~~.json, .txt 변경
        # subprocess.run('python ml/predict_0704.py ml/dataset/testdata/testdata.txt', shell=True)
        subprocess.run('python ml/predict_0704.py ml/dataset/testdata/testdata.json', shell=True)

        pre_data = 'ml/dataset/predict_data/predict_list(*).json'

        with open(pre_data, 'r', encoding="UTF-8") as json_file:
            db_data = json.load(json_file)
            # db_line : json 객체를 가지는 Array
            db_line = db_data['item_list']

            for a in db_line:
                item_id = a["item_id"]
                item_name = a['item_name']

                sql = "REPLACE INTO item_list(item_id, item_name) VALUES (%s, %s)"
                # 똑같은 고유 번호(item_id) 있을 경우 정합 충돌 방지 = replace 사용
                val = (int(item_id), str(item_name))

                curs.execute(sql, val)
            conn.commit()
        print(curs.rowcount, "record inserted")

        # if request.method == 'POST':
        #     data = JSONParser().parse(request)
        #     # data = json.loads(request)
        #     path = 'ml/dataset/testdata/testdata.json'
        #
        #     with open(path, 'w', encoding="UTF-8") as f:
        #         json.dump(data, f, indent=2, ensure_ascii=False)
        # item_list.object.create(item_name=pre_data["food_name"])

        # df = pd.json_normalize(db_data)
        #
        # for idx, row in df.iterrows():
        #     item_list.objects.create(item_id=row['food_list.food_num'], item_name='김치')

        serializer = Item_ListSerializer(data=db_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse({'code': '0000', "msg": '보내짐'}, status=200)

    else:
        return JsonResponse({"msg": 'connection fail'}, status=500)
