import urllib2, base64, json
USER='3c6af81ed42a345711cb2080360cc81f'
PASS='0a012269d6e5f6f5c24901427a7031b4'

# we are finding first one. it has problem when there are multiple ones in one order
def fetch_prop(order_id):
    order = get_order(order_id)
    line_items = order['order']['line_items']
    result = {}
    for i, item in enumerate(line_items):
        if item.has_key('properties'):
            props = item['properties']
            for prop in props:
                if prop['name'] == 'yourtext':
                    result[i] = (prop['value'], item['product_id'])
    return result

def get_order(order_id):
    request = urllib2.Request("https://onesky-store.myshopify.com/admin/orders/%s.json?fields=line_items" %(order_id))
    base64string = base64.encodestring('%s:%s' % (USER, PASS)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    stream = urllib2.urlopen(request)
    result = stream.read()
    stream.close()
    return json.loads(result)

if __name__ == '__main__':
    o = fetch_prop('2314575878')
    print json.dumps(o, sort_keys=1,indent=2)
