import os
from web.config import DevelopmentConfig, ProductionConfig
from web import create_app

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)
