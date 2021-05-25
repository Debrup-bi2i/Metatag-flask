import os
import random
import time
from flask import Flask, json, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask_mail import Mail, Message
from celery import Celery
import numpy as np
import pandas as pd
import time
from pandas.core.frame import DataFrame
import requests
from requests.exceptions import ConnectionError
from urllib.parse import urlparse, urljoin
import random
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import base64
import re
import os
import time
#from flask.ext.mysql import MySQL
import pandas as pd



list_comb=['ar/es',
 'bo/es',
 'br/pt',
 'ca/en',
 'ca/fr',
 'lamerica_nsc_carib/en',
 'cl/es',
 'co/es',
 'ec/es',
 'lamerica_nsc_cnt_amer/es',
 'mx/es',
 'py/es',
 'pe/es',
 'pr/es',
 'us/en',
 'uy/es',
 've/es',
 'au/en',
 'cn/zh',
 'hk/en',
 'hk/zh',
 'in/en',
 'id/en',
 'kr/ko',
 'my/en',
 'nz/en',
 'ph/en',
 'sg/en',
 'tw/zh',
 'th/en',
 'vn/en',
 'emea_africa/en',
 'emea_africa/fr',
 'at/de',
 'by/ru',
 'be/fr',
 'be/nl',
 'bg/bg',
 'hr/hr',
 'cz/cs',
 'dk/da',
 'ee/et',
 'fi/fi',
 'fr/fr',
 'de/de',
 'gr/el',
 'hu/hu',
 'ie/en',
 'il/he',
 'it/it',
 'kz/ru',
 'lv/lv',
 'lt/lt',
 'emea_middle_east/ar',
 'emea_middle_east/en',
 'nl/nl',
 'no/no',
 'pl/pl',
 'pt/pt',
 'ro/ro',
 'ru/ru',
 'sa/ar',
 'sa/en',
 'rs/sr',
 'sk/sk',
 'si/sl',
 'za/en',
 'es/es',
 'se/sv',
 'ch/de',
 'ch/fr',
 'tr/tr',
 'ua/ru',
 'ua/uk',
 'uk/en',
 've/en',
 'jp/ja',
 'si/si',
 'rs/rs']
class my_dictionary(dict): 
 
    def __init__(self): 
        self = dict() 
 
    def add(self, key, value): 
        self[key] = value 
dict_metatag=my_dictionary()
def path_extrt(url):
    fr=""
    sc=""
    fl_nm=""
    pattern=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/[a-z]+\-[a-z]+"
    pat=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/"
    pattern1=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/[a-z]+\/[a-z]+"
    pat1=r"^https://[a-zA-Z0-9]+\.[hp]+\.com/"
    pattern2=r"^https://www.omen.com/[a-z]+\/[a-z]+"
    pat2=r"^https://www.omen.com/"
    if re.search(pattern,url):
        fr=re.findall(pattern,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat,url)[0]
    elif re.search(pattern1,url):
        fr=re.findall(pattern1,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat1,url)[0]
    elif re.search(pattern2, url):
        fr=re.findall(pattern2,url)[0]
        sc=re.sub(fr, "",url)
        fr=re.findall(pat2,url)[0]
    fl_nm=fr+sc
    fl_nm=fl_nm.replace("/","_").replace('.',"").replace(':',"")
       
    return fr,sc,fl_nm
def tag_extractor(comb,url):
    """
    
    Parameters
    ----------
    comb : combination of locale.
    Returns
    -------
    dict_metatag1 :  A dictionary with all the 
    required metatags from the respective page.
    url1 : The url requested for.
    r1.url : The url, from where response is coming from
    """
    

    token=str(random.randint(0,1000))
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'cache-control': "no-cache",
                'postman-token': token
                }
    url1=path_extrt(url)[0]+comb+path_extrt(url)[1]
    print(url1)
    try:
        r1=requests.get(url1,headers=headers,timeout=30)
        print(url1)
        if r1.status_code==200:
        ###CHECKING IF IT's an Ok URL
            htmlcontent1 = r1.content
            # print(htmlcontent)
            soup1 = BeautifulSoup(htmlcontent1, "html.parser")
            dict_metatag1 = my_dictionary()
            for link in soup1.find_all("meta"):
                if link.get("name") != None:
                    if link.get("name") in [
                        "bu",
                        "sub_bu",
                        "flag_all",
                        "web_section_id",
                        "page_content",
                        "segment",
                        "lifecycle",
                        "user_profile",
                        "simple_title",
                        "analytics_template_name",
                        "product_service_name",
                        "analytics_section",
                        "hp_design_version",
                        "page_level",
                        "product_type",
                        "family"]:
                        dict_metatag1.add(link.get("name"), link.get("content"))
            print(dict_metatag1, url1)
            return dict_metatag1, url1, r1.url
                        

        else:
            url1 = path_extrt(url)[0]+re.sub("/","-",comb)+path_extrt(url)[1]
            try:
                r1=requests.get(url1,headers=headers, timeout=30)
                if r1.status_code==200:
                    htmlcontent1 = r1.content
        # print(htmlcontent)
                    soup1 = BeautifulSoup(htmlcontent1, "html.parser")
                    dict_metatag1 = my_dictionary()
                    for link in soup1.find_all("meta"):
                        if link.get("name") != None:
                            if link.get("name") in [
                                "bu",
                                "sub_bu",
                                "flag_all",
                                "web_section_id",
                                "page_content",
                                "segment",
                                "lifecycle",
                                "user_profile",
                                "simple_title",
                                "analytics_template_name",
                                "product_service_name",
                                "analytics_section",
                                "hp_design_version",
                                "page_level",
                                "product_type",
                                "family"]:
                                dict_metatag1.add(link.get("name"), link.get("content"))
                    #print(dict_metatag1, url1)
                    return dict_metatag1, url1, r1.url
                else:
                    pass
                
            except:
                pass
            
    except:
        url1 = path_extrt(url)[0]+re.sub("/","-",comb)+path_extrt(url)[1]
        try:
            r1=requests.get(url1,headers=headers, timeout=30)
            if r1.status_code==200:
                htmlcontent1 = r1.content
    # print(htmlcontent)
                soup1 = BeautifulSoup(htmlcontent1, "html.parser")
                dict_metatag1 = my_dictionary()
                for link in soup1.find_all("meta"):
                    if link.get("name") != None:
                        if link.get("name") in [
                            "bu",
                            "sub_bu",
                            "flag_all",
                            "web_section_id",
                            "page_content",
                            "segment",
                            "lifecycle",
                            "user_profile",
                            "simple_title",
                            "analytics_template_name",
                            "product_service_name",
                            "analytics_section",
                            "hp_design_version",
                            "page_level",
                            "product_type",
                            "family"]:
                            dict_metatag1.add(link.get("name"), link.get("content"))
                #print(dict_metatag1, url1)
                return dict_metatag1, url1, r1.url
        except:
            pass
##configure the log file        
def tag_extractor_wrap(cc_ll,master_url):
    """
    
    Parameters
    ----------
    cc_ll : combination of locale variant.
    Returns
    -------
    df1 : uses folder_tag_extractor as a intermediate function and wraps the 
    metatags within a dataframe.
    """
    dict2=my_dictionary()
    try:
        dict2, url, url2=tag_extractor(cc_ll,master_url)
        print(cc_ll, dict2)
        try:
            df1 = pd.DataFrame(
                columns=(
                    "url",
                    "primary_flag",
                    "redirect",
                    "redirected_url",
                   # "status",
                    "bu",
                    "web_section_id",
                    "page_content",
                    "segment",
                    "lifecycle",
                    "user_profile",
                    "simple_title",
                    "sub_bu",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section",
                    "hp_design_version",
                    "page_level",
                    "product_type",
                    "family"
                )
            )


            for col in df1.columns:
                if col == "url":

                    df1.loc[1, col] = url

                elif col=="primary_flag":

                    s=list()

                    for name in ["bu",
                "web_section_id",
                "page_content",
                "segment",
                "lifecycle",
                "user_profile",
                "simple_title"]:

                        s.append(dict2[name]==dict_metatag[name])

                    if all(s):
                        df1.loc[1,col] = 1
                    else:
                        df1.loc[1,col] = 0
                
                elif col == "redirect":

                    if url2 != url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0
                elif col=="redirected_url":
                    df1.loc[1,col]=url2
                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            print(df1)
            return df1
        except:
            df1 = pd.DataFrame(
                columns=(
                    "url",
                    "primary_flag",
                    "redirect",
                    "redirected_url",
                   # "status",
                    "bu",
                    "web_section_id",
                    "page_content",
                    "segment",
                    "lifecycle",
                    "user_profile",
                    "simple_title",
                    "sub_bu",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section",
                    "hp_design_version",
                    "page_level",
                    "product_type",
                    "family"
                )
            )


            for col in df1.columns:
                if col == "url":

                    df1.loc[1, col] = url

                elif col=="primary_flag":
                    df1.loc[1,col] = 0
                
                elif col == "redirect":

                    if url2!= url:
                        df1.loc[1, col] = 1
                    else:
                        df1.loc[1, col] = 0
                elif col=="redirected_url":
                    df1.loc[1,col]=url2
                else:
                    try:

                        df1.loc[1, col]=dict2[col]
                    except:
                        df1.loc[1, col]=""
            
            return df1
    
    except:
        print(cc_ll)
        pass
df = pd.DataFrame()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

 
from flask_mysqldb import MySQL
#import MySQLdb.cursors
#import re
  
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://metatag:bi2i@1234@localhost/metatag' 
db = SQLAlchemy(app) 
class metatag(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    result = db.Column(db.Text) 
    ref = db.Column(db.Text)
    col_list = db.Column(db.Text)
    validation = db.Column(db.Text)
    page = db.Column(db.Text)

  

  
  
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'metatag'
  
  
# mysql = MySQL(app)


# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'


# Initialize extensions
mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(email_data):
    """Background task to send an email with Flask-Mail."""
    msg = Message(email_data['subject'],
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)
col_list=["url",
    "flag",
    "redirect",
    "bu",
    "web_section_id",
    "page_content",
    "segment",
    "lifecycle",
    "user_profile",
    "simple_title",
    "hp_design_version",
    "page_level",
    "product_type",
    "family",
    "sub_bu",
    "analytics_template_name",
    "product_service_name",
    "analytics_section"
]
metatag_list=["bu",
            "sub_bu",
            "web_section_id",
            "page_content",
            "segment",
            "lifecycle",
            "user_profile"]


@celery.task(bind=True)
def long_task(self,url,col_list_filter,validation,page):
    #with app.app_context():


    #col_list='1,2,3,4,5,6,7,8,9,10'
    #response_list= request.json['idList1']
    col_list_filter = ' '.join([str(elem) for elem in col_list_filter])
    token=str(random.randint(0,1000))
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',

                    'cache-control': "no-cache",
                    'postman-token': token
                    }
    r1=requests.get(url,headers=headers,timeout=30)
    if r1.status_code==200:
        htmlcontent = r1.content
    ##print(htmlcontent)
        soup = BeautifulSoup(htmlcontent, "html.parser")
        
        for link in soup.find_all("meta"):
            if link.get("name") != None:
                if link.get("name") in [
                    "bu",
                    "sub_bu",
                    "web_section_id",
                    "page_content",
                    "segment",
                    "lifecycle",
                    "user_profile",
                    "simple_title",
                    "analytics_template_name",
                    "product_service_name",
                    "analytics_section",
                    "hp_design_version",
                    "page_level",
                    "product_type",
                    "family"]:
                    dict_metatag.add(link.get("name"), link.get("content"))
        metatag_ref = pd.DataFrame(
        columns=(
            "master_url",
            "bu",
            "web_section_id",
            "page_content",
            "segment",
            "lifecycle",
            "user_profile",
            "simple_title",
            "sub_bu",
            "analytics_template_name",
            "product_service_name",
            "analytics_section",
            "hp_design_version",
            "page_level",
            "product_type",
            "family"
            )
            )
       
        print(dict_metatag)
        for col in metatag_ref.columns:
                    if col == "master_url":
                        metatag_ref.loc[1, col] = url
                    else:
                        try:
                            metatag_ref.loc[1, col]=dict_metatag[col]
                        except:
                            metatag_ref.loc[1, col]=""
    
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    global res
    df = pd.DataFrame(
       columns=(
           "url",
           "redirect",
           "bu",
           "web_section_id",
           "page_content",
           "segment",
           "lifecycle",
           "user_profile",
           "simple_title",
           "page_level",
           "product_type",
           "family"
           "sub_bu",
           "analytics_template_name",
           "product_service_name",
           "analytics_section"
        
           )
           )
    #total = random.randint(10, 50)
    
    total=4
    url = url
    for i in range(total):
        l1=i*20
        l2=(i+1)*20
        args = ((b, url) for b in list_comb[l1:l2])
        with ThreadPoolExecutor(max_workers=20) as T:
            res = list(T.map(lambda p:tag_extractor_wrap(*p),args))
            for row in res:
                df=df.append(row)
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    df['index'] = list(range(len(df.index)))
    df=df.set_index('index')
    for i in range(len(df.index)):
                    t=list()
                    for col in metatag_list:
                            t.append(      
                            df.loc[i,col]==metatag_ref.loc[1,col])
                           
                    if all(t):    
                        df.loc[i,'flag']="1"
                    else:    
                        df.loc[i,'flag']="0"
    df=df[col_list]
    metatag_ref=metatag_ref.to_json(orient='index')
    df=df.to_json(orient='index')
    #if request.method == 'POST':
        #name = request.form['name']
        #age = request.form['age']
    
    
        #cursor.execute(''' INSERT INTO info_table VALUES(%s,%s)''',(name,age))
    #connection = mysql.connect()
    #mysql.connection.commit()
   # cursor.close()
    id=int(str(time.time_ns())[10:])

    admin = metatag(id=id, result= df, ref= metatag_ref,  col_list=col_list_filter,validation =validation,page=page) 
    db.session.add(admin) 
    db.session.commit()
    return {'current': 100, 'total': 100, 'status': col_list_filter,
            'result': id,  'url': metatag_ref}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html', email=session.get('email', ''))
    email = request.form['email']
    session['email'] = email

    # send the email
    email_data = {
        'subject': 'Hello from Flask',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }
    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash('Sending email to {0}'.format(email))
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST','GET'])
def longtask():
    url = request.form['url']
    col_list =request.form['idList1']
    validation =request.form['validation']
    page =request.form['page']
    task = long_task.apply_async(args=[url, col_list, validation, page])
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
            'url': task.info.get('url', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

@app.route('/user', methods=['GET' , 'POST'])
def user():
    # with open('./data.json', 'r') as myfile:
    #         data = myfile.read()
    #return res
    id = request.args.get('id')
    res= metatag.query.filter_by(id=id).first()
    #ref= metatag.query.filter_by(id=id).second()
    combine=json.dumps(res.result)
    df=json.dumps(res.ref)
    validation=json.dumps(res.validation)
    page=json.dumps(res.page)
    filter =res.col_list
    col_list = list(filter.split(","))
    print (res)
    data = {
        "output": combine,
        "output2": df,
        "col_list":col_list,
        "validation":validation,
        "page":page
    }
    #return data
    return render_template("results.html", jsonfile = data, mimetype="appication/json")
if __name__ == '__main__':
    app.run(debug=True,port=5003)
