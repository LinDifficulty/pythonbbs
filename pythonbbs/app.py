from flask import Flask, url_for
import config
from exts import db, mail, cache
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from flask_migrate import Migrate
from models import user, post
import commands
from flask_wtf import CSRFProtect
import hooks

app = Flask(__name__)

# 加载配置文件
app.config.from_object(config.DevelopmentConfig)

# 映射ORM模型
migrate = Migrate(app, db)

# 初始化第三方插件
db.init_app(app)
mail.init_app(app)
cache.init_app(app)

# 注册蓝图
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(user_bp)

# 添加命令
app.cli.command("create-permission")(commands.create_permission)
app.cli.command("create-role")(commands.create_role)
app.cli.command("create-admin")(commands.create_admin)
app.cli.command("create-board")(commands.create_board)
app.cli.command("create-test-post")(commands.create_test_post)

# CSRF保护
CSRFProtect(app)

# 添加钩子函数
app.before_request(hooks.bbs_before_request)
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

