import os
import unittest
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app


app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def tests():
    """Run all the tests"""
    test = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(test)


@manager.command
def make_db():
    """Create the database"""
    db.create_all()
    print("Database tables created successfully")


@manager.command
def drop_db():
    """Destroy the database"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Database tables deleted successfully")


if __name__ == '__main__':
    manager.run()
