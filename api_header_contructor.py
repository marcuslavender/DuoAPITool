import base64, email, hmac, json, hashlib, urllib, sys, requests


class api_call_generator:
    def __init__(self):

        self.method = sys.argv[1]
        self.host = sys.argv[2]
        self.path = sys.argv[3]
        self.params = sys.argv[4]
        self.skey = sys.argv[5]
        self.ikey = sys.argv[6]
        self.headers = None
	self.urlprefix = "https://"
	

    def print_help(self):
            print "python api_header_contructor.py $method <GET/PUT/POST> $host <API hostname> $path <API Call> $params <parameters required by API call> $skey <Secret Key>  $ikey <Integration key>"


    def sign(self, method, host, path, params, skey, ikey):
        """
        Return HTTP Basic Authentication ("Authorization" and "Date") headers.
        method, host, path: strings from request
        params: dict of request parameters
        skey: secret key
        ikey: integration key
        """

        # create canonical string
        now = email.Utils.formatdate()
        canon = [now, method.upper(), host.lower(), path]
        args = []
        for key in sorted(params.keys()):
            val = params[key]
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
	headers = {'Date':date, 'Authorization':authorization}

        return headers
        #return {'Date': now, 'Authorization': 'Basic %s' % base64.b64encode(auth)}



generator = api_call_generator()


if len(sys.argv) < 7:
    generator.print_help()



params = json.loads(generator.params)
print "params: ", str(params)


url = generator.urlprefix + generator.host + "/" + generator.path + '?' + "results" + "=" + params['results']
print "url", url 


generator.headers = generator.sign(generator.method, generator.host, generator.path, params, generator.skey, generator.ikey)
print "headers: ", str(generator.headers)


r = requests.get(url, headers=generator.headers)
print "response:", str(r)
