from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DexSerializer
import subprocess
from .models import SrcDex, UserDex
import pandas as pd
from datetime import datetime, timedelta
import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scraper.scraper.spiders.crawler import IndicesInfoSpider, IndexHistorySpider
from scrapy.settings import Settings
from scraper.scraper import settings as my_settings

# Create your views here.
class DexListView(APIView):
    #This is the View FOR USERS to get all Dexes
    def get(self, request):
        srcDexList = SrcDex.objects.all()
        srcDexSerializer = DexSerializer(srcDexList, many=True)
        return Response(srcDexSerializer.data, status=status.HTTP_200_OK)

    def post(self, request):
    #This is the View FOR DEVELOPERS to update every Dex(title, closing) from the web
        try:
            subprocess.call("cd scraper && scrapy crawl indicesinfo --nolog", shell=True)
            return Response({"detail": "Database updated."}, status=status.HTTP_201_CREATED)
        except:
            return Response({"detail": "Error while crawling."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DexDetailView(APIView):
    def get(self, request, dex_id):
        try:
            srcDex = SrcDex.objects.get(id=dex_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DexSerializer(srcDex)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, dex_id):
    #This is the View FOR DEVELOPERS to update a selected Dex(values) from the web
        srcDex = SrcDex.objects.get(id=dex_id)
        url = srcDex.url
        try:
            # 해당 url에 대한 크롤링 실행
            subprocess.call(f"cd scraper && scrapy crawl indexhistory -a URL={url} --nolog", shell=True)
            # process = CrawlerRunner(get_project_settings())
            # process.crawl(IndexHistorySpider, URL=url)
        except Exception as e:
            print(e)
            return Response({"detail": "Error scraping data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"detail": "Database updated."}, status=status.HTTP_200_OK)
    
    def put(self, request, dex_id):
        date_range = [datetime.today().date() - timedelta(days=i) for i in range(31)]
        formatted_indices = [datetime.strptime(date.strftime("%Y-%m-%d"), "%Y-%m-%d") for date in date_range]
        df = pd.DataFrame(index=formatted_indices)

        srcDex = SrcDex.objects.get(id=dex_id)
        src_dict = srcDex.values
        src_df = pd.DataFrame.from_dict(src_dict, orient='index', columns=['src'])
        src_df.index = pd.to_datetime(src_df.index, format='%m/%d/%Y')
        df = df.merge(src_df, left_index=True, right_index=True, how='left')

        compare_list = request.data['indices']
        for index in compare_list:
            compare_dict = SrcDex.objects.get(id=index).values
            compare_df = pd.DataFrame.from_dict(compare_dict, orient='index', columns=[f'{index}'])
            compare_df.index = pd.to_datetime(compare_df.index, format='%m/%d/%Y')
            df = df.merge(compare_df, left_index=True, right_index=True, how='left')
            
        df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace(',',''), errors='coerce'))
        coefs = df.corrwith(df['src'], numeric_only=True)
        filtered_coefs = coefs[abs(coefs) > 0.7]
        if filtered_coefs.empty:
            filtered_coefs = coefs[abs(coefs) > 0.5]
        sorted_coefs = filtered_coefs.abs().sort_values(ascending=False)
        ordered_indices = sorted_coefs.index.tolist()
        ordered_indices.pop(0)
        if len(ordered_indices) > 5:
            ordered_indices = ordered_indices[:5]

        json_tags = {}
        for idx in ordered_indices:
            json_tags[idx] = round(coefs[idx], 3)

        srcDex.tags = json_tags
        srcDex.save()
        serializer = DexSerializer(srcDex)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDexView(APIView):
    def post(self, request, dex_id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials not provided"}, status=status.HTTP_401_UNAUTHORIZED)

        ### 1 ###
        try:
            srcDex = SrcDex.objects.get(id=dex_id)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        ### 2 ###
        userDex_list = srcDex.userdex_set.filter(user=request.user)

        ### 3 ###
        if userDex_list.count() > 0:
            srcDex.userdex_set.get(user=request.user).delete()
        else:
            UserDex.objects.create(user=request.user, srcDex=srcDex)

        serializer = DexSerializer(instance=srcDex)
        return Response(serializer.data, status=status.HTTP_200_OK)
