from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_PORT"] = 3307
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "projectSanguine"
    app.config["MYSQL_DB"] = "stranger_trash"
    mysql.init_app(app)
