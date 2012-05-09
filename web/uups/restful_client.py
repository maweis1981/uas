import urllib2
opener = urllib2.build_opener(urllib2.HTTPHandler)
request = urllib2.Request('http://192.168.91.171:8000/user/1234', data='put_data')
#request = urllib2.Request('http://localhost:8888/test/')
request.add_header('Content-Type', 'your/contenttype')
request.get_method = lambda: 'GET'
url = opener.open(request)
print url.read()
request.get_method = lambda: 'POST'
url = opener.open(request)
print url.read()
request.get_method = lambda: 'PUT'
url = opener.open(request)
print url.read()
request.get_method = lambda: 'DELETE'
url = opener.open(request)
print url.read()
