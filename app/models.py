from app import db


class User(db.Model):
    """This class represents all users in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    password_encrypt = db.Column(db.String(200))
    bucketlist = db.relationship('Bucketlist', backref='user')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketlist(db.Model):
    """This class represents the Bucketlist table"""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """Initialize with name"""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class Item(db.Model):
    """This class represents the items table that are within the bucketlists"""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    bucketlist_owner = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
