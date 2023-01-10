from pybo import rdb


class Question(rdb.Model):
    id = rdb.Column(rdb.Integer, primary_key=True)
    subject = rdb.Column(rdb.String(200), nullable=False)
    content = rdb.Column(rdb.Text(), nullable=False)
    create_date = rdb.Column(rdb.DateTime(), nullable=False)
    user_id = rdb.Column(rdb.Integer, rdb.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = rdb.relationship('User', backref=rdb.backref('question_set'))


class Answer(rdb.Model):
    id = rdb.Column(rdb.Integer, primary_key=True)
    question_id = rdb.Column(rdb.Integer, rdb.ForeignKey('question.id', ondelete='CASCADE'))
    question = rdb.relationship('Question', backref=rdb.backref('answer_set', ))
    content = rdb.Column(rdb.Text(), nullable=False)
    create_date = rdb.Column(rdb.DateTime(), nullable=False)
    user_id = rdb.Column(rdb.Integer, rdb.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = rdb.relationship('User', backref=rdb.backref('answer_set'))


class User(rdb.Model):
    id = rdb.Column(rdb.Integer, primary_key=True)
    username = rdb.Column(rdb.String(150), unique=True, nullable=False)
    password = rdb.Column(rdb.String(200), nullable=False)
    email = rdb.Column(rdb.String(120), unique=True, nullable=False)
