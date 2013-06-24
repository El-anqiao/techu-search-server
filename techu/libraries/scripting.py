from generic import settings
from generic import R
import PyV8 
import json

class Scripting(object):
  def __init__(self, fn):
    self.fn = fn
  
  def __call__(self, *args, **kwargs):
    '''
    |  Javascript Scripting for responses with PyV8.
    |  JS code is passed through the request in the *callback* parameter.
    |  Used as a view decorator. Disable by setting `SCRIPTING = False` in *settings.py*.
    '''
    response = self.fn(*args, **kwargs)
    request = args[0]
    if not settings.SCRIPTING:
      return response
    if hasattr(response, 'content') and response.status_code == 200:
      if 'callback' in request.REQUEST:
        callback = request.REQUEST['callback']
        response_object = json.loads(response.content)
        js_context = PyV8.JSContext({ 'response' : response_object })
        js_context.enter()
        js_context.eval(callback)
        js_context.leave()
        return R(response_object)
    return response
        
