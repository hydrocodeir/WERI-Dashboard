import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from app import app

if __name__ == '__main__':
    
    from livereload import Server
    server = Server(app.wsgi_app)
    server.serve(
        host = "127.0.0.1",
        port=5000
    )
    
    # app.run(
    #     host="127.0.0.1",
    #     port=5000
    # )
