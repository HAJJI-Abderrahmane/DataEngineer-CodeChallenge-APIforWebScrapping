from scrapping import *
from mongodb import *
import json
from flask import Flask,request,jsonify,Response

from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


#####Initialize the API by storing the first 10 pages of The guardian articles
mongodb=Mongodb()
data=scrapepages(1,10)
for i in data:
	if(len(list(mongodb.find_item({"Headline":i["Headline"]})))==0):#Checks if Article already exists in the collection or not
		mongodb.insert_item(i)


def updateDB():
	data=scrapepages(1,1)
	for i in data:
		if(len(list(mongodb.find_item({"Headline":i["Headline"]})))==0):#Checks if Article already exists in the collection or not
			mongodb.insert_item(i)
	print("DB Updated at : "+str(datetime.now()))

scheduler = BackgroundScheduler()
scheduler.add_job(func=updateDB, trigger="interval", seconds=3600)#Updated the DB every 1 hours
scheduler.start()


@app.route('/search/headline', methods=['POST'])
def api_model():
	headline = request.form.get('Headline')

	Results=list(mongodb.find_item({ "Headline": { "$regex": "^.*"+str(headline)+".*$" } }))
	for idx,i in enumerate(Results):
		Results[idx].pop("_id")
	print(Results)
	return jsonify({'Results':Results})


atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=False, threaded=False,host="0.0.0.0",port=3000)


