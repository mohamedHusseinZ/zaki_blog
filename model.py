from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    workouts = db.relationship('Workout', backref='user', lazy=True)
    activities = db.relationship('Activity', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    nutrition_entries = db.relationship('Nutrition', backref='user', lazy=True)
    achievements = db.relationship('Achievement', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
        }

class Workout(db.Model):
    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'workout_id': self.workout_id,
            'user_id': self.user_id,
            'workout_date': self.workout_date.isoformat(),
            'workout_type': self.workout_type,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'notes': self.notes,
        }

class Activity(db.Model):
    activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer)
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'activity_date': self.activity_date.isoformat(),
            'activity_type': self.activity_type,
            'duration': self.duration,
            'notes': self.notes,
        }

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    goal_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Integer, nullable=False)
    current_value = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')

    progress_entries = db.relationship('Progress', backref='goal', lazy=True)

    def to_dict(self):
        return {
            'goal_id': self.goal_id,
            'user_id': self.user_id,
            'goal_type': self.goal_type,
            'target_value': self.target_value,
            'current_value': self.current_value,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
        }

class Progress(db.Model):
    progress_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=False)
    progress_date = db.Column(db.Date, nullable=False)
    progress_value = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'progress_id': self.progress_id,
            'user_id': self.user_id,
            'goal_id': self.goal_id,
            'progress_date': self.progress_date.isoformat(),
            'progress_value': self.progress_value,
        }

class Nutrition(db.Model):
    nutrition_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_calories = db.Column(db.Integer)
    total_protein = db.Column(db.Integer)
    total_carbs = db.Column(db.Integer)
    total_fats = db.Column(db.Integer)
    notes = db.Column(db.Text)

    meals = db.relationship('Meal', backref='nutrition', lazy=True)

    def to_dict(self):
        return {
            'nutrition_id': self.nutrition_id,
            'user_id': self.user_id,
            'date': self.date.isoformat(),
            'total_calories': self.total_calories,
            'total_protein': self.total_protein,
            'total_carbs': self.total_carbs,
            'total_fats': self.total_fats,
            'notes': self.notes,
        }

class Meal(db.Model):
    meal_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    nutrition_id = db.Column(db.Integer, db.ForeignKey('nutrition.nutrition_id'), nullable=False)
    meal_time = db.Column(db.DateTime, nullable=False)
    meal_type = db.Column(db.String(50))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fats = db.Column(db.Integer)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            'meal_id': self.meal_id,
            'user_id': self.user_id,
            'nutrition_id': self.nutrition_id,
            'meal_time': self.meal_time.isoformat(),
            'meal_type': self.meal_type,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,
            'description': self.description,
        }

class Achievement(db.Model):
    achievement_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    achievement_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    social_share = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'achievement_id': self.achievement_id,
            'user_id': self.user_id,
            'achievement_date': self.achievement_date.isoformat(),
            'description': self.description,
            'social_share': self.social_share,
        }

if __name__ == '__main__':
    app.run(debug=True)
