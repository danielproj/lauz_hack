from app import app
from flask import render_template, Flask, request, jsonify, redirect, url_for, flash
from datetime import datetime
from elasticsearch import Elasticsearch
import json
import hashlib
import sys
import io
import os

sys.path.insert(1, '/video')
# from text_parser import parse
import text_parser
sys.path.insert(1, '/pdf')
import process_text
sys.path.insert(1, '/gpt')
import specific_prompts

es = es = Elasticsearch( # https://www.elastic.co/guide/en/elasticsearch/client/python-api/master/connecting.html
    [
        {
            'host':str('es01'),
            'port': 9200,
            'scheme': "https"
        }
    ], 
    http_auth=(str('elastic'), str('ISUKBwgSUM35zQgup4wz')),
    ca_certs="/elastic_search/certs/ca/ca.crt",
)

# Place holder when using flask as the entry point for the website
@app.route('/')
def home():
   return "Gina's bois"

@app.route('/template')
def template():
    return render_template('home.html')

# file upload
@app.route('/upload/pdf/', methods=['GET', 'POST'])
def uploadPDF():
    if request.method == 'POST':
        print(request.files)        
        if 'PDFFile' not in request.files:
            flash('No file part (HTML error)')
            return redirect(request.url)

        if len(request.files.getlist('PDFFile')) == 0:
            flash('No selected file')
            return redirect(request.url)
        
        # open file and parse it
        for uploaded_file in request.files.getlist('PDFFile'):
            if uploaded_file.filename != '':
                m = hashlib.sha256()
                m.update(bytes("{}".format(uploaded_file.filename), 'utf-8'))
                id=m.hexdigest()
                print(uploaded_file.filename, id)

                # all_of_it = uploaded_file.read()
                # print(all_of_it)

                uploaded_file.save("/pdf/tmp.pdf")

                parsed_obj = process_text.StructurePDF("/pdf/tmp.pdf")
                print(parsed_obj)
                

                # open file and parse it
                doc = {
                    "filetype": "pdf",   
                    "created_data": parsed_obj.created_data,
                    "created_by": parsed_obj.created_by,
                    "title": parsed_obj.title,
                    "full_text": parsed_obj.content,
                    'inserted_at': datetime.now(),
                }
                es_insert_worker(index="corpus", id=id, doc=doc)

        flash('File processed successfully')
        return redirect(request.url)
    return render_template('uploadPDF.html')

@app.route('/upload/video/', methods=['GET', 'POST'])
def uploadVideo():
    if request.method == 'POST':
        print(request.files)
        if 'VideoFile' not in request.files:
            flash('No file part (HTML error)')
            return redirect(request.url)

        if len(request.files.getlist('VideoFile')) == 0:
            flash('No selected file')
            return redirect(request.url)
        
        for uploaded_file in request.files.getlist('VideoFile'):
            if uploaded_file.filename != '':
                m = hashlib.sha256()
                m.update(bytes("{}".format(uploaded_file.filename), 'utf-8'))
                id=m.hexdigest()
                print(uploaded_file.filename, id)

                # all_of_it = uploaded_file.read()
                # print(all_of_it)

                uploaded_file.save("/video/tmp.txt")

                parsed_obj = text_parser.parse("/video/tmp.txt")

                # open file and parse it
                doc = {
                    "filetype": "video",   
                    "full_text": parsed_obj.full_text,
                    "timestamped_text": parsed_obj.timestamped_text,
                    'title': parsed_obj.title,
                    'timestamp': parsed_obj.timestamp,
                    'url': parsed_obj.url,
                    'course_title': parsed_obj.course_title,
                    'inserted_at': datetime.now(),
                }
                es_insert_worker(index="corpus", id=id, doc=doc)

        flash('File processed successfully')
        return redirect(request.url)
    return render_template('uploadVideo.html')

# Elastic search
def es_insert_worker(index: str, id: str, doc: dict):
    return es.index(index=index, id=id, document=doc)

@app.get('/es/queryTerm')
def es_query_term():
    query_body = {
        "query": {
            # "match": {
            #     "full_text": request.args.get('query'),
            # }
            "multi_match": {
                "query": request.args.get('query'),
                "fields": [ "full_text", "title", "course_title"] 
            },
        },
        "highlight": {
            "fields": {
                "full_text": {}
            }
        }
    }

    return es.search(index='corpus', body=query_body).body
   
@app.get('/es/queryAll')
def es_query_all():
    query_body = {
        "query": {
            "match_all": {
            }
        }
    }

    return es.search(index='corpus', body=query_body).body

def es_query_worker(term: str):
    query_body = {
        "query": {
            "multi_match": {
                "query": term,
                "fields": [ "full_text", "title" ] 
            },
        },
        "highlight": {
            "fields": {
                "full_text": {}
            }
        }
    }

    return es.search(index='corpus', body=query_body).body

user_cache = {}

# GPT3 API
# curl -i -H "Content-Type: application/json" -H "user-id: 1" -H "session-id: 1" -X POST -d '{"Term": "epfl", "Context": "university"}' https://api.henrybear327.com/get_explanation
@app.post('/get_explanation')
def ui_get_explanation():
    data = {}
    f = open('/tmp/data.json', 'w+')
    f.close()
    if os.stat("/tmp/data.json").st_size > 0:
        data = json.load(f)
        f.close()
    print("data", data)

    user_id = request.headers.get('user-id')
    session_id = request.headers.get('session-id')
    # print("request.headers", request.headers)

    term = request.json['Term'] 
    context = request.json['Context']

    explanation = specific_prompts.initial_gpt(term, context)

    if user_id is not None and session_id is not None:
        if user_id not in user_cache:
            user_cache[user_id] = {} # new user
        if session_id not in user_cache[user_id]: # new session
            # user_cache[user_id] = {} # clear history
            user_cache[user_id][session_id] = [term, ""] # new history

        ret = user_cache[user_id][session_id]
        ret[0] = term
        ret[1] += "\n\n" + term + "\n\n" + explanation
        user_cache[user_id][session_id] = ret
    print("ui_get_explanation (logging)", user_cache[user_id][session_id], user_id, session_id, term, context)

    with open('/tmp/data.json', 'w') as f:
        json.dump(data, f)

    return json.dumps({
        "explanation": explanation,
    })

# curl -i -H "Content-Type: application/json" -H "user-id: 1" -H "session-id: 1" -X POST -d '{"Question": "question"}' https://api.henrybear327.com/get_answer
@app.post('/get_answer')
def ui_get_answer():
    data = {}
    f = open('/tmp/data.json', 'w+')
    f.close()
    if os.stat("/tmp/data.json").st_size > 0:
        data = json.load(f)
        f.close()
    print("data", data)

    user_id = request.headers.get('user-id')
    session_id = request.headers.get('session-id')

    question = request.json['Question']
    step_1_result = specific_prompts.get_answer_step_1(query=question)
    print("step_1_result", step_1_result)

    if user_id is not None and session_id is not None:
        if user_id not in user_cache:
            user_cache[user_id] = {} # new user
        if session_id not in user_cache[user_id]: # new session
            # user_cache[user_id] = {} # clear history
            user_cache[user_id][session_id] = ["", ""] # new history

    term = user_cache[user_id][session_id][0]
    context = "" 
    title = ""
    no_result = False
    if "C" not in step_1_result:
        term = user_cache[user_id][session_id][0]
        ret = es_query_worker(term)
        # update context, title
        print("ret", ret)
        if len(ret["hits"]["hits"]) > 0:
            title = "{} ({})".format(ret["hits"]["hits"][0]["_source"]["title"], str(ret["hits"]["hits"][0]["_source"]["url"]).strip())
            context = ret["hits"]["hits"][0]["highlight"]["full_text"]
        else:
            no_result = True
            
    print("term, context, title", term, context, title)
    print("ui_get_answer (logging)", user_cache[user_id][session_id], user_id, session_id, term, context)

    if no_result == False:
        answer = specific_prompts.process_option(term, step_1_result, user_cache[user_id][session_id][1], term, context, title)

        if user_id is not None and session_id is not None:
            ret = user_cache[user_id][session_id]
            ret[1] += "\n\n" + question + "\n\n" + answer # the dialog
            user_cache[user_id][session_id] = ret
    else:
        answer = "You haven't seen this term anywhere"

    with open('/tmp/data.json', 'w') as f:
        json.dump(data, f)

    return json.dumps({
        "answer": answer,
    })