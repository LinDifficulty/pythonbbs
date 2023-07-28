from flask import session, g, render_template
from models.user import UserModel

# 将user设置为全局变量
def bbs_before_request():
    if "user_id" in session:
       user_id = session.get("user_id")
       try:
           user = UserModel.query.get(user_id)
           setattr(g, "user", user)
       except:
           pass

# 错误提示
def bbs_404_error(error):
    return render_template("errors/404.html"), 404


def bbs_401_error(error):
    return render_template("errors/401.html"), 401


def bbs_500_error(error):
    return render_template("errors/500.html"), 500