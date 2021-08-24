
import requests
url = 'http://52.158.42.152:3333/search/headline'
data={"Headline":"vaccine"}

x = requests.post(url,data=data)

print(x.text)

