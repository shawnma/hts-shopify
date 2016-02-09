from bottle import route, run, template, response, abort
import draw, io, download

@route('/app/cert/preview/<pid>/<text>')
def index(pid, text):
    response.set_header('Content-Type', 'image/png')
    bytes = io.BytesIO()
    draw.draw('origin.png', text, bytes)
    return bytes.getvalue()

#download cert base OID
@route('/app/cert/download/<oid>/<idx>')
def index(oid, idx):
    props = download.fetch_prop(oid)
    id = int(idx)
    if props.has_key(id):
        text, prod_id = props[id]
        config = eval(open('%d/config.json' %(prod_id)).read())
        bytes = io.BytesIO()
        draw.draw('%d/origin.jpg' % (prod_id), text, bytes, config)
        response.set_header('Content-Type', 'image/jpg')
        return bytes.getvalue()
    abort(404)
run(port=9999)

