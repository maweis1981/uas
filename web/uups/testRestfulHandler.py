from RESTHandler import *

class testHandler(RESTHandler):
  def get(self,id):
    return self.write('get %s' % id)

  def post(self, *args, **kwargs):
    return self.write('post')

  def put(self,id):
    return self.write('put %s' % id)

  def delete(self,id):
    return self.write('delete %s ' % id)
