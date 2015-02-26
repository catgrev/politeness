import sys
import os
import smtplib
from app import app
from flask import make_response, request, current_app
from functools import update_wrapper
import json
import cPickle as pickle
import datetime
from datetime import timedelta
from politeness import model
from flask_politeness import add_together

SENDMAIL = "/usr/sbin/sendmail" # sendmail location
print 'loaded classifier'

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route('/index')
def index():
    return "Hello, World! cross 2"

@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def login():
    try:
        if request.method == 'POST':
            try:
                user = request.form[u'username']
                res = {}
                if user == 'https://www.facebook.com/catgrev':
                    res['login'] = True
                else:
                    res['login'] = True #change to false for study
                return json.dumps(res)
            except KeyError:
                raise ValueError("Using POST. No sentence detected.")
        else:
            return "Using GET. Use POST instead. "
    except ValueError as e:
        errres = {}
        errres['login'] = False
        return json.dumps(errres)

@app.route('/access', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def access():
    try:
        if request.method == 'POST':
            try:
                access = request.form[u'access']
                res = {}

                print access

                print os.path.join(os.path.split(__file__)[0],'access.txt')
                f = open(os.path.join(os.path.split(__file__)[0],'access.txt'), 'a+')
                f.write(str(datetime.datetime.utcnow())+"\t")
                f.write(str(access)+"\n")
                f.close()

                if access == '1001':
                    res['access'] = True
                else:
                    res['access'] = True #change to false for study                                                                          
                return json.dumps(res)
            except KeyError:
                raise ValueError("Using POST. No sentence detected.")
        else:
            return "Using GET. Use POST instead. "
    except ValueError as e:
        errres = {}
        errres['access'] = False
        return json.dumps(errres)

@app.route('/submit', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def submit():
    try:
        if request.method == 'POST':
            try:
                text = request.form[u'text'].encode('utf-8')
                print text
                res = {}

                print os.path.join(os.path.split(__file__)[0],'survey.txt')
                f = open(os.path.join(os.path.split(__file__)[0],'survey.txt'), 'a+')
                f.write(str(datetime.datetime.utcnow())+"\t")
                f.write(str(text)+"\n")
                f.close()

                #p = os.popen("%s -t" % SENDMAIL, "w")
                #p.write("To: catgrev@gmail.com\n")
                #p.write("Subject: From submit\n")
                #p.write("\n") # blank line separating headers from body                            
                #p.write(text)
                #p.write("\n")
                #sts = p.close()
                #if sts != 0:
                #    print "Sendmail exit status", sts
             
                return json.dumps(res)
            except KeyError:
                raise ValueError("Using POST. No sentence detected.")
        else:
            return "Using GET. Use POST instead. "
    except ValueError as e:
        print e
        errres = {}
        errres['access'] = False
        return json.dumps(errres)


@app.route('/politeness',methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*')
def politeness():
    '''Method to get politeness score'''
    try:
        if request.method == 'POST':
            try:
                #f = open('log.txt', 'a+')
                sentence = request.form[u'sentence']
                #f.write(sentence+"\n")
                #f.close
                try:
                    result = model.get_score(sentence)
                except Exception as e:
                    #print e, "for sentence: ", sentence
                    print "ERROR ",sys.exc_info()[0]
                    raise ValueError(sentence,'There is a problem: {0}'.format(e))
                if(request.form.has_key('pthr')): pthr = float(request.form[u'pthr'])
                else: pthr = 0.15
                if(request.form.has_key('ipthr')): ipthr = float(request.form[u'ipthr'])
                else: ipthr = 0.15
                ipthreshold = ipthr
                pthreshold = pthr
                print result
                ans = 'Impolite' if (result['impolite'] >= (.5 + ipthreshold)) else ('Neutral' if (result['impolite'] >= (0.5 - pthreshold)) else 'Polite')
                res = {}
                res['score'] = ans
                res['value'] = result
                res['msg'] = "Fine"
                if(request.form.has_key('txt')):res['txt'] = request.form[u'txt']
                if(request.form.has_key('id')): res['id'] = request.form[u'id']
                
                access = ''
                if(request.form.has_key('access')):access = request.form[u'access']

                print os.path.join(os.path.split(__file__)[0],'impolite.txt')
                f = open(os.path.join(os.path.split(__file__)[0],'impolite.txt'), 'a+')
                f.write(str(datetime.datetime.utcnow())+"\t")
                f.write(str(res)+"\t"+access+"\n")
                f.close()
                
                return json.dumps(res)

            except KeyError:
                raise ValueError("Using POST. No sentence detected.")
        else:
                return "Using GET. Use POST instead. "
    except ValueError as e:
        errres = {}
        errres['score'] = 'Neutral'
        errres['value'] = {}
        errres['msg'] = str(e)
        #if(request.form.has_key('txt')):erres['txt'] = request.form[u'txt']
        #if(request.form.has_key('id')): erres['id'] = request.form[u'id']
        return json.dumps(errres)
