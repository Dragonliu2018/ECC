# -*- coding = utf-8 -*-
# @Time : 2020/11/24 22:11
# @Author : Dragon Liu
# @File : app.py
# @Software : PyCharm
from flask import Flask,render_template,request,redirect,url_for,session,g,flash,\
    current_app,jsonify
import json, random
# import numpy as np
# import ecc#测试ecc
import SM2#SM2
from Elgamal import ELGAMAL#Elgamal
import DH#DH
# import string

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/index')
def home1():
    # return render_template("index.html")
    return home()

#SM2界面
@app.route('/sm2',methods=['GET'])
def sm2():
    # if request.method == 'GET':
    return render_template('sm2.html')

#SM2数据交互
@app.route('/sm2-data',methods=['GET','POST'])
def sm2_data():
    op_type = request.form['type']
    if op_type == 'encode':
        public_key = request.form['public_key'] 
        private_key = request.form['private_key'] 
        message  = request.form['message'].encode('utf-8')
        enc_data = SM2.encrypt(message)
        # print(enc_data)
        # print(type(enc_data))
        ciphertext = enc_data.hex()
        return jsonify({"ciphertext1": ciphertext}) 
    elif op_type == 'decode':
        public_key = request.form['public_key'] 
        private_key = request.form['private_key'] 
        ciphertext  = request.form['ciphertext1']
        enc_data = bytes.fromhex(ciphertext)
        dec_data = SM2.decrypt(enc_data)
        message = dec_data.decode('utf-8')
        return jsonify({"message": message}) 

#Elgamal界面
@app.route('/elgamal')
def elgamal():
    return render_template("elgamal.html")

#elgamal数据交互
@app.route('/elgamal-data',methods=['GET','POST'])
def elgamal_data():    
    op_type = request.form['type']
    if op_type == 'genkey':#仅仅随机生成int范围内整数
        # p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
        index = random.sample(range(2,0xffffffff),1)[0]
        print(index)
        # while obj_elg.egcd(index, p-1) != 1:
        #     index = random.sample(range(2,0xffffffff),1)[0]
        return jsonify({"par_d": index})  
    elif op_type == 'encode':
        par_d = eval( request.form['par_d'] ) 
        message  = request.form['message']
        obj_elg = ELGAMAL(message, par_d)
        ciphertext = obj_elg.encrypt(message, par_d)
        return jsonify({"ciphertext1": ciphertext}) 
    elif op_type == 'decode':
        par_d = eval( request.form['par_d'] ) 
        ciphertext  = request.form['ciphertext1']
        obj_elg = ELGAMAL(ciphertext, par_d)
        message = obj_elg.decrypt(ciphertext, par_d)
        # print(len(message))
        # message = message.rstrip("")
        # print(len(message))
        # print(ciphertext)
        return jsonify({"message": message}) 

#DH界面
@app.route('/dh')
def dh():
    return render_template("dh.html")

#DH数据交互
@app.route('/dh-data',methods=['GET','POST'])
def dh_data():    
    op_type = request.form['type']
    if op_type == 'genkey':
        keys = DH.genkey()
        keys_dict = {
            "private_keyA": hex(keys[0]),
            "public_keyA": (hex(keys[1][0]), hex(keys[1][1])),
            "private_keyB": hex(keys[2]),
            "public_keyB": (hex(keys[3][0]), hex(keys[3][1])),
            "keyAB": (hex(keys[4][0]), hex(keys[4][1])),
        }
        return jsonify(keys_dict)
    elif op_type == 'test':
        exchange  = request.form['keyAB']
        messageA  = request.form['messageA']
        keyAB = exchange.split(',')#分割
        par_key = keyAB[0][2:].encode('utf-8')#0x字符串转对应hex
        # print(par_key)
        # print(type(par_key))
        ans_list = DH.test(messageA, par_key)
        # print(ans_list)
        # print(type(ans_list))
        message_dict = {
            "ciphertextA":ans_list[0], 
            "messageB":ans_list[1], 
        }
        return jsonify(message_dict) 

@app.route('/team')
def team():
    return render_template("team.html")


@app.route('/test')
def test():
    return render_template("test.html")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8003, debug=True)