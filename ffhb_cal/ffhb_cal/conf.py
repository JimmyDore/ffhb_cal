# ---- CONF FTP
HOST_FTP = '<host_ftp>'
USERNAME_FTP = '<user_ftp>'
PASSWORD_FTP = '<pw_ftp>'

# ---- CONF DB

SYSTEM_DB = 'PostgreSQL'             # 'MySQL'
DATABASE_NAME = 'ffhb_cal_db'
USERNAME_DB = '<username_db>'        # '<username_db>'
PASSWORD_DB = '<password_db>'        # '<password_db>'
HOST_DB = 'localhost'                # '127.0.0.1'
PORT_DB = '5432'                     # '3306'

# ---- CONF DEBUG
DEBUG = True

# DON'T TOUCH THIS
# ----------------------------------------------------------------
# Custom dictionnary
DICT_DB_ENGINE: {
    'PostgreSQL': 'django.db.backends.postgresql_psycopg2',
    'MySQL': 'django.db.backends.mysql',
    'SQLite3': 'django.db.backends.sqlite3'
}
# ----------------------------------------------------------------
