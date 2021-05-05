from flask import render_template, request, Blueprint
from flaskbook.modelss import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    stranica = request.args.get('pageee', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=stranica, per_page=2)
    return render_template('home.html', posts=posts)