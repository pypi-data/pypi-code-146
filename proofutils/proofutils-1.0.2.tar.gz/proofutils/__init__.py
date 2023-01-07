import requests, random, base64, string, json, datetime, pytz, io
from typing import Union

def format_html(sender_username: str, sender_avatar: str, receiver_username: str, receiver_avatar: str, messages: list, nitro_type: int, nitro_code: str) -> str:
  """
  Formats HTML for the gifting proof, requires some variables.
  """
  tz = pytz.timezone('EST')
  now = datetime.datetime.now(tz).strftime('%-I:%M %p')
  before = datetime.datetime.now(tz) - datetime.timedelta(minutes=1)
  before = before.strftime('%-I:%M %p')

  if nitro_type == 1:
    splash = "https://cdn.discordapp.com/app-assets/521842831262875670/store/971526227435323423.webp?size=1024"
  elif nitro_type == 2:
    splash = "https://cdn.discordapp.com/app-assets/521842831262875670/store/971526227435323422.webp?size=1280"
  elif nitro_type == 3:
    splash = "https://cdn.discordapp.com/app-assets/521842831262875670/store/1039257000355307530.webp?size=1024"
  else:
    raise Exception('Invalid nitro type!')
  
  return f'''<!DOCTYPE html>
<html>
<head style="font-size: 100%; --saturation-factor: 1; --devtools-sidebar-width: 0px;">
</head>
<body>
<div id="capture">
<li id="chat-messages-1008466017527279626" class="messageListItem-ZZ7v6g" aria-setsize="-1"><div class="message-2CShn3 cozyMessage-1DWF9U groupStart-3Mlgv1 wrapper-30-Nkg cozy-VmLDNB zalgo-26OfGz {'mentioned-Tre-dv' if '[PING]' in messages[0] else ''}" role="article" data-list-item-id="chat-messages___chat-messages-1008466017527279626" tabindex="-1" aria-setsize="-1" aria-roledescription="Message" aria-labelledby="message-username-1008466017527279626 uid_1 message-content-1008466017527279626 uid_2 message-timestamp-1008466017527279626"><div class="contents-2MsGLg"><img src="{receiver_avatar}" aria-hidden="true" class="avatar-2e8lTP clickable-31pE3P receiver" alt=" "><h2 class="header-2jRmjb" aria-labelledby="message-username-1008466017527279626 message-timestamp-1008466017527279626"><span id="message-username-1008466017527279626" class="headerText-2z4IhQ"><span class="username-h_Y3Us desaturateUserColors-1O-G89 clickable-31pE3P receiver" aria-controls="popout_18939" aria-expanded="false" role="button" tabindex="0">{receiver_username}</span></span><span class="timestamp-p1Df1m timestampInline-_lS3aK"><time aria-label="Today at 4:03 PM" id="timestamp1" datetime="2022-08-14T20:03:54.971Z"><i class="separator-AebOhG" aria-hidden="true"> — </i>Today at {before}</time></span></h2><div id="question" class="markup-eYLPri messageContent-2t3eCI">{messages[0].replace('[PING]', f'<span class="mention wrapper-1ZcZW- mention interactive" aria-expanded="false" tabindex="0" role="button">@{receiver_username}</span>') if '[PING]' in messages[0] else messages[0]}</div></div><div id="message-accessories-1008466017527279626" class="container-2sjPya"></div><div class="buttonContainer-1502pf"><div class="buttons-3dF5Kd container-2gUZhU isHeader-2bbX-L" role="group" aria-label="Message Actions"><div class="wrapper-2vIMkT"><div class="button-3bklZh" aria-label="Add Reaction" aria-controls="popout_18980" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M12.2512 2.00309C12.1677 2.00104 12.084 2 12 2C6.477 2 2 6.477 2 12C2 17.522 6.477 22 12 22C17.523 22 22 17.522 22 12C22 11.916 21.999 11.8323 21.9969 11.7488C21.3586 11.9128 20.6895 12 20 12C15.5817 12 12 8.41828 12 4C12 3.31052 12.0872 2.6414 12.2512 2.00309ZM10 8C10 6.896 9.104 6 8 6C6.896 6 6 6.896 6 8C6 9.105 6.896 10 8 10C9.104 10 10 9.105 10 8ZM12 19C15.14 19 18 16.617 18 14V13H6V14C6 16.617 8.86 19 12 19Z"></path><path d="M21 3V0H19V3H16V5H19V8H21V5H24V3H21Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="Reply" role="button" tabindex="0"><svg class="icon-1zidb7" width="24" height="24" viewBox="0 0 24 24"><path d="M10 8.26667V4L3 11.4667L10 18.9333V14.56C15 14.56 18.5 16.2667 21 20C20 14.6667 17 9.33333 10 8.26667Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="More" aria-controls="popout_18981" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M7 12.001C7 10.8964 6.10457 10.001 5 10.001C3.89543 10.001 3 10.8964 3 12.001C3 13.1055 3.89543 14.001 5 14.001C6.10457 14.001 7 13.1055 7 12.001ZM14 12.001C14 10.8964 13.1046 10.001 12 10.001C10.8954 10.001 10 10.8964 10 12.001C10 13.1055 10.8954 14.001 12 14.001C13.1046 14.001 14 13.1055 14 12.001ZM19 10.001C20.1046 10.001 21 10.8964 21 12.001C21 13.1055 20.1046 14.001 19 14.001C17.8954 14.001 17 13.1055 17 12.001C17 10.8964 17.8954 10.001 19 10.001Z"></path></svg></div></div></div></div></div></li>
<li id="chat-messages-1008524388481642556" class="messageListItem-ZZ7v6g" aria-setsize="-1"><div class="message-2CShn3 cozyMessage-1DWF9U groupStart-3Mlgv1 wrapper-30-Nkg cozy-VmLDNB zalgo-26OfGz" role="article" data-list-item-id="chat-messages___chat-messages-1008524388481642556" tabindex="-1" aria-setsize="-1" aria-roledescription="Message" aria-labelledby="message-username-1008524388481642556 uid_1 message-content-1008524388481642556 uid_2 message-timestamp-1008524388481642556"><div class="contents-2MsGLg"><img src="{sender_avatar}" aria-hidden="true" class="avatar-2e8lTP clickable-31pE3P sender" alt=" "><h2 class="header-2jRmjb" aria-labelledby="message-username-1008524388481642556 message-timestamp-1008524388481642556"><span id="message-username-1008524388481642556" class="headerText-2z4IhQ"><span class="username-h_Y3Us desaturateUserColors-1O-G89 clickable-31pE3P sender" aria-controls="popout_119" aria-expanded="false" role="button" tabindex="0">{sender_username}</span><span id="bot" style="display: none;" class="botTagCozy-3NTBvK botTag-1NoD0B botTagRegular-kpctgU botTag-7aX5WZ rem-3kT9wc"><svg aria-label="Verified Bot" class="botTagVerified-2KCPMa" aria-hidden="false" role="img" width="16" height="16" viewBox="0 0 16 15.2"><path d="M7.4,11.17,4,8.62,5,7.26l2,1.53L10.64,4l1.36,1Z" fill="currentColor"></path></svg><span class="botText-1fD6Qk">BOT</span></span></span><span class="timestamp-p1Df1m timestampInline-_lS3aK"><time aria-label="Today at {now}" id="timestamp2" datetime="2022-08-14T23:55:51.691Z"><i class="separator-AebOhG" aria-hidden="true"> — </i>Today at {now}</time></span></h2><div id="message-content-1008524388481642556" class="markup-eYLPri messageContent-2t3eCI"><aaaaa class="anchor-1MIwyf anchorUnderlineOnHover-2qPutX" title="https://discord.gift/eeee" href="https://discord.gift/eeee" rel="noreferrer noopener" target="_blank" role="button" tabindex="0"><span class="spoilerText-27bIiA hidden-3B-Rum" aria-label="Spoiler" aria-expanded="false" tabindex="0" role="button"><span aria-hidden="true" id="code" class="inlineContent-2YnoDy">{nitro_code}</span></span></aaaaa></div></div><div id="message-accessories-1008524388481642556" class="container-2sjPya"><div class="giftCodeContainer-3ObH0O" style="position: relative;"><div class="tile-2mmK5T tileHorizontal-1DBMDZ embedHorizontal-2GF6zV checked"><div id="3suxn262qiz" class="tile-2mmK5T tileHorizontal-1DBMDZ embedHorizontal-2GF6zV checked">	
    <div class="media-1cVFCz mediaHorizontal-1eDgDq">
		<figure class="splashContainer-Bv4lwJ splashContainerHorizontal-2KmXEq">
			<div class="splash-PDbb7Y splashVideo-uVbleJ" style="opacity: 1;"><img class="splash-PDbb7Y splashVideo-uVbleJ" id="nitro_splash" src="{splash}" alt="Discord Nitro" style="opacity: 1;"></div>
		</figure>
	</div>
	<div class="description-X8_53U">
		<h2 class="title-oJa_A6">You gifted a subscription!</h2>
		<div class="tagline-3DhQWg">If you want to claim this gift for yourself, go right ahead! We won't judge :)</div>
		<div class="actions-3Gkxv6">
			<div class="tileActions-VUBz_1">
				<div class="flex-2S1XBF flex-3BkGQD horizontal-112GEH horizontal-1Piu5- flex-3BkGQD directionRow-2Iu2A9 justifyBetween-wAERV6 alignStretch-Uwowzr noWrap-hBpHBz" style="flex: 1 1 auto;">
					<div class="flex-1xMQg5 flex-1O1GKY horizontal-1ae9ci horizontal-2EEEnY flex-1O1GKY directionRow-3v3tfG justifyStart-2NDFzi alignStretch-DpGPf3 noWrap-3jynv6" style="flex: 1 1 auto;margin: 0;padding: 0;border: 0;font-weight: inherit;font-style: inherit;font-family: inherit;font-size: 100%;vertical-align: baseline;outline: 0;display: flex;-webkit-box-align: stretch;-ms-flex-align: stretch;align-items: stretch;-webkit-box-pack: start;-ms-flex-pack: start;justify-content: flex-start;-ms-flex-wrap: nowrap;flex-wrap: nowrap;-webkit-box-orient: horizontal;-webkit-box-direction: normal;-ms-flex-direction: row;flex-direction: row;margin-left: 0;margin-right: 10px;">
						<button type="button" id="tipw9qkhmkg" class="button-f2h6uQ lookFilled-yCfaCM colorBrand-I6CyqQ sizeSmall-wU2dO- grow-2sR_-F" style="font-family: Whitney, Helvetica Neue, Helvetica, Arial, sans-serif;font-weight: 500;border: none;cursor: pointer;text-rendering: optimizeLegibility;outline: 0;position: relative;display: flex;-webkit-box-pack: center;-ms-flex-pack: center;justify-content: center;-webkit-box-align: center;-ms-flex-align: center;align-items: center;-webkit-box-sizing: border-box;box-sizing: border-box;background: none;border-radius: 3px;font-size: 14px;line-height: 16px;padding: 2px 16px;-webkit-user-select: none;-moz-user-select: none;-ms-user-select: none;user-select: none;-webkit-transition: background-color .17s ease, color .17s ease;transition: background-color .17s ease, color .17s ease;width: auto;height: 32px;min-width: 60px;min-height: 32px;color: #fff;background-color: #6064f4;">
							<div class="contents-18-Yxp">Accept</div>
						</button>
					</div>
					<div class="flex-2S1XBF flex-3BkGQD vertical-3aLnqW flex-3BkGQD directionColumn-3pi1nm justifyEnd-2G0m6w alignEnd-2awoY_ noWrap-hBpHBz metadata-3MqUp5" style="flex: 1 1 auto;">Expires in 47 hours</div>
				</div>
			</div>
		</div>
	</div>
</div></div><div class="erd_scroll_detection_container erd_scroll_detection_container_animation_active" style="visibility: hidden; display: inline; width: 0px; height: 0px; z-index: -1; overflow: hidden; margin: 0px; padding: 0px;"><div dir="ltr" class="erd_scroll_detection_container" style="position: absolute; flex: 0 0 auto; overflow: hidden; z-index: -1; visibility: hidden; width: 100%; height: 100%; left: 0px; top: 0px;"><div class="erd_scroll_detection_container" style="position: absolute; flex: 0 0 auto; overflow: hidden; z-index: -1; visibility: hidden; inset: -1px 0px 0px -1px;"><div style="position: absolute; flex: 0 0 auto; overflow: scroll; z-index: -1; visibility: hidden; width: 100%; height: 100%;"><div style="position: absolute; left: 0px; top: 0px; width: 685px; height: 184px;"></div></div><div style="position: absolute; flex: 0 0 auto; overflow: scroll; z-index: -1; visibility: hidden; width: 100%; height: 100%;"><div style="position: absolute; width: 200%; height: 200%;"></div></div></div></div></div></div></div><div class="buttonContainer-1502pf"><div class="buttons-3dF5Kd container-2gUZhU isHeader-2bbX-L" role="group" aria-label="Message Actions"><div class="wrapper-2vIMkT"><div class="button-3bklZh" aria-label="Add Reaction" aria-controls="popout_120" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M12.2512 2.00309C12.1677 2.00104 12.084 2 12 2C6.477 2 2 6.477 2 12C2 17.522 6.477 22 12 22C17.523 22 22 17.522 22 12C22 11.916 21.999 11.8323 21.9969 11.7488C21.3586 11.9128 20.6895 12 20 12C15.5817 12 12 8.41828 12 4C12 3.31052 12.0872 2.6414 12.2512 2.00309ZM10 8C10 6.896 9.104 6 8 6C6.896 6 6 6.896 6 8C6 9.105 6.896 10 8 10C9.104 10 10 9.105 10 8ZM12 19C15.14 19 18 16.617 18 14V13H6V14C6 16.617 8.86 19 12 19Z"></path><path d="M21 3V0H19V3H16V5H19V8H21V5H24V3H21Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="Edit" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="16" height="16" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M19.2929 9.8299L19.9409 9.18278C21.353 7.77064 21.353 5.47197 19.9409 4.05892C18.5287 2.64678 16.2292 2.64678 14.817 4.05892L14.1699 4.70694L19.2929 9.8299ZM12.8962 5.97688L5.18469 13.6906L10.3085 18.813L18.0201 11.0992L12.8962 5.97688ZM4.11851 20.9704L8.75906 19.8112L4.18692 15.239L3.02678 19.8796C2.95028 20.1856 3.04028 20.5105 3.26349 20.7337C3.48669 20.9569 3.8116 21.046 4.11851 20.9704Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="More" aria-controls="popout_121" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M7 12.001C7 10.8964 6.10457 10.001 5 10.001C3.89543 10.001 3 10.8964 3 12.001C3 13.1055 3.89543 14.001 5 14.001C6.10457 14.001 7 13.1055 7 12.001ZM14 12.001C14 10.8964 13.1046 10.001 12 10.001C10.8954 10.001 10 10.8964 10 12.001C10 13.1055 10.8954 14.001 12 14.001C13.1046 14.001 14 13.1055 14 12.001ZM19 10.001C20.1046 10.001 21 10.8964 21 12.001C21 13.1055 20.1046 14.001 19 14.001C17.8954 14.001 17 13.1055 17 12.001C17 10.8964 17.8954 10.001 19 10.001Z"></path></svg></div></div></div></div></div></li>
<li id="chat-messages-1008466017527279626" class="messageListItem-ZZ7v6g" aria-setsize="-1"><div class="message-2CShn3 cozyMessage-1DWF9U groupStart-3Mlgv1 wrapper-30-Nkg cozy-VmLDNB zalgo-26OfGz {'mentioned-Tre-dv' if '[PING]' in messages[0] else ''}" role="article" data-list-item-id="chat-messages___chat-messages-1008466017527279626" tabindex="-1" aria-setsize="-1" aria-roledescription="Message" aria-labelledby="message-username-1008466017527279626 uid_1 message-content-1008466017527279626 uid_2 message-timestamp-1008466017527279626"><div class="contents-2MsGLg"><img src="{receiver_avatar}" aria-hidden="true" class="avatar-2e8lTP clickable-31pE3P receiver" alt=" "><h2 class="header-2jRmjb" aria-labelledby="message-username-1008466017527279626 message-timestamp-1008466017527279626"><span id="message-username-1008466017527279626" class="headerText-2z4IhQ"><span class="username-h_Y3Us desaturateUserColors-1O-G89 clickable-31pE3P receiver" aria-controls="popout_18939" aria-expanded="false" role="button" tabindex="0">{receiver_username}</span></span><span class="timestamp-p1Df1m timestampInline-_lS3aK"><time aria-label="Today at 4:03 PM" id="timestamp3" datetime="2022-08-14T20:03:54.971Z"><i class="separator-AebOhG" aria-hidden="true"> — </i>Today at {now}</time></span></h2><div id="response" class="markup-eYLPri messageContent-2t3eCI">{messages[1].replace('[PING]', f'<span class="mention wrapper-1ZcZW- mention interactive" aria-expanded="false" tabindex="0" role="button">@{receiver_username}</span>') if '[PING]' in messages[1] else messages[1]}
</div></div><div id="message-accessories-1008466017527279626" class="container-2sjPya"></div><div class="buttonContainer-1502pf"><div class="buttons-3dF5Kd container-2gUZhU isHeader-2bbX-L" role="group" aria-label="Message Actions"><div class="wrapper-2vIMkT"><div class="button-3bklZh" aria-label="Add Reaction" aria-controls="popout_18980" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M12.2512 2.00309C12.1677 2.00104 12.084 2 12 2C6.477 2 2 6.477 2 12C2 17.522 6.477 22 12 22C17.523 22 22 17.522 22 12C22 11.916 21.999 11.8323 21.9969 11.7488C21.3586 11.9128 20.6895 12 20 12C15.5817 12 12 8.41828 12 4C12 3.31052 12.0872 2.6414 12.2512 2.00309ZM10 8C10 6.896 9.104 6 8 6C6.896 6 6 6.896 6 8C6 9.105 6.896 10 8 10C9.104 10 10 9.105 10 8ZM12 19C15.14 19 18 16.617 18 14V13H6V14C6 16.617 8.86 19 12 19Z"></path><path d="M21 3V0H19V3H16V5H19V8H21V5H24V3H21Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="Reply" role="button" tabindex="0"><svg class="icon-1zidb7" width="24" height="24" viewBox="0 0 24 24"><path d="M10 8.26667V4L3 11.4667L10 18.9333V14.56C15 14.56 18.5 16.2667 21 20C20 14.6667 17 9.33333 10 8.26667Z" fill="currentColor"></path></svg></div><div class="button-3bklZh" aria-label="More" aria-controls="popout_18981" aria-expanded="false" role="button" tabindex="0"><svg class="icon-1zidb7" aria-hidden="true" role="img" width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M7 12.001C7 10.8964 6.10457 10.001 5 10.001C3.89543 10.001 3 10.8964 3 12.001C3 13.1055 3.89543 14.001 5 14.001C6.10457 14.001 7 13.1055 7 12.001ZM14 12.001C14 10.8964 13.1046 10.001 12 10.001C10.8954 10.001 10 10.8964 10 12.001C10 13.1055 10.8954 14.001 12 14.001C13.1046 14.001 14 13.1055 14 12.001ZM19 10.001C20.1046 10.001 21 10.8964 21 12.001C21 13.1055 20.1046 14.001 19 14.001C17.8954 14.001 17 13.1055 17 12.001C17 10.8964 17.8954 10.001 19 10.001Z"></path></svg></div></div></div></div></div></li>
</div>
</body>
</html>
  '''

class HTML2Image:
  """
  Convert HTML & CSS to images quickly.
  """
  HTML_TO_IMAGE = "https://htmlcsstoimage.com/"
  GENERATE_IMAGE = "https://htmlcsstoimage.com/demo_run"
  def __init__(self):
    """
    Initalize the HTML2Image class and set up a requests session.
    """
    self.session = requests.Session()
  def _get_cookies(self) -> None:
    """
    Retrieves cookies for the HTML & CSS to image API.
    """
    response = self.session.get(self.HTML_TO_IMAGE)
    if 'Set-Cookie' not in response.headers:
      raise Exception('Failed to receive cookie for hTML2Image.')
  def _get_image(self, css: str, html: str, render_when_ready: bool, selector: str = None) -> Union[str, bool]:
    """
    Converts HTML & CSS to an image and returns the URL.
    """
    if selector == None:
      selector = ""
    height = 370
    payload = {
      "html": html,
      "console_mode": "",
      "url": "",
      "css": css,
      "selector": selector,
      "ms_delay": "",
      "render_when_ready": "false",
      "viewport_height": height,
      "viewport_width": "767",
      "google_fonts": "",
      "device_scale": ""
    }
    response = self.session.post(self.GENERATE_IMAGE, headers={
      'accept-language': 'en-US,en;q=0.8',
      'content-length': str(len(json.dumps(payload))),
      'content-type': 'application/json',
      'origin': 'https://htmlcsstoimage.com',
      'referer': 'https://htmlcsstoimage.com/',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'sec-gpc': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }, json=payload)
    if 'url' in response.json():
      return response.json()['url']
    return False

class ProofUtils:
  """
  ProofUtils, a swift package to generate fake gifting proofs for Discord owners.
  """
  
  AVATARS_API_ENDPOINT = "https://api.github.com/repos/itschasa/Discord-Scraped/git/trees/cbd70ab66ea1099d31d333ab75e3682fd2a80cff"
  AVATAR_GET_API_ENDPOINT = "https://api.github.com/repos/itschasa/Discord-Scraped/git/blobs/{blob}"
  
  def __init__(self, sender_username: str, sender_avatar: str, receiver_username: str, messages: list, nitro_type: int, html_client: HTML2Image = None):
    """
    Initalize ProofUtils and provide the variables needed for generating proofs.
    """
    self.sender_username = sender_username
    self.sender_avatar = sender_avatar
    self.receiver_username = receiver_username
    self.messages = messages
    self.nitro_type = nitro_type # Regular, Classic, Basic
    self.html_client = html_client
    self.avatar_list = None

    if type(self.messages) != list:
      raise TypeError("Messages variable is not a list.")
  def fetch_avatars(self) -> None:
    """
    Fetches a list of avatars for generating proofs.
    """
    avatar_urls = []
    response = requests.get(self.AVATARS_API_ENDPOINT).json()
    for avatar in response["tree"]:
      avatar_urls.append(avatar["sha"])
    self.avatar_list = avatar_urls
  def get_avatar(self) -> Union[str, None]:
    """
    Returns a random avatar from list of avatars. (Must fetch avatars first)
    """
    if self.avatar_list == None:
      raise Exception('No avatars found, fetch avatars before trying to get an avatar.')

    def fetch_avatar() -> str:
      """
      Fetchs an avatar and returns base64 data URI.
      """
      url = self.AVATAR_GET_API_ENDPOINT.replace("{blob}", random.choice(self.avatar_list))
      content = requests.get(url).json()["content"]
      avatar = 'data:image/jpeg;base64,' + content
      
      return avatar
      
    return fetch_avatar()
  def fetch_sender_avatar(self) -> str:
    """
    Fetchs the sender's avatar and returns base64 data URI.
    """
    response = requests.get(self.sender_avatar)
    return 'data:image/' + self.sender_avatar.rsplit('.', 1)[1] + ';base64,' + base64.b64encode(response.content).decode('utf-8')
  def generate(self) -> Union[bytes, bool]:
    """
    Generates a nitro giting proof and returns the image.
    """
    if self.avatar_list == None:
      self.fetch_avatars() # Use fetch_avatars before to speed up the process of generating proofs.
    
    receiver_avatar = self.get_avatar()
    for i, message in enumerate(self.messages):
      if "\n" in message:
        self.messages[i] = message.replace('\n', '<br>')

    nitro_code = 'https://discord.gift/' + ''.join([random.choice(string.ascii_letters + string.digits) for i in range(16)])

    css = ""
    with open('style.css', 'r') as f:
      css = css + f.read()
    with open('style2.css', 'r') as f:
      css = css + f.read()

    self.sender_avatar = self.fetch_sender_avatar()
    body = format_html(self.sender_username, self.sender_avatar, self.receiver_username, receiver_avatar, self.messages, self.nitro_type, nitro_code)

    if self.html_client == None:
      hti = HTML2Image()
      hti._get_cookies()
    else:
      hti = self.html_client
      
    rendered = hti._get_image(css, body, True)
    if type(rendered) == str:
      response = requests.get(rendered)
      return io.BytesIO(response.content)
    else:
      return False
