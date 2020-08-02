from app import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(host=app.config['HOST'], debug=True if app.config['FLASK_DEBUG'] is True else False, port=8080)
