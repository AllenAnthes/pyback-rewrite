from flask_security import RoleMixin, UserMixin

from pyback import db

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

channel_mods = db.Table('channels_mods',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'))
                        )


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'id: {self.id} | name: {self.name} | description: {self.description}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    slack_id = db.Column(db.String(32), index=True, unique=True)
    slack_name = db.Column(db.String(32), index=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'id: {self.id} | email: {self.email} | roles: {self.roles}'

    def __str__(self):
        return self.email


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    channel_id = db.Column(db.String(32), nullable=False)
    mods = db.relationship("User", secondary=channel_mods)
