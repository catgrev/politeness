from simplejson import loads
import jsonrpclib
import cPickle as pickle
import os.path

from politeness import model

server = jsonrpclib.Server("http://127.0.0.1:8080")

text = 'Please help me out here. Hi, woops, I really appreciate your unlikely honesty.'
        
print model.get_score(text)
