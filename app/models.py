from app import app, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    bucketlists = db.relationship('Bucketlist', backref='user', lazy='dynamic')

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<User %r>' % self.email

class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id')) #has to be similar to the table name that it's coming from
    items = db.relationship('BucketlistItem', backref='bucketlist', lazy='dynamic')

    def __init__(self, name, owner_id):
        self.owner_id = owner_id
        self.name = name

    def __repr__(self):
        return '<Bucketlist %r belongs>' % (self.name)


class BucketlistItem(db.Model):
    __tablename__ = 'BLitems'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(225))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __init__(self, description, bucketlist_id):
        self.description = description
        self.bucketlist_id = bucketlist_id

    def __repr__(self):
        return '<Item %r belongs to>' % (self.title)