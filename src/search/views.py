from django.shortcuts import render
import requests
import re
import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import (
        HTTP_200_OK, 
        HTTP_400_BAD_REQUEST,
        HTTP_500_INTERNAL_SERVER_ERROR,
        HTTP_400_BAD_REQUEST
    )
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from search.serializers import SingleSearchSerializer,MultipleSearchSerializer
import os
BASE = os.path.dirname(os.path.abspath(__file__))

#Calling Algo Module's class Trie
from logic.algo import Trie

# Create your views here.

def validateRequest(request):
    '''
        This function is used to check weather the request parameter is given or not
    '''
    search_text = request.data['search_text']
    num = request.data['relevance_number']

    if search_text == '' or num == '':
        return False
    else: 
        return True

def cleanText(phrase):
    '''
        This function removes the special characters from the string so that we can get simple string for operation
    '''
    pattern=['[^!.?]+']

    for pat in pattern:
        return(re.findall(pat,phrase))


def getJsonData():
    '''
        This function is used for reading the json file and return the summary data.
    '''
    json_data = open(os.path.join(BASE, "data.json"))   
    full_data = json.load(json_data)
    return full_data


class SearchSingleText(APIView):
    '''
        This class based view is used accepting post request with single query string and relevance number and returned the matched data
    '''
    permission_classes = [AllowAny]
    serializer_class = SingleSearchSerializer
    def post(self, request, *args, **kwargs):
        try:
            valid = validateRequest(request)
            if valid == False:
                return Response({'status': False, 
                        'message': 'can not be empty',
                        'response' : None,
                        'request': request.data},
                    status=status.HTTP_400_BAD_REQUEST)
            
            i = 0
            lst = []
            dict = {}
            t = Trie()

            text = "".join(cleanText(request.data['search_text']))
            num = request.data['relevance_number']            
            
            #Creating the tree by calling algo module function add_word
            create_tree = t.add_word(text,0)
            data = getJsonData()
            
            for v in data["summaries"]:
                count_mached_text = 0
                simple_summary = "".join(cleanText(v['summary']))

                #searching for the query strings and getting count and query id from the algo module function count_match
                count_mached_text , found_query = t.count_match(simple_summary)

                if(count_mached_text > 0):
                    
                    #if list length equals to relevance number
                    if len(lst) == int(num):
                        break
                    dicto={}               
                    dicto['summery'] = v['summary']
                    dicto['id'] = v['id']
                    
                    lst.append(dicto)                
            
            return Response({'status': True, 
                            'message': "Result",
                            'summaries' : lst,
                            'request': request.data},
                            status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'status': False, 
                            'message': str(e),
                            'response' : None,
                            'request': request.data},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchMultipleText(APIView):
    '''
        This class based view is used accepting post request with multiple query string and single relevance number and returned the matched data
    '''
    permission_classes = [AllowAny]
    serializer_class = MultipleSearchSerializer

    def post(self, request, *args, **kwargs):
        try:
            valid = validateRequest(request)

            if valid == False:
                return Response({'status': False, 
                        'message': 'can not be empty',
                        'response' : None,
                        'request': request.data},
                    status=status.HTTP_400_BAD_REQUEST)

            dict = {}
            t = Trie()

            text = request.data['search_text']
            num = int(request.data['relevance_number'])
            
            if(len(text) == 1):
                cleaned_text = "".join(cleanText(text[0]))

                #Creating the tree by calling algo module function add_word
                create_tree = t.add_word(cleaned_text,0)
            else:
                i = 0
                lst = []

                for txt in range(len(text)):
                    cleaned_text = "".join(cleanText(text[txt]))

                    #Creating the tree by calling algo module function add_word
                    create_tree = t.add_word(cleaned_text,txt)

                data = getJsonData()               

                for v in data["summaries"]:
                    count_mached_text = 0

                    #searching for the query strings and getting count and query id from the algo module function count_match
                    count_mached_text , found_query = t.count_match(v['summary'])

                    if(count_mached_text > 0):

                         #if list length equals to relevance number
                        if len(lst) == request.data['relevance_number']:
                            break

                        dicto={}               
                        dicto['summery'] = v['summary']
                        dicto['id'] = v['id']

                        if found_query > -1:
                            dicto['query'] = text[found_query]

                        #calling external api for getting book author name
                        req = requests.post('https://ie4djxzt8j.execute-api.eu-west-1.amazonaws.com/coding', json={'book_id':v['id']})
                        if req.status_code == 200:
                            search_result = req.json()
                            dicto['author']= search_result['author']  

                        lst.append(dicto)

            return Response({'status': True, 
                            'message': "Result",
                            'Books' : lst,
                            'request': request.data},
                            status=status.HTTP_200_OK)
                            
        except Exception as e:
            return Response({'status': False, 
                            'message': str(e),
                            'response' : None,
                            'request': request.data},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)