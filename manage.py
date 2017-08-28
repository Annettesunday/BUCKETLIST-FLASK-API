import unittest

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import config

from app import app, db
from app.models import User, Bucketlist, BucketlistItem


app.config.from_object(config.Config)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

# Usage: python manage.py test
@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
