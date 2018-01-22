from emissary import app


@app.route('/', methods=['GET'])
def handle_root():
    return ('Root of emissary service', 200)
