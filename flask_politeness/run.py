#!/usr/bin/python2.7
from app import app
#from OpenSSL import SSL
#context = SSL.Context(SSL.SSLv23_METHOD)
#context.use_privatekey_file('/home/ubuntu/private-key.pem')
#context.use_certificate_file('/home/ubuntu/keys/niceonline.be.crt')

app.run(host='0.0.0.0', port=443, debug=True)
