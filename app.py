#The first thing you do when opening a new folder to start project is type in terminal: pip3 install flask
#To use a database from local sql, type in the terminal: pip3 install flask-sqlalchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Use the mysql database to create a prem schedule with home team, home score, away team, away score, win/loss/draw,

app = Flask(__name__)

#Setting up the database using alchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journals.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Fastboy2002@localhost/arsenalStats' #Setting up the database using mysql
db = SQLAlchemy(app)
dbStats = SQLAlchemy(app)

#Model for the datacase with columns id, title, content, author, and date posted.
class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default = 'Unknown')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #Display database content to the screen
    def __repr__(self):
        return 'Journal Entry ' + str(self.id)

#These are the columns for the database
class Ars_Stats(dbStats.Model):
    id = dbStats.Column(dbStats.Integer, primary_key=True)
    number = dbStats.Column(dbStats.Text, nullable=False)
    name = dbStats.Column(dbStats.String(100), nullable=False)
    games = dbStats.Column(dbStats.Text, nullable=False)
    goals = dbStats.Column(dbStats.Text, nullable=False)
    assists = dbStats.Column(dbStats.Text, nullable=False)
    shots = dbStats.Column(dbStats.Text, nullable=False)
    yellow_cards = dbStats.Column(dbStats.Text, nullable=False)
    red_cards = dbStats.Column(dbStats.Text, nullable=False)
    saves = dbStats.Column(dbStats.Text, nullable=False)
    clean_sheets = dbStats.Column(dbStats.Text, nullable=False)


#Routes for the pages
@app.route('/') #Home page of the website
def index():
    #Display the index.html webpage
    return render_template('index.html')

#Journal page
@app.route('/journal', methods=['GET', 'POST']) #Journal page of the website
def posts():
    #If the request method is post, collect the title, content, and author from the form on edit.html and add it to the database. Then display it
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = JournalEntry(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        #After updating the database, go back to the journal page
        return redirect('/journal')
    else:
        all_posts= JournalEntry.query.order_by(JournalEntry.date_posted).all()
        return render_template('journal.html', posts=all_posts)

#Delete a blogpost
@app.route('/journal/delete/<int:id>') #Route to delete a journal entry
def delete(id):
    post = JournalEntry.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/journal')

#Edit a blog post page
@app.route('/journal/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    #Get the post ID 
    post = JournalEntry.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/journal')
    else:
        return render_template('edit.html', post=post)

#New blog post page
@app.route('/journal/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = JournalEntry(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_entry.html')

#Arsenal Roster Page
@app.route('/roster')
def roster():
    return render_template('roster.html')

#Stats page
@app.route('/roster/stats')
def stats():
    return render_template('stats.html', player_query=Ars_Stats.query.all())

#One route is used to show the template
@app.route('/roster/stats/editPlayer', methods=['POST'])
def editStats():

    #Modify the player data based on the ID from the request form
    player = Ars_Stats.query.get_or_404(request.form['id'])

    if request.form["editStatus"]=='Edit':
        if request.method=='POST':
            return render_template('editPlayer.html', player=player)


    if request.form["editStatus"]=='Save':
        if request.method=='POST':
            player.games = request.form['games']
            player.goals = request.form['goals']
            player.assists = request.form['assists']
            player.shots = request.form['shots']
            player.yellow_cards = request.form['yellow_cards']
            player.red_cards = request.form['red_cards']
            player.saves = request.form['saves']
            player.clean_sheets = request.form['clean_sheets']
            dbStats.session.commit()
            return redirect('/roster/stats')

#About me page
@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')



if __name__ == "__main__":
    app.run(debug=True)