from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DexSerializer
import subprocess
from .models import SrcDex, UserDex, HankyungTitle
from datetime import datetime
from .dftools import get_tags_from_corr, merge_compare_df, merge_src_df, get_date_information
from .ecos import get_statistic
from .codes import statistic_codes
from .utils import generate_summary

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
            print("Crawling all done at {}".format(datetime.now()))
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
            print("Crawling index {} done at {}".format(dex_id, datetime.now()))
        except Exception as e:
            print(e)
            return Response({"detail": "Error scraping data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"detail": "Database updated."}, status=status.HTTP_200_OK)
    
    def put(self, request, dex_id):
        # get date-dataframe of 31 days
        df = get_date_information(datetime.today())

        # get SrcDex object
        src_obj = SrcDex.objects.get(id=dex_id)

        # add src data to df
        src_dict = src_obj.values
        df = merge_src_df(src_dict, df)

        # add compare data to df
        compare_list = request.data['indices']
        for index in compare_list:
            compare_dict = SrcDex.objects.get(id=index).values
            df = merge_compare_df(index, compare_dict, df)
        
        # get correlation between src compare data
        json_tags = get_tags_from_corr(df)

        # save data
        src_obj.tags = json_tags
        src_obj.save()
        serializer = DexSerializer(src_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDexView(APIView):
    def get(self, request):
        if SrcDex.objects.exists():
            return Response({"is_empty": False}, status=status.HTTP_200_OK)
        else:
            return Response({"is_empty": True}, status=status.HTTP_200_OK)

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

class EcoDexView(APIView):
    # ECOS API
    def get(self, request):
        pass
    def post(self, request):
        try:
            for code in statistic_codes:
                get_statistic(code[-1], code[0], code[1])
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "Error scraping data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class HankyungView(APIView):
    def get(self, request):     # need to be modified
        try:
            news_titles = HankyungTitle.objects.values_list('title', flat=True)[:90]
            news_titles = "\n".join(news_titles)
            summaries = generate_summary(news_titles)
            return Response({"summaries": summaries}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"detail": "Error summurizing news."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 한국경제 크롤링
    def post(self, request):
        try:
            subprocess.call(f"cd scraper && scrapy crawl hankyung --nolog", shell=True)
            print("Crawling Hankyung done at {}".format(datetime.now()))
            return Response({"detail": "Database updated."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": "Error scraping data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)