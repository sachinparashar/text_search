TEXT SEARCH ENGINE

A project related to Book Search Engine. Searching in this project is implemented by using "Trie Algorithm".

Steps for installing the repository:-

Download the repository.

Steps:

1. After downloading, Goto text_search folder and run: pip3 install -r requirements.txt

2. After installing all the dependencies, create virtual environment called "venv".

3. After this, run : python manage.py migrate

4. Run: python manage.py runserver

There are Two Api's in this project:

##############################################################################################

FOR TASK ONE:-

First api: http://127.0.0.1:8000/search/searchSingleText/
accepts post request and two parameters:

a)search_text(Single string)

b)relevance_number

Request format:

{ "search_text": "your problems",

"relevance_number": 2 }

This api returns the search text related list of summeries with ids.

##############################################################################################

FOR TASK TWO:-

2.Second api: http://127.0.0.1:8000/search/multipleSearchText/

accepts post request and two parameters:

a)search_text(Multiple string)

b)relevance_number

Request format:

{

"search_text": ["your problems", "hello world"],

"relevance_number": 2

}

This api returns the search text related list of summeries, book id, query string, book author.

##############################################################################################

NOTE: Unit Test cases are not implement in this project
