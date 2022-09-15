from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

from urllib import response
from flask import Flask, request
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os


#inisiasi object flask
app= Flask(__name__)

#inisiasi project flask restful
api=Api(app)

#inisiasi CORS
CORS(app)

#inisiasi object flask sqlalchemy
db = SQLAlchemy(app)

#konfigurasi database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

#membuat database model
class ModelDatabase(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    #method utk menyimpan data
    def save(self):
        try: 
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

#creating database
db.create_all()


#inisiasi variabel kosong berupa dictionary
identitas={} #variabel global, json

#membuat class resource, punya method get sama post
class ContohResource(Resource):

    #method
    def get(self):

        #menampilkan data dari database sql 
        query = ModelDatabase.query.all()

        #iterasi data pada modelDatabase memakai list comprehension
        output = [
            {
                "id":data.id,
                "nama":data.nama,
                "umur":data.umur,
                "alamat":data.alamat
            }
            for data in query
                 ]
        
        response = {
            "code":200,
            "msg":"query sukses",
            "data":output

        }

        return response,200

    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]

        #dalam json ada key sama value, keynya yg dalam kurung kotak valuenya yg habis tanda sama dengan
        #identitas["nama"] = nama
        #identitas["umur"] = umur
 
        #masukkan data ke dalam database model
        model = ModelDatabase(nama=dataNama,umur=dataUmur,alamat=dataAlamat)
        model.save()
        response = {"msg":"data berhasil dimasukkan", "code":200,}
        return response,200

    def delete(self):

        #hapus semua data
        query = ModelDatabase.query.all()

        #looping utk mengambil semua data
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "msg":"hapus semua data berhasil",
            "code": 200
        }
        return response

#class update database
class UpdateDatabase(Resource):

    #method
    def put(self,id):

        #pilih data yang ingin diedit berdasarkan id
        query = ModelDatabase.query.get(id)

        #form untuk edit
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]
        
        #replace nilai yg ada di kolom
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat
        db.session.commit()

        response = {
            "msg":"edit data berhasil",
            "code": 200
        }
        return response



    def delete(self,id):   

         #pilih data yang ingin di hapus berdasarkan id
        queryData = ModelDatabase.query.get(id)
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg":"hapus data berhasil",
            "code": 200
        }
        return response

#setup resource
#urlnya ada di /
api.add_resource(ContohResource, "/database", methods=["GET","POST","DELETE"])
api.add_resource(UpdateDatabase, "/database/<id>", methods=["PUT","DELETE"])


