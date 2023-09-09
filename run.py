from nymeria_enricher import create_app, Config

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=Config.APP_PORT)