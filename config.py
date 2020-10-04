from app.controller.randomGenerator import generate_key


class Config(object):
    DEBUG = True
    SECRET_KEY = generate_key(20)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/StoryTime'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    pass

# env = 'dev'
# if env == 'dev':
#  SQLALCHEMY_DATABASE_URI = 'sqlite:///test'

# else:
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = 'postgres://wzyzzpqrftcmap:13fad4cc04b93900680a000b605c91b2c6f40eef0878081fd8682ae6994f8888@ec2-52-72-221-20.compute-1.amazonaws.com:5432/d78iuiim587e63'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
