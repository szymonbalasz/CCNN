web: gunicorn ccnn.wsgi
heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git
if __name__ == '__main__':
    app.run(port=33507)
app.run(host='0.0.0.0')