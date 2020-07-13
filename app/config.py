env = 'dev'
if env == 'dev':
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/StoryTime'

else:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://wzyzzpqrftcmap:13fad4cc04b93900680a000b605c91b2c6f40eef0878081fd8682ae6994f8888@ec2-52-72-221-20.compute-1.amazonaws.com:5432/d78iuiim587e63'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
