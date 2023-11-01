from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Homepage redirects to most recent 10 posts."""

    posts = Post.query.order_by(Post.created_at()).limit(10).all()
    return render_template("/posts/all_posts.html", posts=posts)

@app.route('/404')
def page_not_found(e):
    """Error Page"""

    return render_template("/404.html"), 404


@app.route('/users/all_users')
def show_users():
    """Show a page with info on all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/all_users.html', users=users)


@app.route('/users/new', methods=["GET"])
def show_new_user():
    """Show a form to create a new user"""

    return render_template('users/new_user.html')


@app.route("/users/new", methods=["POST"])
def new_user():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users/user_details.html", user=new_user)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show a page with info on a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/user_details.html', user_id=user)


@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)

    
    return render_template('users/edit_user.html', user_id=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect("/users/user_details.html", user_id=user)


@app.route('/details/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")

    return redirect("/users/all_users.html")


"""Posts"""

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('/posts/user_posts.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('/post/edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    db.session.add(post)
    db.session.commit()
    flash(f"Post {post.title} edited.")

    return redirect("/posts/user_posts.html", post=post)


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post {post.title} deleted.")

    return redirect("/posts/all_posts.html")


"""Tags route"""
@app.route("/tags")
def tags_index():
    """show page with all tags"""

    tags= Tag.query.all()
    return render_template('/tags/index.html', tags=tags)

@app.route("/tags/new")
def new_tag_form():
    """create a new tag"""

    posts = Post.query.all()
    return render_template('/tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_id = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(Post.id)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag {new_tag.name} added.")

    return redirect("/tags/new.html")


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """shows a page with info for a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tag/show_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """shows a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('/tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_id = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter((Post.id.in_(Post.id)).all())

    db.session.add(tag_id)
    db.session.commit()
    flash(f"Tag {tag.name} edited.")

    return redirect('/tags/show_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.name} has been deleted.")

    return redirect("/tags/index.html")





