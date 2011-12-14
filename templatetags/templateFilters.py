from google.appengine.ext import webapp

# get registry, we need it to register our filter later.
register = webapp.template.create_template_register()

def truncate(value, maxsize, stopper='...'):
    """ truncates a string to a given maximum
        size and appends the stopper if needed """
    stoplen = len(stopper)
    if len(value) > maxsize and maxsize > stoplen:
       return value[:(maxsize - stoplen)] + stopper
    else:
       return value[:maxsize]

register.filter(truncate)