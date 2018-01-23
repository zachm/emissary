from emissary import app


# Run the app in a single-threaded, hot-reloadable fashion.
# Do *NOT* use this in production. Debugging only!

app.debug = True
app.run(host='0.0.0.0', port=8008)
