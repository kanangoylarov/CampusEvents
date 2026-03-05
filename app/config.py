import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'fallback-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_TOKEN_EXPIRES', 604800)))  # 7 days
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = False  # Set to True in production with HTTPS
    JWT_COOKIE_HTTPONLY = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'sqlite:///database.db'
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
