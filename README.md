<<<<<<< HEAD
politeness-classifier
=====================

An implementation of the classifier described in this paper. http://www.stanford.edu/~jurafsky/pubs/politeness-acl13.pdf

Setup instructions:
-------------------
The basic instructions to set up the Flask app have been adapted from this helpful tutorial [http://blog.garethdwyer.co.za/2013/07/getting-simple-flask-app-running-on.html].

With these modifications:
Create an EC2 instance with at least 3GB of RAM

To setup the webpage for the server: <br>
Instead of "sudo nano sitename.com" do "sudo nano sitename.conf" <br>
Instead of "sudo a2dissite default" -> "sudo a2dissite 000-default.conf"<br>
Instead of "sudo a2ensite sitename.com" -> "sudo a2ensite sitename.conf"<br>

The git repo would be the politeness classifier repo.

2) Setting up the core-nlp server

Follow these instructions:
https://bitbucket.org/torotoki/corenlp-python

The core-nlp server should be launched at port 8080.

3) Setting up the politeness classifier

In the flask_politeness/run.py add host='0.0.0.0' inside of run()<br>
Then: sudo python run.py

4) Making requests

Go to a browser, check for the EC2 public IP in the URL bar. 
Something other than a 404 page should appear.<br>
Go to the RESTClient installed on Firefox.<br>
Use the following config:<br>
Method => POST<br>
URL => http://yourIP:5000/politeness<br>
Header => Content-Type = application/x-www-form-urlencoded<br>
Body => sentence=\"your sentence goes here\"<br>

The politeness scores should appear.

Example request:<br>
"method":"POST","url":"http://yourIP:5000/politeness",
"body":"sentence=\"Please help me out here. Hi, woops, I really appreciate your unlikely honesty.\"",
"overrideMimeType":false,"headers":[["Content-Type","application/x-www-form-urlencoded"]]
=======
politeness
==========
>>>>>>> 0a7e546154dc7801929d6f01b21584dd6cb53366
