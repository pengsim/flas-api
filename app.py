import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from flask import Flask , jsonify , send_from_directory , request
from flask_cors import CORS
import pymysql
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
CORS(app)
# connect database 
app.config['MYSQL_HOST'] = 'api-hghvb024-1c5a.l.aivencloud.com'
app.config['MYSQL_PORT'] = 17980
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_tqMV-vPcTQsi9mgA6vv'
app.config['MYSQL_DB'] = 'defaultdb'
cloudinary.config( 
    cloud_name = "dhgfrrblt", 
    api_key = "679837445747363", 
    api_secret = "eSkdWfhfvbgzXqsPD7RwmMMT98Y", 
    secure=True
)
# get database 
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
# upload image
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    connection = get_database()
    cur = connection.cursor()
    cur.execute('SELECT * FROM users')
    store_data = cur.fetchall()
    return jsonify(store_data)

@app.route('/add',methods=['POST'])
def add():
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')
    image_file = request.files.get('image')
    if image_file and image_file.filename != '':
        filename = secure_filename(image_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        image_file.save(filepath)
    else:
        filename = ''
    connection = get_database()
    cur = connection.cursor()
    cur.execute('INSERT INTO users (name, gender, email , image) VALUES (%s,%s,%s,%s)',\
                (name, gender, email, filename))
    cur.connection.commit()
    return jsonify({'message':'success'})
if __name__ == '__main__':
    app.run(host='0.0.0.0' , port= 5000)
