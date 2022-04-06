from os import error
from flask import jsonify, request as req
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from pymongo import MongoClient
import json
from bson import json_util
from bson import ObjectId
#from werkzeug.security import generate_password_hash, check_password_hash
con = MongoClient("mongodb+srv://user:normi@cluster0.kpekd.mongodb.net/NormiPayrollDTR?retryWrites=true&w=majority")
db = con["NormiPayrollDTR"]

#collection validator
validCol = ["employeesInfo", "designation", "dtr", "payroll", "requests"]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class Data(Resource):

    def get(self, col, query):
        try:
            if validCol.count(col) > 0:
                qry = json.loads(query)
                print(qry)
                reqData = db[col].find(qry)
                if reqData:
                    data = []
                    for el in reqData:
                        el["_id"] = str(el["_id"]).replace("ObjectId('","").replace("')","")
                        data.append(el)
                           
                    print(data)
                    data
                    return {"data": data }, 200
                else:
                    return {"data": None, "errMsg": "Cannot find query on '"+ col + "' database!" }, 205
            else:
                return {"data": None, "errMsg":"'"+ col +"' is not in the database!" }, 404
        except error:
            print(error)
            return {"data": None }, 500
    
    def post(self, col, query):
        try:
            qry = json.loads(query)
            body = req.get_json(force=True)
            print(col)
            print(body)
            print(validCol.count(col) > 0)
            if validCol.count(col) > 0:
                db[col].insert_one(body)
                return {"inserted": True}, 200
            else:
                return {"inserted": False, "errMsg":"'"+ col +"' is not in the database!" }, 404
        except:
            return {"inserted": False}, 500

    def put(self, col, query):
        try:
            qry = json.loads(query)
            body = req.get_json(force=True)
            print(body)
            if validCol.count(col) > 0:
                print('was here')
                exist = db[col].update_one(qry ,{"$set": body })
                if exist:
                    return {"updated": True}, 200
                else:
                    return {"updated": False, "errMsg": body["fullName"]+" is already exists in '"+ col +"' database!"}, 205
            else:
                print('was here4')
                return {"updated": False, "errMsg":"'"+ col +"' is not in the database!" }, 404
        except:
            return {"updated": False}, 500

    def delete(self, col, query):
        return { "response" : "unavailable" }

