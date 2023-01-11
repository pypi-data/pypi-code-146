# To scrape data from HMTV website.
def scrape_data():
    choice = input("enter ur chooice :")
    pagenum = int(input("enter page number :"))
    try:
        import pandas as pd
        import requests
        from bs4 import BeautifulSoup
        def _subFun():
            for pk in range(1,pagenum+1):
                    url = f"https://www.hmtvlive.com/search?search={choice}&search_type=all&page={pk}"
                    req = requests.get(url)
                    print(req,"Page :",pk)
                    soup = BeautifulSoup(req.content,"html.parser")
                    # print(soup.prettify())
                    for a in soup.findAll("div",{"class":"row two-colum-listing bigger-image"}):
                        for b in a.findAll("div",{"class":"col-md-8 col-8"}):
                            for c in b.findAll("a"):
                                print(c.text.strip()) 
                                print("https://www.hmtvlive.com"+c.get("href"))
                                aurl = "https://www.hmtvlive.com"+c.get("href")
                                req1 = requests.get(aurl)
                                soup1 = BeautifulSoup(req1.content,"html.parser")
                                for d in soup1.findAll("div",{"class":"image-wrap"}):
                                        for e in d.findAll("img",{"data-class":"h-custom-image"}):
                                            print(e['src'])
                                            print(e.get("alt"))
                                data = ""
                                for f in soup1.findAll("p"):
                                    data+=f.text.strip()
                                print(data)
                            print()
        if len(choice.split()) == 1:
            _subFun()    
        else:
            choice = "+".join(choice.split())
            _subFun()
    except Exception as e:
        raise e

# scrape_data(choice,pagenum)