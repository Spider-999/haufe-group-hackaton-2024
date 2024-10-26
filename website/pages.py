from flask import render_template, Blueprint, url_for, request, redirect, abort, current_app
from flask_login import login_required, current_user
from .forms import PartyPostForm, PartyPostComment, UpdateAccountForm
from .models import PartyPost, User, Participant, Comment
from . import db
import os, secrets
from PIL import Image


pages = Blueprint('pages', __name__)


@pages.route('/')
@login_required
def home():
    return render_template('pages/home.html', title='Home')  


@pages.route('/party')
@login_required
def party():
    party = PartyPost.query.order_by(PartyPost.date_posted.desc())
    return render_template('pages/party.html', title='Party', party=party)


@pages.route('/party/post', methods=['GET', 'POST'])
@login_required
def create_post():
    party_form = PartyPostForm()

    if party_form.validate_on_submit():
        if request.method == 'POST':
            party = PartyPost(title=party_form.title.data, content=party_form.content.data,
                              location=party_form.location.data, user=current_user)
            db.session.add(party)
            db.session.commit()

            return redirect(url_for('pages.party', title='Party', party=party))
        
    return render_template('pages/createpost.html', title='Party', party_form=party_form)


@pages.route('/party/post-<int:post_id>', methods=['GET', 'POST'])
@login_required
def party_post(post_id):
    post = PartyPost.query.get_or_404(post_id)
    comment_form = PartyPostComment()

    if not post:
        abort(403)

    if comment_form.validate_on_submit():
        comment = Comment(content=comment_form.content.data, user_id=current_user.id, post_id=post_id)
        db.session.add(comment)
        db.session.commit()

    return render_template('pages/partypost.html', title=post.title, post=post, comment_form=comment_form, comments=post.comments)


@pages.route('/party/post-<int:post_id>/join-party', methods=['GET', 'POST'])
@login_required
def update_participants(post_id):
    post = PartyPost.query.filter_by(id=post_id).first()
    participant = Participant.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if not post:
        abort(404)
    elif participant:
        # Delete participation
        db.session.delete(participant)
        db.session.commit()
    else:
        # Add participation
        participant = Participant(user_id=current_user.id, post_id=post.id)
        db.session.add(participant)
        db.session.commit()

    return redirect(url_for('pages.party_post', title=post.title, post=post, post_id=post.id))


def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    _, filext = os.path.splitext(form_picture.filename)
    picture_filename = rand_hex + filext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)
    output_size = (120,120)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    return picture_filename


@pages.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    update_form = UpdateAccountForm()

    if update_form.validate_on_submit():
        if update_form.picture.data:
            picture_file = save_picture(update_form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = update_form.username.data
        db.session.commit()
        print(db)
        return redirect(url_for('pages.profile'))
    elif request.method == 'GET':
        update_form.username.data = current_user.username

    img_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('pages/profile.html', image_file=img_file, form=update_form)
