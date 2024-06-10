from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def read_articles():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    result = list(db.memos.find({}, {'_id':0}).sort('likes', -1))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'memos':result })

@app.route('/memo/like', methods = ["POST"])
def like_memo():
   title_receive = request.form['title_give']
   memo = db.memos.find_one({'title' : title_receive})
   print(memo)
   
   new_likes = memo['likes'] + 1
   result = db.memos.update_one({'title' : title_receive}, {'$set': {'likes': new_likes}})
   
   if result.modified_count == 1:
        return jsonify({'result': 'success'})
   else:
        return jsonify({'result': 'failure'})

@app.route('/memo/delete', methods = ['POST'])
def delete_memo():
   title_receive = request.form['title_give']
   db.memos.delete_one({'title' : title_receive})
   
   return jsonify({'result' : 'success'})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def post_article():
		# 1. 클라이언트로부터 데이터를 받기
  title_receive = request.form['title_give']
  info_receive = request.form['info_give']
		# 2. meta tag를 스크래핑하기
  likes = 0
  likes = int(likes)
  
  article = {'title': title_receive, 'info': info_receive, 'likes' : likes}
  
		# 3. mongoDB에 데이터 넣기
  db.memos.insert_one(article)
  return jsonify({'result': 'success'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)