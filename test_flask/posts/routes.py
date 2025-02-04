from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from test_flask import db
from test_flask.models import Post, Comment
from test_flask.posts.forms import PostForm, CommentForm
from test_flask.users.utils import save_posts_pictures

posts = Blueprint('posts', __name__)


@posts.route("/allpost")
@login_required
def allpost():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('allpost.html', posts=posts)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    picture_name = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_posts_pictures(form.picture.data)
        post = Post(title=form.title.data, content=form.content.data,
                    author=current_user, image_file=picture_name)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html',
                           title='Новый пост', form=form, image_file=picture_name, legend='Новый пост')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.comment.data, post_id=post_id,
                          username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        flash('Ваш комментарий добавлен!', 'success')
        return redirect(f'/post/{post_id}')
    return render_template('post.html', title=post.title, post=post, form=form)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_posts_pictures(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        image_file = url_for('static', filename='food_pics/' +
                                                post.image_file)
    return render_template('create_post.html', title='Обновление поста',
                           form=form,  image_file=image_file, legend='Обновление поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.allpost'))


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.username != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Ваш комментарий был удален!', 'success')
    return redirect(url_for('posts.post', post_id=comment.post_id))
