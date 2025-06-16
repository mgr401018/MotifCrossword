from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crossword.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    hint = db.Column(db.String(200), nullable=False)
    literary_work = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    extra_info = db.Column(db.Text)
    start_x = db.Column(db.Integer)
    start_y = db.Column(db.Integer)
    orientation = db.Column(db.String(10))  # 'horizontal' or 'vertical'
    number = db.Column(db.Integer)
    level = db.Column(db.Integer, nullable=False, default=1)  # 1: Easy, 2: Medium, 3: Hard
    show_work_info = db.Column(db.Boolean, default=False)  # New field to control work info display

    def __repr__(self):
        return f'<Word {self.word}>'

# Initialize database
with app.app_context():
    db.create_all()
    # Add show_work_info column if it doesn't exist
    try:
        with db.engine.connect() as conn:
            conn.execute(text("ALTER TABLE word ADD COLUMN show_work_info BOOLEAN DEFAULT FALSE"))
            conn.commit()
    except Exception as e:
        print(f"Column might already exist: {str(e)}")
    print("Database initialized successfully")

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    try:
        words = Word.query.all()
        return render_template('admin.html', words=words)
    except Exception as e:
        print(f"Error in admin route: {str(e)}")
        return render_template('admin.html', words=[])

@app.route('/play')
def play():
    try:
        level = request.args.get('level', default=1, type=int)
        words = Word.query.filter_by(level=level).order_by(Word.number).all()
        return render_template('play.html', words=words, current_level=level)
    except Exception as e:
        print(f"Error in play route: {str(e)}")
        return render_template('play.html', words=[], current_level=level)

@app.route('/api/add_word', methods=['POST'])
def add_word():
    try:
        data = request.get_json()
        word = Word(
            word=data['word'],
            hint=data['hint'],
            literary_work=data['literary_work'],
            author=data['author'],
            year=data['year'],
            extra_info=data.get('extra_info', ''),
            level=data.get('level', 1),
            show_work_info=data.get('show_work_info', False)
        )
        db.session.add(word)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        print(f"Error adding word: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/update_word_position', methods=['POST'])
def update_word_position():
    data = request.get_json()
    word = Word.query.get(data['id'])
    if word:
        # Ensure coordinates are within 1-15 range
        x = int(data['start_x']) if data['start_x'] else None
        y = int(data['start_y']) if data['start_y'] else None
        
        if x is not None:
            x = max(1, min(15, x))
        if y is not None:
            y = max(1, min(15, y))
            
        word.start_x = x
        word.start_y = y
        word.orientation = data['orientation']
        word.number = data['number']
        word.level = data['level']
        word.show_work_info = data.get('show_work_info', False)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Word not found'}), 404

@app.route('/api/get_word_positions')
def get_word_positions():
    words = Word.query.filter(Word.start_x.isnot(None), Word.start_y.isnot(None)).all()
    positions = []
    for word in words:
        # Ensure coordinates are within 1-15 range
        x = max(1, min(15, word.start_x)) if word.start_x is not None else None
        y = max(1, min(15, word.start_y)) if word.start_y is not None else None
        
        positions.append({
            'id': word.id,
            'word': word.word,
            'start_x': x,
            'start_y': y,
            'orientation': word.orientation,
            'number': word.number
        })
    return jsonify(positions)

@app.route('/api/update_word', methods=['POST'])
def update_word():
    try:
        data = request.get_json()
        word = Word.query.get(data['id'])
        if word:
            word.word = data['word']
            word.hint = data['hint']
            word.literary_work = data['literary_work']
            word.author = data['author']
            word.year = data['year']
            word.extra_info = data.get('extra_info', '')
            word.level = data.get('level', 1)
            word.show_work_info = data.get('show_work_info', False)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'error': 'Word not found'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Error updating word: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    try:
        data = request.get_json()
        word = Word.query.get(data['id'])
        if word:
            db.session.delete(word)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'error': 'Word not found'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting word: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 