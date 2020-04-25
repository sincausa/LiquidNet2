from config import DevelopmentConfig

from api.app import create_app

app = create_app(DevelopmentConfig)  # pylint: disable=invalid-name

if __name__ == '__main__':
    app.run()