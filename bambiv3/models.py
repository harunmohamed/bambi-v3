from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bambiv3 import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

followers = db.Table(
	'followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

liked = db.relationship(
		'PostLike',
		foreign_keys='PostLike.user_id',
		backref='user', lazy='dynamic')

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	department = db.Column(db.String(20), nullable=False)
	student_number = db.Column(db.Integer(), unique=True, nullable=False)
	age = db.Column(db.Integer(), nullable=False)
	country = db.Column(db.String(20), nullable=False)
	hobby = db.Column(db.String(20), nullable=False)
	bio = db.Column(db.String(120), nullable=True)
	private = db.Column(db.Boolean, default=False, nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	products = db.relationship('Product', backref='author', lazy=True)
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	messages_sent = db.relationship('Message',
									foreign_keys='Message.sender_id',
									backref='author', lazy='dynamic')
	messages_received = db.relationship('Message',
										foreign_keys='Message.recipient_id',
										backref='recipient', lazy='dynamic')
	last_message_read_time = db.Column(db.DateTime)


	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id' : self.id}).decode('utf-8')


	@staticmethod
	def verify_reset_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)


	def __repr__(self):
		return f"User('{self.username}' , '{self.email}', '{self.image_file}')"

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		followed = Post.query.join(
			followers, (followers.c.followed_id == Post.user_id)).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return followed.union(own).order_by(Post.date_posted.desc())

	def like_post(self, post):
		if not self.has_liked_post(post):
			like = PostLike(user_id=self.id, post_id=post.id)
			db.session.add(like)

	def unlike_post(self, post):
		if self.has_liked_post(post):
			PostLike.query.filter_by(
				user_id=self.id,
				post_id=post.id).delete()

	def has_liked_post(self, post):
		return PostLike.query.filter(
			PostLike.user_id == self.id,
			PostLike.post_id == post.id).count() > 0

	def new_messages(self):
		last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
		return Message.query.filter_by(recipient=self).filter(
			Message.timestamp > last_read_time).count()


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100)) #nullable=False
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	image = db.Column(db.String(20))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	likes = db.relationship('PostLike', backref='post', lazy='dynamic')

	def __repr__(self):
		if self.title != None:
			return f"Post('{self.title}','{self.content}', '{self.date_posted}')"
		else:
			return f"Post({self.content}', '{self.date_posted}')"

class PostLike(db.Model):
	__tablename__ = 'post_like'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100)) #nullable=False
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	description = db.Column(db.Text, nullable=False)
	location = db.Column(db.String(50))
	price = db.Column(db.String(50))
	contact = db.Column(db.String(50))
	image1 = db.Column(db.String(20), nullable=False)
	#image2 = db.Column(db.String(20))
	#image3 = db.Column(db.String(20))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
			return f"Product('{self.title}','{self.description}', '{self.price}','{self.location}','{self.contact}','{self.image1}','{self.date_posted}')"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text) #db.String(140)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

