from bs4 import BeautifulSoup as BS
import requests


"""Getting article links from theguardian page number
   Some of the headers wont be accessible inside of the links, so we get all of the headers in the page"""
def getlinksfrompage(pagenumber):

	theGuardianURL="https://www.theguardian.com/world/all?page="+str(pagenumber)
	page = requests.get(theGuardianURL) #Getting the html text

	soup = BS(page.text, 'html.parser')

	myDivs = soup.find_all("div", class_="fc-item__content")
	links=[]
	headers=[]
	for i in myDivs:
		span=i.find("a")
		links.append(span["href"])
		header=span.text
		if(header):
			headers.append(span.text.strip('\n'))
	return links,headers

######Getting the needed attributes from the link
def getattr(link):
	page = requests.get(link)			#Getting the html text
	soup = BS(page.text, 'html.parser')
	######Getting authors
	authorsP = soup.find("p", class_="byline")
	authors=[]
	if(authorsP):
		authspans=authorsP.find_all("span",{"itemprop":"name"})
		for i in authspans:
			authors.append(i.text)
	#######Getting standfirst
	standfirstDIV = soup.find("div", class_="tonal__standfirst")
	standfirst=""
	if(standfirstDIV):
		standfirstp=standfirstDIV.find("p")
		if(standfirstp):
			standfirst=standfirstp.text
	#######Getting datePublished
	datepublishedTIME = soup.find("time",{"itemprop":"datePublished"})
	datepublished=""
	if(datepublishedTIME):
		datepublished=datepublishedTIME["datetime"]
	return authors,standfirst,datepublished

def scrapepages(startpage,endpage):
	scrapeddata=[]
	for i in range(startpage,endpage+1):
		print("Page : "+str(i))
		links,headers=getlinksfrompage(i)
		dicte={}
		for idx,link in enumerate(links):
			# print(link)
			authors,standfirst,datepublished=getattr(link)
			dicte["Headline"]=headers[idx]
			dicte["Author"]=authors
			dicte["Standfirst"]=standfirst
			dicte["datepublished"]=datepublished
			dicte["url"]=link
			# print(d)

			scrapeddata.append(dicte.copy())
			# yield dicte
	return scrapeddata

