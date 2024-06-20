from app import app, db
from app import User, Post, Comment, Category, Tag, Like

def populate_db():
    # Create sample users
    user1 = User(username='john_doe', email='john@example.com')
    user1.set_password('password123')
    user2 = User(username='jane_smith', email='jane@example.com')
    user2.set_password('password123')

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Create sample categories
    cat1 = Category(name='Technology')
    cat2 = Category(name='Lifestyle')
    db.session.add(cat1)
    db.session.add(cat2)
    db.session.commit()

    # Create sample tags
    tag1 = Tag(name='Python')
    tag2 = Tag(name='Flask')
    tag3 = Tag(name='Vue.js')
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()

    # Create sample posts
    post1 = Post(title='Introduction to Flask', content='Flask is a micro web framework for Python.', author=user1)
    post1.categories.append(cat1)
    post1.tags.extend([tag1, tag2])
    
    post2 = Post(title='Building Modern Web Apps with Vue.js', content='Vue.js is a progressive JavaScript framework.', author=user2)
    post2.categories.append(cat2)
    post2.tags.append(tag3)
    
    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    # Create sample comments
    comment1 = Comment(content='Great post!', user=user2, post=post1)
    comment2 = Comment(content='Very informative.', user=user1, post=post2)
    db.session.add(comment1)
    db.session.add(comment2)
    db.session.commit()

    # Create sample likes
    like1 = Like(user_id=user1.id, post_id=post1.id)
    like2 = Like(user_id=user2.id, post_id=post2.id)
    db.session.add(like1)
    db.session.add(like2)
    db.session.commit()

    print('Database populated with sample data.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
        populate_db()
