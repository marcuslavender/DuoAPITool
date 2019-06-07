import base64, email, hmac, json, hashlib, urllib, sys, requests, ast, httplib


def print_help():
    print """python api_header_contructor.py $method <GET/PUT/POST> $host <API hostname> $path <API Call> $params <parameters required by API call> $skey <Secret Key>  $ikey <Integration key>
             If no params are required enter 'no'
    """


class api_call_generator:
    def __init__(self,method,host,path,params,ikey,skey):

        self.method = method
        self.host = host
        self.path = path
        self.params = params
        self.ikey = ikey
        self.skey = skey
        self.headers = None
        self.urlprefix = "https://"

    def sign(self, method, host, path, params, skey, ikey):
        """
        Return HTTP Basic Authentication ("Authorization" and "Date") headers.
        method, host, path: strings from request
        params: dict of request parameters
        skey: secret key
        ikey: integration key
        """

        # create canonical string
        #now = email.Utils.formatdate()
        now = 'Mon, 20 May 2019 17:49:45 -0000'
        canon = [now, method.upper(), host.lower(), path]
        args = []
        for key in sorted(params.keys()):
            val = params[key]
            val = unicode(val,"utf-8")
            if isinstance(val, unicode):
                val = val.encode("utf-8")
                args.append(
                    '%s=%s' % (urllib.quote(key, '~'), urllib.quote(val, '~')))
        canon.append('&'.join(args))
        canon = '\n'.join(canon)

        # sign canonical string
        sig = hmac.new(skey, canon, hashlib.sha1)
        auth = '%s:%s' % (ikey, sig.hexdigest())
        authorization = 'Basic %s' % base64.b64encode(auth)
        date = now
        #date = 'Mon, 20 May 2019 17:49:45 -0000'
        headers = {'Date': date, 'Authorization': authorization}
        print headers
        #return headers
        return {'Date': now, 'Authorization': 'Basic %s' % base64.b64encode(auth)}


# check if enough parameters have been supplied at command line

if len(sys.argv) < 6:
    print_help()
    exit(1)



generator = api_call_generator(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])


# Check if any params have been passed and convert json formatted params to python dict object
if str(generator.params).lower() == 'no':
    print "No parameters provided, continuing"
    params = {}
else:
    params = json.dumps(json.loads(generator.params))
    params = ast.literal_eval(params)
    print "params: ", str(params)

# determine request type:
if generator.method == 'GET':
    if str(generator.params).lower() == 'no':
        url = generator.urlprefix + generator.host + "/" + generator.path
        print "url", url
    else:
        url = generator.urlprefix + generator.host + "/" + generator.path + '?' + "results" + "=" + params['results']
        print "url", url
elif generator.method == 'POST':
    pass
else:
    print "invalid method"

# create HMAC signature and store in the variable headers
generator.headers = generator.sign(generator.method, generator.host, generator.path, params, generator.skey,
                                   generator.ikey)
print "headers: ", str(generator.headers)
print ""
print ""
# make the call using requests library, supplying the headers returned from the signing method
httplib.HTTPConnection.debuglevel = 1
r = requests.get(url, headers=(generator.headers))
print "response:", str(r)
print ""
print r.status_code, r.headers, r.encoding, r.json(),
