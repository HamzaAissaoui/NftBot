import os
import requests

class Settings:
    @classmethod
    def get_setting(cls, name, defaultValue):
        val = os.environ.get(name)
        if val is None:
            val = defaultValue
        return val

    @classmethod
    def get_platform_name(cls):
        return cls.get_setting("PLATFORM_NAME", "Android")

    @classmethod
    def get_device_name(cls):
        return cls.get_setting("DEVICE_NAME", "Android Emulator")

    @classmethod
    def get_app_package(cls):
        return cls.get_setting("APP_PACKAGE", "com.test.mobile")

    @classmethod
    def get_server_url(cls):
        return cls.get_setting("SERVER_URL", "http://localhost:4723/wd/hub")

    @classmethod
    def get_actions_url(cls):
        return cls.get_setting("SERVER_URL", "http://localhost:8226/wd/hub")
    
    @classmethod
    def session_base_uri(cls, session_id):
        return cls.get_server_url() +'/session/%s' % session_id


    @classmethod
    def get_celery_broker(cls, session_id):
        return cls.get_setting("CELERY_BROKER", "amqp://guest:guest@localhost:5672//")

    @classmethod
    def get_db_name(cls, session_id):
        return cls.get_setting("DB_NAME", "postgres")

    @classmethod
    def get_db_user(cls, session_id):
        return cls.get_setting("DB_USER", "postgres")


    @classmethod
    def get_db_password(cls, session_id):
        return cls.get_setting("DB_PASS", "postgres")

    @classmethod
    def get_db_host(cls, session_id):
        return cls.get_setting("DB_HOST", "localhost")

    @classmethod
    def get_db_port(cls, session_id):
        return cls.get_setting("DB_PORT", "5432")

    @classmethod
    def get_db_ORDBMS(cls, session_id):
        return cls.get_setting("ORDBMS", "postgresql")
    

    @classmethod
    def get_db_interpreter(cls, session_id):
        return cls.get_setting("DB_INTERPRETER", "psycopg2")