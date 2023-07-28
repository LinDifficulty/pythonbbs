from flask import Blueprint, request, render_template, g, redirect, flash
from models.post import BoardModel, PostModel
from decorators import login_required
from forms.post import PublicPostForm
from exts import db
from flask_paginate import current_app, Pagination

bp = Blueprint('front', __name__, url_prefix='')


@bp.route("/")
def index():
    boards = BoardModel.query.all()
    # 获取页码参数
    page = request.args.get("page", type=int, default=1)

    # 获取板块参数
    board_id = request.args.get("board_id", type=int, default=0)

    # 获取搜索关键字
    q = request.args.get("q")

    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get("PER_PAGE_COUNT")
    # 当前page下的结束位置
    end = start + current_app.config.get("PER_PAGE_COUNT")
    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())

    # 过滤帖子
    if board_id:
        query_obj = query_obj.filter_by(board_id=board_id)
    if q:
        query_obj = query_obj.filter(PostModel.title.contains(q))

    # 总共有多少帖子
    total = query_obj.count()

    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)

    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total,
                            outer_window=0, inner_window=2, alignment="center")

    context = {
        "posts": posts,
        "boards": boards,
        "pagination": pagination,
        "current_board": board_id
    }
    return render_template("front/index.html", **context)


# @bp.route("/search")
# def search():
#     q = request.args.get("q")
#     posts = PostModel.query.filter(PostModel.title.contains(q)).all()
#     return render_template("front/index.html", posts=posts)

@bp.get("/post/detail/<int:post_id>")
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    post.read_count += 1
    db.session.commit()
    return render_template("front/post_detail.html", post=post)


@bp.route("/post/public", methods=['POST', 'GET'])
@login_required
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/public_post.html", boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            post = PostModel(title=title, content=content, board_id=board_id, author=g.user)
            db.session.add(post)
            db.session.commit()
            return redirect("/")
        else:
            for message in form.messages:
                flash(message)
            boards = BoardModel.query.all()
            return render_template("front/public_post.html", boards=boards)
