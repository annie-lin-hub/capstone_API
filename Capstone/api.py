import pymysql, json, configparser, os, datetime, time, shutil, base64
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS, cross_origin
from flask_api import status
from subfunction import getSize
import hashlib
import datetime

path = os.path.abspath('.')
cfgpath = path.split('Capstone')[0] + 'Capstone/config.ini'

config = configparser.ConfigParser()
config.read(cfgpath)

app = Flask(__name__)

@app.route('/Store', methods = ['POST'])
@cross_origin()
def object_store():
    mysql = pymysql.connect(user = config['MYSQL']["user"], password = config['MYSQL']["password"], port = int(config["MYSQL"]["port"]), host = config['MYSQL']["host"])
    cur = mysql.cursor()
    data_json = {}
    
    Student_id = request.form.get('Student_id')
    
    check_account = cur.execute("SELECT * FROM Capstone.Information WHERE Student_id = '%s'"%(Student_id))
    print(check_account)
    if check_account == 0:
        Student_name = request.form.get('Student_name')
        Email = request.form.get('Email')
        Department = request.form.get('Department')
    else:
        return jsonify({"error": 100, "msg": "Account already exist"}), status.HTTP_400_BAD_REQUEST
   
    if(not request.files['jpg']):
        return jsonify({"error" : "request jpg file", "code" : "file_01"}), status.HTTP_400_BAD_REQUEST

    File_jpg = request.files['jpg'] 
    File_jpg_name = File_jpg.filename.rsplit('.',1)[1]
    if(File_jpg_name != 'jpg'):
        return jsonify({"error": 1001, "msg": "Not jpg file"}), status.HTTP_400_BAD_REQUEST

    file_path = os.path.join(config['PATH']['file_path'], Student_id)

    if not os.path.isdir(file_path):
        os.makedirs(file_path)

    Picture_path = os.path.join(file_path, Student_id + '.jpg')

    File_jpg.save(Picture_path)


    INSERT = '''INSERT INTO Capstone.Information(
                                                Student_id,
                                                Student_name,
                                                Email,
                                                Department,
                                                Picture_path
                                                )VALUES(%s, %s, %s, %s, %s);'''

    insert_data = (
        Student_id,
        Student_name,
        Email,
        Department,
        Picture_path
        )

    cur.execute(INSERT, insert_data)
    mysql.commit()

    data_json['Log'] = "Upload Success"

    return json.dumps(data_json), status.HTTP_200_OK

@app.route('/Get', methods = ['GET'])
@cross_origin()
def object_information():
    mysql = pymysql.connect(user = config['MYSQL']["user"], password = config['MYSQL']["password"], port = int(config["MYSQL"]["port"]), host = config['MYSQL']["host"])
    cur = mysql.cursor()
    data_json = {}
    Student_id = request.args.get('Student_id')

    cur.execute('''SELECT * FROM Capstone.Information WHERE Student_id = '%s';''' %Student_id)
    data = cur.fetchall()
    if(len(data) == 0):
        data_json["Log"] = "Student ID is not exist!"
        return json.dumps(data_json), status.HTTP_400_BAD_REQUEST
    else: 
        Picture_path = data[0][4]

        file_jpg= open(Picture_path, 'rb').read()
        file_jpg_64 = base64.b64encode(file_jpg)
        
        data_json['Student_id'] = Student_id
        data_json['Student_name'] = data[0][1]
        data_json['Email'] = data[0][2]
        data_json['Department'] = data[0][3]
        data_json['Picture'] = file_jpg_64.decode('UTF-8')

        return json.dumps(data_json), status.HTTP_200_OK



app.run(host = config['FLASK']['host'], port = int(config['FLASK']['port']), debug=True )

#if __name__ == '__main__':
#   app.run(host='0.0.0.0',port=5053,debug=True)
