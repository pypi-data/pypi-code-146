from requests import get, post

class SetClines:
	web = {
		"app_name"    : "Main",
		"app_version" : "4.0.7",
		"platform"    : "Web",
		"package"     : "web.rubika.ir",
		"lang_code"   : "fa"
	}

	android = {
	    "app_name":"Main",
		"app_version":"2.9.5",
		"platform":"Android",
		"package":"ir.resaneh1.iptv",
		"lang_code":"fa"
	}


class Server:
	matnadress = []
	m = get("https://getdcmess.iranlms.ir/").json()["data"]["API"]
	for k,v in m.items(): 
	      matnadress.append(v)
	      
	      


	
	filesadress = []
	m = get("https://getdcmess.iranlms.ir/").json()["data"]["API"]
	for k,v in m.items():
	      filesadress.append(v)
	      
	socket = []
	sock = get("https://getdcmess.iranlms.ir/").json()["data"]["socket"]
	
	for k,v in sock.items():
	      socket.append(v)
	      
	      
	      


