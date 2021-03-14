from views import init_app
from flask_cors import *  # 解决跨域问题

if __name__ == '__main__':
    app = init_app()
    # 跨域问题解决方法
    CORS(app, supports_credentials=True)
    app.run()
