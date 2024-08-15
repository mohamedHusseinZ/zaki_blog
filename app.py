from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import db, User, Post, Comment, Category, Tag, Like

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Helper function to create response
def create_response(data, status=200):
    return make_response(jsonify(data), status)

# User API routes
@app.route('/users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'GET':
        users = User.query.all()
        return create_response([user.to_dict() for user in users])
    elif request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return create_response(new_user.to_dict(), 201)

@app.route('/users/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(user.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        return create_response(user.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return create_response({'message': 'User deleted'})

# Post API routes
@app.route('/posts', methods=['GET', 'POST'])
def manage_posts():
    if request.method == 'GET':
        posts = Post.query.all()
        return create_response([post.to_dict() for post in posts])
    elif request.method == 'POST':
        data = request.json
        new_post = Post(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return create_response(new_post.to_dict(), 201)

@app.route('/posts/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(post.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'title' in data:
            post.title = data['title']
        if 'content' in data:
            post.content = data['content']
        db.session.commit()
        return create_response(post.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(post)
        db.session.commit()
        return create_response({'message': 'Post deleted'})

# Comment API routes
@app.route('/comments', methods=['GET', 'POST'])
def manage_comments():
    if request.method == 'GET':
        comments = Comment.query.all()
        return create_response([comment.to_dict() for comment in comments])
    elif request.method == 'POST':
        data = request.json
        new_comment = Comment(content=data['content'], user_id=data['user_id'], post_id=data['post_id'])
        db.session.add(new_comment)
        db.session.commit()
        return create_response(new_comment.to_dict(), 201)

@app.route('/comments/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_comment(id):
    comment = Comment.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(comment.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'content' in data:
            comment.content = data['content']
        db.session.commit()
        return create_response(comment.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(comment)
        db.session.commit()
        return create_response({'message': 'Comment deleted'})

# Category API routes
@app.route('/categories', methods=['GET', 'POST'])
def manage_categories():
    if request.method == 'GET':
        categories = Category.query.all()
        return create_response([category.to_dict() for category in categories])
    elif request.method == 'POST':
        data = request.json
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return create_response(new_category.to_dict(), 201)

@app.route('/categories/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(category.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'name' in data:
            category.name = data['name']
        db.session.commit()
        return create_response(category.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return create_response({'message': 'Category deleted'})

# Tag API routes
@app.route('/tags', methods=['GET', 'POST'])
def manage_tags():
    if request.method == 'GET':
        tags = Tag.query.all()
        return create_response([tag.to_dict() for tag in tags])
    elif request.method == 'POST':
        data = request.json
        new_tag = Tag(name=data['name'])
        db.session.add(new_tag)
        db.session.commit()
        return create_response(new_tag.to_dict(), 201)

@app.route('/tags/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_tag(id):
    tag = Tag.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(tag.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'name' in data:
            tag.name = data['name']
        db.session.commit()
        return create_response(tag.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(tag)
        db.session.commit()
        return create_response({'message': 'Tag deleted'})

# Like API routes
@app.route('/likes', methods=['GET', 'POST'])
def manage_likes():
    if request.method == 'GET':
        likes = Like.query.all()
        return create_response([like.to_dict() for like in likes])
    elif request.method == 'POST':
        data = request.json
        new_like = Like(user_id=data['user_id'], post_id=data['post_id'])
        db.session.add(new_like)
        db.session.commit()
        return create_response(new_like.to_dict(), 201)

@app.route('/likes/<int:id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manage_like(id):
    like = Like.query.get_or_404(id)
    if request.method == 'GET':
        return create_response(like.to_dict())
    elif request.method in ['PUT', 'PATCH']:
        data = request.json
        if 'user_id' in data:
            like.user_id = data['user_id']
        if 'post_id' in data:
            like.post_id = data['post_id']
        db.session.commit()
        return create_response(like.to_dict())
    elif request.method == 'DELETE':
        db.session.delete(like)
        db.session.commit()
        return create_response({'message': 'Like deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=4433)





