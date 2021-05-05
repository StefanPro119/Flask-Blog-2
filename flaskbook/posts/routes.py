from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_required, current_user
from flaskbook.modelss import Post
from flaskbook import db
from flaskbook.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
    formation = PostForm()
    if formation.validate_on_submit():
        poster = Post(titlee=formation.title.data, contentt=formation.content.data, author=current_user)
        db.session.add(poster)
        db.session.commit()
        flash('Your Post has been created', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=formation)


@posts.route("/posts/<int:post_idi>")
def postff(post_idi):
    postff = Post.query.get_or_404(post_idi)
    return render_template('every_post.html', title=postff.titlee, post=postff)


@posts.route("/posts/<int:post_idi>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_idi):
    postff = Post.query.get_or_404(post_idi)
    if postff.author != current_user:
        abort(403)
    formation = PostForm()
    if formation.validate_on_submit():
        postff.titlee = formation.title.data
        postff.contentt = formation.content.data
        db.session.commit()
        flash("Your post has been updated", 'success')
        return redirect(url_for('posts.postff', post_idi=postff.idd)) #obrati paznju da ovde se za post_idi = koristi postff.idd, jer je definisan sa postff = Post.query.get_or_404(post_idi), dok u html na stranici every_post se poziva post.idd direktno iz modelss.py
    elif request.method == 'GET':
        formation.title.data = postff.titlee
        formation.content.data = postff.contentt
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=formation)

@posts.route("/posts/<int:post_idi>/delete", methods=['POST'])
@login_required
def delete_post(post_idi):
    postic = Post.query.get_or_404(post_idi)
    if postic.author != current_user:
        abort(403)
    db.session.delete(postic)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('main.home'))