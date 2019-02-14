from flask import render_template, request, redirect, url_for, flash, abort
from . import main
from .forms import PitchForm, UpdateProfile, CategoryForm, CommentForm, ContentForm
from flask_login import login_required, current_user
from ..models import User, Pitch, Comment, Like, Dislike, PhotoProfile, PitchCategory
from .. import db, photos
import markdown2


@main.route('/')
def index():

    category = PitchCategory.get_categories()
    pitches = Pitch.query.order_by('-id').all()
    print(pitches)

    title = 'Pitch'
    return render_template('index.html', title=title, categories=category, all_pitches=pitches)


@main.route('/user/<uname>')
def profile(uname):

    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.update_profile', id_user=user.id, uname=user.username))
    title = 'Update Bio'
    return render_template('profile/update.html', title=title, form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname, id_user=user.id))


@main.route('/new/pitch', methods=['GET', 'POST'])
@login_required
def pitch():
    form = PitchForm()
    category = PitchCategory.query.filter_by(category=category).first()

    if form.validate_on_submit():
        content = form.content.data
        pitch = Pitch(content=content, category_id=category.id,
                      user_id=current_user.id)
        pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('comment.html', form=form, category=category)


@main.route('/new/comment/<int:pitch_id>')
@login_required
def new_comment(pitch_id):
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        comment = comment_form.comment.data

        comment = Comment(comment=comment)

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for('main.comment'))

    comment = Comment.get_comment()
    title = 'comment'
    return render_template('pitch.html', title=title, pitch_form=pitch, pitches=pitches, comment=comment)


@main.route('/category/<int:id>')
def category(id):
    category = PitchCategory.query.get(id)

    pitches = Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)


@main.route('/add/category', methods=['GET', 'POST'])
@login_required
def add_category():

    form = CategoryForm()

    if form.validate_on_submit():
        category = form.category.data
        add_category = PitchCategory(category=category)
        add_category.save_category()

        return redirect(url_for('.index'))

    title = 'category'
    return render_template('add_category.html', category_form=form, title=title)


@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):

    add_category = PitchCategory.get_categories()
    pitches = Pitch.query.get(id)
    pitches = Pitch.query.filter_by(id=id).all()
    comment = Comment.get_comments(id)
    count_likes = Like.query.filter_by(pitches_id=id,)
    count_dislikes = Dislike.query.filter_by(pitches_id=id,)
    return render_template('view-pitch.html', pitches=pitches, comment=comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes), category_id=id, categories=category)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):

    form = CommentForm()
    title = 'comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        comment = form.comment.data
        add_comment = Comment(
            comment=comment, user_id=current_user.id, pitches_id=pitches.id)
        add_comment.save_comment()
        return redirect(url_for('.new_pitch', id=pitches.id))

    return render_template('comment.html', comment_form=form, title=title)


@main.route('/pitch/like/<int:pitch_id>/like')
@login_required
def like(pitch_id):
    '''
    route to view number of likes
    '''
    get_pitches = Like.get_votes(id)
    valid_string = f'{current_user.id}:{id}'

    for pitch in get_pitches:
        to_str = f'{pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch', id=id))
        else:
            continue

    like_pitch = Like(user=user, pitching_id=id)
    like_pitch.save_vote()

    return redirect(url_for('main.pitch', id=id))


@main.route('/pitch/dislike/<int:pitch_id>//dislike')
@login_required
def dislike(pitch_id):
    '''
    route to view number of dislikes
    '''
    get_pitches = Dislike.get_downvotes(id)
    valid_string = f'{current_user.id}:{id}'
    for get_pitch in get_pitches:
        to_str = f'{get_pitch}'
        print(valid_string+" "+to_str)
        if valid_string == to_str:
            return redirect(url_for('main.pitch', id=id))
        else:
            continue
    dislike_pitch = Like(user=user, pitching_id=id)
    dislike_pitch.save_vote()
    return redirect(url_for('main.pitch', id=id))
