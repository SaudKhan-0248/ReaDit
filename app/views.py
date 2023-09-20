from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from .models import Post, User, Vote, Comment
from .utils import check_logout_status

views = Blueprint('views', __name__)


@views.route('/home', methods=['GET'])
def home():
    page = request.args.get('page')
    limit = 10
    offset = (int(page) * limit) - limit

    from . import session

    query = select(Post).order_by(Post.id.desc()).offset(offset).limit(limit)
    record = session.execute(query).all()

    posts = list()

    for post in record:
        posts.append({"id": post[0].id, "title": post[0].title, "content": post[0].content,
                      "posted on": post[0].date, "posted by": post[0].user.username})

    return jsonify(posts), 200


@views.route('/post/create', methods=['POST'])
@jwt_required()
def create_post():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    user_id = get_jwt_identity()
    post_title = request.json.get('title')
    post_content = request.json.get('content')

    post = Post(title=post_title, content=post_content, owner_id=user_id)

    from . import session

    try:
        session.add(post)
        session.commit()

    except IntegrityError:
        session.rollback()
        abort(401, "Unauthorized to perform requested action")

    return jsonify({"message": "Post Created Successfuly!"}), 200


@views.route('/post/update', methods=['PUT'])
@jwt_required()
def update_post():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    user_id = get_jwt_identity()
    pid = request.args.get('pid')
    title = request.json.get('title')
    content = request.json.get('content')

    from . import session

    query = select(Post).where(Post.id == pid)
    record = session.execute(query).first()

    if not record:
        abort(404, "Error: No such post exists!")

    post = record[0]

    if user_id != post.owner_id:
        abort(403, "message: Not authorized to perform requested action")

    post.title = title
    post.content = content
    post.date = datetime.today()
    session.commit()

    return jsonify({"message": "Post updated successfully"}), 200


@views.route('/post/delete', methods=['DELETE'])
@jwt_required()
def delete_post():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    user_id = get_jwt_identity()
    pid = request.args.get('pid')

    from .import session

    query = select(Post).where(Post.id == pid)
    record = session.execute(query).first()

    if not record:
        abort(404, "Error: No such post exists!")

    post = record[0]

    if user_id != post.owner_id:
        abort(403, "message: Not authorized to perform requested action")

    session.delete(post)
    session.commit()

    return jsonify({"message": "Post deleted Successfuly!"}), 200


@views.route('/post/votes')
def get_votes_on_post():
    post_id = request.args.get('post_id')

    from . import session

    post_exist = session.query(Post).filter(Post.id == post_id).exists()

    if not session.query(post_exist).scalar():
        abort(404, "No such Post Exists")

    upvotes = session.query(Vote).filter(
        and_(Vote.post_id == post_id, Vote.value == "1")).count()
    downvotes = session.query(Vote).filter(
        and_(Vote.post_id == post_id, Vote.value == "-1")).count()

    return jsonify({"UpVotes": f"{upvotes}", "DownVotes": f"{downvotes}"})


@views.route('/post/comments', methods=['GET'])
def get_comments_on_post():
    page = request.args.get('page')
    limit = 30
    offset = (int(page) * limit) - limit
    post_id = request.args.get('post_id')

    from . import session

    post_exist = session.query(Post).filter(Post.id == post_id).exists()

    if not session.query(post_exist).scalar():
        abort(404, "No such Post Exists")

    query = select(Comment).where(Comment.post_id ==
                                  post_id).order_by(Comment.id.desc()).offset(offset).limit(limit)
    record = session.execute(query).all()

    comments = list()

    for comment in record:
        comments.append(
            {"id": comment[0].id, "posted by": comment[0].user.username, "content": comment[0].content})

    return jsonify(comments), 200


@views.route('/vote', methods=['GET'])
@jwt_required()
def vote():
    user_id = get_jwt_identity()
    post_id = request.args.get('post_id')
    value = request.args.get('value')

    from . import session

    post_exist = session.query(Post).filter(Post.id == post_id).exists()

    if not session.query(post_exist).scalar():
        abort(404, "No such Post Exists")

    vote = Vote(user_id=user_id, post_id=post_id, value=value)

    try:
        session.add(vote)
        session.commit()

    except IntegrityError:
        session.rollback()
        abort(409, "Unable to perform action!")

    return jsonify({"message": "Successfully voted on post"}), 200


@views.route('/vote/delete', methods=['DELETE'])
@jwt_required()
def delete_vote():
    user_id = get_jwt_identity()
    post_id = request.args.get('post_id')

    from . import session

    query = select(Vote).where(
        and_(Vote.user_id == user_id, Vote.post_id == post_id))
    record = session.execute(query).first()

    if not record:
        abort(404, 'Record Not Found!')

    vote = record[0]

    session.delete(vote)
    session.commit()

    return jsonify({"message": "Vote removed Successfully"}), 200


@views.route('/comment/create', methods=['POST'])
@jwt_required()
def post_comment():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    post_id = request.args.get('post_id')
    user_id = get_jwt_identity()
    content = request.json.get('content')

    from . import session

    post_exist = session.query(Post).filter(Post.id == post_id).exists()

    if not session.query(post_exist).scalar():
        abort(404, "No such Post Exists")

    comment = Comment(content=content, post_id=post_id, user_id=user_id)

    try:
        session.add(comment)
        session.commit()
    except IntegrityError:
        session.rollback()
        abort(409, "Unable to perform action. Please try again")

    return jsonify({"message": "Posted the comment Successfully"}), 200


@views.route('/comment/delete', methods=['DELETE'])
@jwt_required()
def delete_comment():
    cmnt_id = request.args.get('comment_id')
    user_id = get_jwt_identity()

    from . import session

    query = select(Comment).where(Comment.id == cmnt_id)
    record = session.execute(query).first()

    if not record:
        abort(404, 'Record Not Found!')

    comment = record[0]

    if user_id != comment.user_id:
        abort(401, 'Unauthorized to perform action!')

    session.delete(comment)
    session.commit()

    return jsonify({"message": "Comment deleted Successfuly!"}), 200


@views.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    user_id = get_jwt_identity()

    from . import session

    query = select(User).where(User.id == user_id)
    record = session.execute(query).first()

    if not record:
        abort(404, "Error: Record Not Found!")

    user = record[0]

    posts = list()

    for post in user.posts:
        posts.append({"id": post.id, "title": post.title, "content": post.content,
                      "posted on": post.date})

    return jsonify({"user_id": user.id, "username": user.username, "email": user.email,
                    "age": user.age, "gender": user.gender, "posts": posts})


@views.route('/account/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    if check_logout_status():
        abort(401, "message: Unauthorized to perform requested action")

    user_id = get_jwt_identity()

    from . import session

    query = select(User).where(User.id == user_id)
    record = session.execute(query).first()

    if not record:
        abort(404, "Error: User Not Found!")

    user = record[0]

    session.delete(user)
    session.commit()

    return jsonify({"message": "Account deleted successfull"}), 200
