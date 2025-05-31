import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)

# Cloudinary config
cloudinary.config( 
    cloud_name = "dhgfrrblt", 
    api_key = "679837445747363", 
    api_secret = "eSkdWfhfvbgzXqsPD7RwmMMT98Y", 
    secure=True
)

# Database config
app.config['MYSQL_HOST'] = 'api-hghvb024-1c5a.l.aivencloud.com'
app.config['MYSQL_PORT'] = 17980
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_tqMV-vPcTQsi9mgA6vv'
app.config['MYSQL_DB'] = 'defaultdb'

def get_database():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        port=app.config['MYSQL_PORT'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        ssl={'ssl-mode': 'REQUIRED'},
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    connection = get_database()
    cur = connection.cursor()
    cur.execute('SELECT * FROM users')
    store_data = cur.fetchall()
    return jsonify(store_data)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')
    image_file = request.files.get('image')

    image_url = ''
    if image_file and image_file.filename != '':
        # ✅ Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(image_file)
        image_url = upload_result.get('secure_url')

    connection = get_database()
    cur = connection.cursor()
    cur.execute('INSERT INTO users (name, gender, email, image) VALUES (%s, %s, %s, %s)',
                (name, gender, email, image_url))
    connection.commit()
    return jsonify({'message': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
