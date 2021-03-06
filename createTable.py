# -*- coding:utf-8 -*-
from views import db
from views import init_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = init_app()

db.create_all(app=app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.run()
