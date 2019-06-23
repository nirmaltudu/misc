'''
For more details about how wiki search works, refer to https://www.mediawiki.org/wiki/API:Main_page
'''
import urllib
import simplejson

API_SEARCH = 'https://en.wikipedia.org/w/api.php'
WIKI_BASE_URL = 'https://en.wikipedia.org/wiki/'

def searchParamsToUrl(params):
    # Python 'list comprehension'. This is same as,
    # -------------------------------------------
    # p = list()
    # for k, v in params.iteritems():
    #   s = '='.join([str(k), str(v)])
    #   p.append(s)
    # return '&'.join(p)
    # -------------------------------------------
    return '&'.join(['='.join([str(k), str(v)]) for k,v in params.iteritems()])

def urlencode(url):
    formatDict = { ' ' : '%20'}
    for k,v in formatDict.iteritems():
        url = url.replace(k, v)
    return url

def getParseUrl(page):
    page = urlencode(page)
    params = {
        "action": "parse",
        "page": page,
        "prop": "sections",
        "format": "json"
    }
    params = searchParamsToUrl(params)
    url = API_SEARCH + '?' + params
    return url

def getSearchUrl(query, limit=10):
    query = urlencode(query)
    query_params = { 'action': 'query',
                     'list': 'search',
                     'srlimit': limit,
                     'srprop': '',
                     'srsearch': query,
                     'format': 'json'}
    query_params = searchParamsToUrl(query_params)
    url = API_SEARCH + '?' + query_params
    return url

def search(query, limit=10):
    url = getSearchUrl(query, limit)
    response = urllib.urlopen(url)
    return ''.join(response.readlines())

def parse(title):
    url = getParseUrl(title)
    response = urllib.urlopen(url)
    return ''.join(response.readlines())

def getTitleContent(title):
    try:
        parsedJson = parse(title)
    except UnicodeEncodeError:
        # TODO: Handle this
        return list()
    jstr = simplejson.loads(parsedJson)
    return [i['line'] for i in jstr['parse']['sections']]

def getSearchResults(result):
    j = simplejson.loads(result)
    for page in j['query']['search']:
        title = page['title']
        wiki_url = WIKI_BASE_URL + title
        sections = getTitleContent(title)
        print "Title: %s" % title
        print "Link: %s" % wiki_url
        print "Contents: \n%s" % '\n'.join(['\t\t%s' % i for i in sections])

if __name__ == '__main__':
    query = raw_input("Type search key: ")
    res = search(query)
    getSearchResults(res)