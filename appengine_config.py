from util.gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
	app = SessionMiddleware(app, cookie_key="\xcb\xd2\x9c\xbfZW\xab\xe9\xdb!5L\x80\xa0u\x0b\x05_>\xabn\xd6\xcf\xac`Zi\xe9\x14\xed\x80\xec\x9e\x95|\xd0;g\xa3^\x0ee\x86R\x0f\x90N\xdf\xb0\xbb\xf8\x8e\xd25\xd8\x8e\t\xb084o\x16\x07\x10")
	return app