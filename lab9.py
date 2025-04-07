from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id}>'


with app.app_context():
    db.create_all()


@app.route('/clear', methods=['POST'])
def clear_reviews():
    Review.query.delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        review_text = request.form['text']
        review_rate = int(request.form['rate'])

        new_review = Review(text=review_text, rate=review_rate)
        db.session.add(new_review)
        db.session.commit()
        return redirect(request.url)

    reviews = Review.query.order_by(Review.date.desc()).all()
    avg = sum(r.rate for r in reviews) / len(reviews) if reviews else 0
    return render_template('index.html',
                           reviews=reviews,
                           avg_rating=round(avg, 1))


if __name__ == '__main__':
    app.run(debug=True)