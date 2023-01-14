try:
    # System imports.
    from typing import Tuple, Any, Union, Optional

    import asyncio
    import sys
    import datetime
    import json
    import functools
    import os
    import random as py_random
    import logging
    import uuid
    import json
    import subprocess

    # Third party imports.
    from fortnitepy.ext import commands
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    from functools import partial

    from datetime import timedelta

    import crayons
    try:
        import PirxcyPinger
    except:
        pass
    import fortnitepy
    import FortniteAPIAsync
    import sanic
    import aiohttp
    import uvloop
    import requests

except ModuleNotFoundError as e:
    print(f'Error: {e}\nAttempting to install packages now.')

    for module in (
        'crayons',
        'PirxcyPinger',
        'fortnitepy==3.6.8',
        'FortniteAPIAsync',
        'sanic==21.6.2',
        'aiohttp',
        'requests'
    ):
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

    os.system('clear')

    print('Installed packages, restarting script.')

    python = sys.executable
    os.execl(python, python, *sys.argv)


print(crayons.blue(f'Mathyslolbots by Mathyslol, Cousin & helped by Pirxcy.'))
print(crayons.magenta(f'Discord server: https://discord.gg/EFZj6SdYzk - For support, questions, etc.'))


sanic_app = sanic.Sanic(__name__)
server = None

cid = ""
name = ""
friendlist = ""

password = "9678"
copied_player = ""
__version__ = "1.5"
adminsss = 'MathyslolFN'
owner = '097271eaeea9430a9e8e1ebe92a65b6b'
errordiff = 'errors.com.epicgames.common.throttled', 'errors.com.epicgames.friends.inviter_friendships_limit_exceeded'

shit_partys_errrors = 'errors.com.epicgames.social.party.invite_already_exists', 'errors.com.epicgames.social.party.party_not_found', 'errors.com.epicgames.social.party.stale_revision', 'errors.com.epicgames.social.party.party_change_forbidden', 'errors.com.epicgames.social.party.invite_forbidden'#HTTPexception (soon...)fix error like party invalid etc


vips = ""#no one 


with open('info.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

#vip command (kicked)
#def is_vips():
    #async def predicate2(ctx):
        #return ctx.author.display_name in vips
    #return commands.check(predicate2)

def is_admin():
    async def predicate(ctx):
        return ctx.author.display_name in info['FullAccess']
    return commands.check(predicate)


#only me (Mathyslol)
def is_owner():
    async def predicate1(ctx):
        return ctx.author.id in owner
    return commands.check(predicate1)


prefix = '!','?','/','',' ','+'



@sanic_app.middleware('response')
async def custom_banner(request: sanic.request.Request, response: sanic.response.HTTPResponse):
    response.headers["Access-Control-Allow-Origin"] = "*/*"


@sanic_app.route('/', methods=['GET'])
async def root(request: sanic.request.Request) -> None:
    if 'Accept' in request.headers and request.headers['Accept'] == 'application/json':
        return sanic.response.json(
            {
                "status": "online"
            }
        )

    return sanic.response.html(
        """
<html>
   <head>
      <style>
         body {
         font-family: Arial, Helvetica, sans-serif;
         position: absolute;
         left: 50%;
         top: 50%;  
         -webkit-transform: translate(-50%, -50%);
         transform: translate(-50%, -50%);
         background-repeat: no-repeat;
         background-attachment: fixed;
         background-size: cover;
         background-color: #333;
         color: #f1f1f1;
         }
 
        ::-webkit-scrollbar {
          width: 0;
        }
        :root {
          --gradient: linear-gradient(90deg, #4ce115, #15c5e1, #e17815);
 
        }
        body {
          font-family: basic-sans, sans-serif;
          min-height: 100vh;
          display: flex;
          justify-content: ;
          align-items: center;
          font-size: 1.125em;
          line-height: 1.6;
          color: #2e2d2d;
          background: #ddd;
          background-size: 300%;
          background-image: var(--gradient);
          animation: bg-animation 25s infinite;
        }
        @keyframes bg-animation {
          0% {background-position: left}
          50% {background-position: right}
          100% {background-position: left}
        }
        .content {
          background: white;
          width: 70vw;
          padding: 3em;
          box-shadow: 0 0 3em rgba(0,0,0,.15);
        }
        .title {
          margin: 0 0 .5em;
          text-transform: uppercase;
          font-weight: 900;
          font-style: italic;
          font-size: 3rem;
          color: #2e2d2d;
          line-height: .8;
          margin: 0;
          
          background-image: var(--gradient);
          background-clip: text;
          color: transparent;
          // display: inline-block;
          background-size: 100%;
          transition: background-position 1s;
        }
        .title:hover {
          background-position: right;
        }
        .fun {
          color: white;
 
      </style>
   </head>
   <body>
      <center>
         <h2 id="response">
            """ + f"""Online now {name}""" + """
            <h2>
            """ + f"""Total Friends: {friendlist}/1000""" + """
            </h2>
            <h2>
            """ + f"""💎 Version {__version__} 💎""" + """
 
            </h2>
         </h2>
      </center>
   </body>
</html>
        """
    )


@sanic_app.route(
  '/stop',
  methods=[
    "POST"
  ]
)
async def stopall(request):
  if request.method == "POST":
    python = sys.executable
    os.execl(python, python, *sys.argv) 
    

@sanic_app.route("/default")
async def index(request):
    return sanic.response.json(
        {
            "username": name,
            "friend_count": friendlist,
            "cid": cid
        }
    )

@sanic_app.route('/ping', methods=['GET'])
async def accept_ping(request: sanic.request.Request) -> None:
    return sanic.response.json(
        {
            "status": "online"
        }
    )


@sanic_app.route('/name', methods=['GET'])
async def display_name(request: sanic.request.Request) -> None:
    return sanic.response.json(
        {
            "display_name": name
        }
    )


class XBXBOT(commands.Bot):
    def __init__(self, device_id: str, account_id: str, secret: str, loop=asyncio.get_event_loop(), **kwargs) -> None:

        self.status = '🏁 STARTING 🏁'
        
        self.fortnite_api = FortniteAPIAsync.APIClient()
        self.loop = asyncio.get_event_loop()

        super().__init__(
            command_prefix=prefix,
            case_insensitive=True,
            auth=fortnitepy.DeviceAuth(
                account_id=account_id,
                device_id=device_id,
                secret=secret
            ),
            status=self.status,
            platform=fortnitepy.Platform('PS5'),
            **kwargs
        )

        self.session = aiohttp.ClientSession()

        self.skin = "CID_NPC_Athena_Commando_M_Apparition_Heavy"
        self.backpack = "Backpack_FNBirthday5"
        self.pickaxe = "Pickaxe_ID_376_FNCS"
        self.banner = "BRS19_ShowdownPanda"
        self.bn_color = "defaultcolor22"
        self.level = 1000
        self.tier = 1000
        self.uptimerobot_key = ""
        self.remove_bots = ""

        self.sanic_app = sanic_app
        self.server = server



        self.rst = "F"
        self.vr = "0.0"
        self.bl = "0.0"

        self.ban_player = ""
        self.bl_msg = ""
        self.ban_lobbybots = ""

        self.bl_inv = 'MathyslolFN'
        self.inv_on = "F"
 
        self.adminx = "MathyslolFN"
 
        self.inv_all = "F"
        self.url = f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co"
 
        self.skin_bl = ("")
        self.add_auto = ''
        self.number = ""
 
 
        self.inv_msg = "Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n"
      
        self.add_msg = "Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n"
      
        self.join_msg = "Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n Want FREE SKINS & BATTLE PASS ? \n 1. USE CODE : XBX \n 2. Invite 5 friends on this Lobby \n 3. Free 4K V-BUCKS code in this map 2743-6640-6400 \n~~~~~~~~<💚>~~~~~~~~ \n"
    
        
 
 
    async def add_list(self) -> None:
        try:
            if '097271eaeea9430a9e8e1ebe92a65b6b' in self.friends:
                await asyncio.sleep(0)
            else:
                await self.add_friend('097271eaeea9430a9e8e1ebe92a65b6b')
        except: pass
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// CHECK/ERROR/PARTY ////////////////////////////////////////////////////////////////////////////////////////////////////////        
    
    async def check_party_validity(self):
        await asyncio.sleep(80)
        try:
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
        except:
            pass
        await asyncio.sleep(80)
 
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// FRIENDS/ADD ////////////////////////////////////////////////////////////////////////////////////////////////////////
    
 
 
    async def set_and_update_party_prop(self, schema_key: str, new_value: Any) -> None:
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)
 
    async def event_device_auth_generate(self, details: dict, email: str) -> None:
        print(self.user.display_name)
 
 
 
    async def event_ready(self) -> None:
        global name
        global friendlist
        global cid
        
        name = self.user.display_name
        #get user outfit
        cid = self.party.me.outfit
        friendlist = len(self.friends)
 
        print(Fore.GREEN + "[+] " + Fore.RESET + f"Client ready as {self.user.display_name}.")
      
        if self.party.me.leader:
          await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)


        coro = self.sanic_app.create_server(
            host='0.0.0.0',
            port=8000,
            return_asyncio_server=True,
            access_log=False
        )
        self.server = await coro
 
        await asyncio.sleep(3)


        self.loop.create_task(self.add_list())

        #self.loop.create_task(self.invitefriends())

        self.loop.create_task(self.pinger())
        self.loop.create_task(self.update_api())
        #self.loop.create_task(self.uptimerobot())

        #self.loop.create_task(self.delete_pending_on_start())
        self.loop.create_task(self.checker_skin_bl())
        #self.loop.create_task(self.checker_status())
        #await asyncio.sleep(4)
        
        
        self.loop.create_task(self.delete_friends_last_logout())

        self.loop.create_task(self.auto_add_s())
        self.loop.create_task(self.check_update())
        self.loop.create_task(self.update_settings())



        

        try:   
          #print(f'Incoming pending friends: {len(self.incoming_pending_friends)}')

          for pending in self.incoming_pending_friends:
            try:
              epic_friend = await pending.accept()
              if isinstance(epic_friend, fortnitepy.Friend):
                  print(f"Accepted: {epic_friend.display_name}.")
              else:
                  print(f"Declined: {pending.display_name}.")
            except fortnitepy.InviteeMaxFriendshipsExceeded:
              await pending.decline()
              print(f"Declined: {pending.display_name}.")

              print(f"Declined: {pending.display_name}.")
              
            except fortnitepy.HTTPException as epic_error:
                if epic_error.message_code != 'errors.com.epicgames.common.throttled':
                    raise
                await asyncio.sleep(int(epic_error.message_vars[0] + 1))
                try:
                  await pending.accept()
                  print(f"Accepted: {pending.display_name}.")
                except:
                  try:
                    await pending.decline()
                    print(f"Declined: {pending.display_name}.")
                  except:
                    pass
            except:
              try:
                await pending.decline()
                print(f"Declined: {pending.display_name}.")
              except:
                print(f'Unable to accept or decine friend request from {pending.display_name}.')

        except:
          print('error in incoming')
        print(f'Incoming pending friends: {len(self.incoming_pending_friends)}')



      
#remove friends if the name is in my blacklist or pirxcys blacklist :)
        await asyncio.sleep(2)
        if self.remove_bots == "T":
          for friend in self.friends:
            if friend.display_name in self.ban_lobbybots or friend.id in self.ban_lobbybots or any(word in friend.display_name for word in self.ban_player):
              await friend.block()
              print(f'removed {friend} because its a lobbybot :)')





 
    async def auto_add_s(self):

      try:
        r = requests.get(f"https://control-bot-v3.mathyslolx.repl.co/add_auto.json").json()
      except:
        pass
      
      self.add_auto_check = r['name']
      self.added = r['active']

      if not self.add_auto_check == self.add_auto:
        self.add_auto = self.add_auto_check

      if self.added == 'T':
        try:
            user = await self.fetch_user(self.add_auto)
            friends = self.friends

            if user.id in friends:
                print(f'I already have {user.display_name} as a friend')
            else:
              try:
                await self.add_friend(user.id)
                print(f'Sent ! I send a  friend request to {user.display_name}.')
              except:
                pass

        except fortnitepy.HTTPException:
            print("There was a problem trying to add this friend.")
        except AttributeError:
            print("I can't find a player with that name.")
 
    #async def checker_status(self):
      #async with aiohttp.ClientSession() as session:
        #async with session.request(
            #method="GET",
            #url="https://control-bot-v3.mathyslolx.repl.co/status.json"
        #) as r:
            #data = await r.json()
 
           # if r.status == 200:
              #  self.status_verif = data['status']
 
                #if not self.status_verif == self.status:
                   # self.status = self.status_verif
 
                   # await self.set_presence(self.status)
                   # await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
 
    async def checker_skin_bl(self):

      try:
        jk = requests.get(f"https://control-bot-v3.mathyslolx.repl.co/skinbl.json").json()
      except:
        pass
 

      self.skinbl_check = jk['skinbl']

      if not self.skinbl_check == self.skin_bl:
          self.skin_bl = self.skinbl_check


    #async def uptimerobot(self):#deleted
      #name = self.user.display_name

      #try:
        
        #url = "https://api.uptimerobot.com/v2/newMonitor"
                  
        #payload = f"api_key={self.uptimerobot_key}&format=json&type=1&url=https://{os.environ['REPL_ID']}.id.repl.co&friendly_name={name}"
        #headers = {
           # 'cache-control': "no-cache",
          #  'content-type': "application/x-www-form-urlencoded"
             # }
                  
       # response = requests.request("POST", url, data=payload, headers=headers)
        #print('Uploaded to uptimerobot')
     # except:
       # print('Unable to upload in uptimerobot, do it manually')


    async def pinger(self):
        try:
            await PirxcyPinger.post(f"https://{os.environ['REPL_ID']}.id.repl.co")
        except:
            pass
        return

      
    
    #test for delete online friend with las logout 80 hours
    async def delete_friends_last_logout(self):
      now = datetime.datetime.now()
      try:
        for friend in self.friends:
          if friend.last_logout < now - timedelta(hours=200):
              await friend.remove()
              print(f'Removed {friend}')
      except:
        pass





 
    async def update_api(self) -> None:
        resp = requests.post(
                url=f'https://36978c7c-534d-4362-9a81-39d89f840079.id.repl.co/update',
                json={
                    "url": f"https://{os.environ['REPL_ID']}.id.repl.co"}
                    )
        try:
            await resp.json()
        except:
            pass
        return
 

    async def update_settings(self) -> None:
        while True:
          global vips
          global adminsss
          global __version__

          try:
            e = requests.get(f"https://control-bot-v3.mathyslolx.repl.co/restart.json").json()
          except:
            pass
          self.rst = e['restarting']
          self.vr = e['version']
          self.bl = e['versionbl']

          if self.rst == 'T':
              print('True for restarting')

              if not self.vr == self.bl:
                  python = sys.executable
                  os.execl(python, python, *sys.argv)



          try:
            z = requests.get(f"https://control-bot-v3.mathyslolx.repl.co/default.json").json()
          except:
            pass
          self.skin_check = z['skin']
          self.backpack_check = z['sac']
          self.pickaxe_check = z['pioche']
          self.banner_check = z['banner']
          self.bn_color_check = z['bn_color']
          self.level_check = z['level']
          self.tier_check = z['tier']
          self.add_msg_check = z['add_msg']
          self.inv_msg_check = z['inv_msg']
          self.inv_all_check = z['inv_all']
          self.join_msg_check = z['join_msg']
          self.vips_check = z['admin']
          self.versiongame = z['version_web']
          self.inv_bl = z['bl_inv']
          self.inv_on_check = z['inv_on']
          self.number_check = z['style']
          self.adminsss = z['admin']
          self.status_verif = z['status']
          self.uptimerobot_key_check = z['uptimerobot_apikey']
          self.remove_bots_check = z['remove_bots']

          
          if not self.remove_bots_check == self.remove_bots:
              self.remove_bots = self.remove_bots_check
                      
          if not self.status_verif == self.status:
              self.status = self.status_verif

              await self.set_presence(self.status)
              try:
                await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
              except:
                pass

          if not self.adminsss == adminsss:
              adminsss = self.adminsss

          if not self.uptimerobot_key_check == self.uptimerobot_key:
              self.uptimerobot_key = self.uptimerobot_key_check

            
          if not self.number_check == self.number:
              self.number = self.number_check
              try:
                await self.party.me.set_outfit(asset=self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number))
              except:
                pass

          if not self.inv_on_check == self.inv_on:
              self.inv_on = self.inv_on_check

          if not self.inv_bl == self.bl_inv:
              self.bl_inv = self.inv_bl

          if not self.versiongame == __version__:
              __version__ = self.versiongame

          if not self.vips_check == vips:
              vips = self.vips_check

          if not self.skin_check == self.skin:
              self.skin = self.skin_check

          if not self.backpack_check == self.backpack:
              self.backpack = self.backpack_check

          if not self.pickaxe_check == self.pickaxe:
              self.pickaxe = self.pickaxe_check

          if not self.banner_check == self.banner:
              self.banner == self.banner_check

          if not self.bn_color_check == self.bn_color:
              self.bn_color = self.bn_color_check

          if not self.level_check == self.level:
              self.level = self.level_check

          if not self.tier_check == self.tier:
              self.tier = self.tier_check

          if not self.add_msg_check == self.add_msg:
              self.add_msg = self.add_msg_check

          if not self.inv_msg_check == self.inv_msg:
              self.inv_msg = self.inv_msg_check

          if not self.join_msg_check == self.join_msg:
              self.join_msg = self.join_msg_check

          if not self.inv_all_check == self.inv_all:
              self.inv_all = self.inv_all_check



          try:
            await self.party.me.set_outfit(asset=self.skin)
            await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
          except:
            pass

          try:
            v = requests.get(f"https://control-bot-v3.mathyslolx.repl.co/kick.json").json()
          except:
            pass
          self.ban_player_check = v['ban']
          self.bl_msg_checks = v['bl_msg']

          if not self.ban_player_check == self.ban_player:
              self.ban_player = self.ban_player_check

          if not self.bl_msg_checks == self.bl_msg:
              self.bl_msg = self.bl_msg_checks

          try:
            try:
              hgd = requests.get(f"https://lobbybotconfiguration.pirxcy1942.repl.co/blacklist").json()
            except: 
              pass

            
            self.ban_lobbybots_check = hgd['blocked_names']
  
  
            if not self.ban_lobbybots_check== self.ban_lobbybots:
                self.ban_lobbybots = self.ban_lobbybots_check

          except:
            pass

          await asyncio.sleep(3600)#1 hour


 
    async def check_update(self):
        await asyncio.sleep(40)
        self.loop.create_task(self.update_settings())
        await asyncio.sleep(40)
        self.loop.create_task(self.check_update())


  
    async def event_party_invite(self, invite: fortnitepy.ReceivedPartyInvitation) -> None:
        if invite.sender.display_name in info['FullAccess']:
            await invite.accept()
            await self.party.me.edit(functools.partial(self.party.me.set_outfit,self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number)),functools.partial(self.party.me.set_backpack,self.backpack),functools.partial(self.party.me.set_pickaxe,self.pickaxe),functools.partial(self.party.me.set_banner,icon=self.banner,color=self.bn_color,season_level=self.level),functools.partial(self.party.me.set_battlepass_info,has_purchased=True,level=self.tier))
        elif self.inv_on == 'T':
          try:
            await invite.accept()
            await self.party.me.edit(functools.partial(self.party.me.set_outfit,self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number)),functools.partial(self.party.me.set_backpack,self.backpack),functools.partial(self.party.me.set_pickaxe,self.pickaxe),functools.partial(self.party.me.set_banner,icon=self.banner,color=self.bn_color,season_level=self.level),functools.partial(self.party.me.set_battlepass_info,has_purchased=True,level=self.tier))
            
          except fortnitepy.HTTPException:
            pass
        elif invite.sender.display_name in self.adminx:
          try:
            await invite.accept()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull: 
            pass
        else:
          try:
            await invite.decline()
            await invite.sender.send(self.inv_msg)
            await invite.sender.invite()
          except fortnitepy.HTTPException:
            pass
          except AttributeError:
            pass
          except fortnitepy.PartyError:
            pass
          except fortnitepy.Forbidden:
            pass
          except fortnitepy.PartyIsFull:
            pass
          except:
            pass
 
    async def event_friend_presence(self, old_presence: Union[(None, fortnitepy.Presence)], presence: fortnitepy.Presence):
        if not self.is_ready():
            await self.wait_until_ready()
        if self.inv_all == 'T':
            if old_presence is None:
                friend = presence.friend
                if friend.display_name != self.bl_inv:
                    try:
                        await friend.send(self.inv_msg)
                    except:
                        pass
                    else:
                        if not self.party.member_count >= 16:
                          try:
                            await friend.invite()
                          except:
                            pass
 
    async def event_party_member_update(self, member: fortnitepy.PartyMember) -> None:
        name = member.display_name
        if any(word in name for word in self.ban_player):
            try:
                await member.kick()
            except: pass
    
        if member.display_name in self.ban_player:
            try:
                await member.kick()
            except: pass
    
        if member.outfit in (self.skin_bl) and member.id != self.user.id:
            await member.kick()
 

 
    async def event_friend_request(self, request: fortnitepy.IncomingPendingFriend) -> None:
      if isinstance(request, fortnitepy.OutgoingPendingFriend):
          return

      print(f"Received friend request from: {request.display_name}.")
      try:
        await request.accept()
        print(f"Accepted friend request from: {request.display_name}.")

      except fortnitepy.InviteeMaxFriendshipsExceeded:
        await request.decline()

        print('delete 1 dans event friend req')
      except fortnitepy.MaxFriendshipsExceeded:
        request.decline()
 
    async def event_friend_add(self, friend: fortnitepy.Friend) -> None:
        try:
            await asyncio.sleep(0.3)
            await friend.send(self.add_msg.replace('{DISPLAY_NAME}', friend.display_name))
            await friend.invite()
        except: pass

  
    async def event_friend_remove(self, friend: fortnitepy.Friend) -> None:
        try:
            await self.add_friend(friend.id)
        except: pass


    async def event_party_member_join(self, member: fortnitepy.PartyMember) -> None:
      try:
        await self.party.send(self.join_msg.replace('{DISPLAY_NAME}', member.display_name))
 
        if self.default_party_member_config.cls is not fortnitepy.party.JustChattingClientPartyMember:
            await self.party.me.edit(functools.partial(self.party.me.set_outfit,self.skin,variants=self.party.me.create_variants(material=self.number,clothing_color=self.number,parts=self.number,progressive=self.number)),functools.partial(self.party.me.set_backpack,self.backpack),functools.partial(self.party.me.set_pickaxe,self.pickaxe),functools.partial(self.party.me.set_banner,icon=self.banner,color=self.bn_color,season_level=self.level),functools.partial(self.party.me.set_battlepass_info,has_purchased=True,level=self.tier))
 
            if not self.has_friend(member.id):
                try:
                    await self.add_friend(member.id)
                except: pass
 
            name = member.display_name
            if any(word in name for word in self.ban_player):
                try:
                    await member.kick()
                    try:
                      await member.block()
                      print(f'blocked {member}')
                    except:
                      pass
                except: pass
 
            if member.display_name in self.ban_player:
                try:
                    await member.kick()
                    try:
                      await member.block()
                    except:
                      pass
                except: pass
 
            if member.outfit in (self.skin_bl) and member.id != self.user.id:
                if not member.display_name in self.adminx:
                  await member.kick()
                  try:
                    await member.block()
                  except:
                    pass
      except:
        pass
 
    async def event_party_member_leave(self, member) -> None:
        if not self.has_friend(member.id):
            try:
                await self.add_friend(member.id)
            except: pass

              
    async def event_party_join_request(self, request) -> None:
      try:
        await request.accept()
        print('Accepted join request')
      except:
        pass

          

    async def event_party_message(self, message: fortnitepy.FriendMessage) -> None:
        if not self.has_friend(message.author.id):
            try:
                await self.add_friend(message.author.id)
            except: pass    

    async def event_friend_message(self, message: fortnitepy.FriendMessage) -> None:
        if not message.author.display_name != "MathyslolFN":
            await self.party.invite(message.author.id)

    async def event_party_message(self, message = None) -> None:
        if self.party.me.leader:
            if message is not None:
                if message.content in self.bl_msg:
                    if not message.author.display_name in self.adminx:
                        await message.author.kick()

    async def event_party_message(self, message: fortnitepy.FriendMessage) -> None:
        msg = message.content
        if self.party.me.leader:
            if message is not None:
                if any(word in msg for word in self.bl_msg):
                    if not message.author.display_name in self.adminx:
                        await message.author.kick()


    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, IndexError):
            pass
        elif isinstance(error, fortnitepy.HTTPException):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, TimeoutError):
            pass
        else:
            print(error)


 
    @commands.command(
      name="skin",
      aliases=[
        'outfit',
        'character'
      ]
    )
    async def skinx(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'pinkghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'ghoul':    
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))     
        elif content.lower() == 'pkg':  
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'colora':   
            await self.party.me.set_outfit(asset='CID_434_Athena_Commando_F_StealthHonor')
        elif content.lower() == 'pink ghoul':   
            await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        elif content.lower() == 'nikeu mouk':
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))  
        elif content.lower() == 'renegade': 
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'caca':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))        
        elif content.lower() == 'rr':   
            await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        elif content.lower() == 'skull trooper':    
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'skl':  
            await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        elif content.lower() == 'honor':    
            await self.party.me.set_outfit(asset='CID_342_Athena_Commando_M_StreetRacerMetallic') 
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaCharacter")
                await self.party.me.set_outfit(asset=cosmetic.id)
                await ctx.send(f'Skin set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass
 
    @commands.command(
      name="backpack",
      aliases=[
        'sac'
      ]
    )
    async def backpackx(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaBackpack")
            await self.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass
 
    #@commands.command()
    #async def vips(self, ctx: fortnitepy.ext.commands.Context) -> None:
        #await ctx.send('you have the perms')
        #await ctx.send('now you can have perms to kick people')

 
    #@is_vips()
    #@commands.command()
    #async def kicked(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        #if epic_username is None:
            #user = await self.fetch_user(ctx.author.display_name)
            #member = self.party.get_member(user.id)
        #else:
            #user = await self.fetch_user(epic_username)
           # member = self.party.get_member(user.id)
 
        #if member is None:
            #await ctx.send("Failed to find that user, are you sure they're in the party?")
       # else:
           # try:
               # if not member.display_name in info['FullAccess']:
                    #await member.kick()

                   # await ctx.send(f"Kicked user: {member.display_name}.")
            #except fortnitepy.errors.Forbidden:
               # await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")
    
 
    @commands.command(aliases=['crowns'])
    async def crown(self, ctx: fortnitepy.ext.commands.Context, amount: str) -> None:
        meta = self.party.me.meta
        data = (meta.get_prop('Default:AthenaCosmeticLoadout_j'))['AthenaCosmeticLoadout']
        try:
            data['cosmeticStats'][1]['statValue'] = int(amount)
        except KeyError:
          data['cosmeticStats'] = [{"statName": "TotalVictoryCrowns","statValue": int(amount)},{"statName": "TotalRoyalRoyales","statValue": int(amount)},{"statName": "HasCrown","statValue": 0}]
          
        final = {'AthenaCosmeticLoadout': data}
        key = 'Default:AthenaCosmeticLoadout_j'
        prop = {key: meta.set_prop(key, final)}
      
        await self.party.me.patch(updated=prop)
 
        await asyncio.sleep(0.2)
        await ctx.send(f'Set {int(amount)} Crowns')
        await self.party.me.clear_emote()
        await self.party.me.set_emote('EID_Coronet')
 
      
    @commands.command(
      name="emote",
      aliases=[
        'danse',
        'dance'
      ]
    )
    async def emotex(self, ctx: fortnitepy.ext.commands.Context, *, content = None) -> None:
        if content is None:
            await ctx.send()
        elif content.lower() == 'sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Sce':
            await self.party.me.set_emote(asset='EID_KpopDance03')    
        elif content.lower() == 'scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')
        elif content.lower() == 'Scenario':
            await self.party.me.set_emote(asset='EID_KpopDance03')     
        else:
            try:
                cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaDance")
                await self.party.me.clear_emote()
                await self.party.me.set_emote(asset=cosmetic.id)
                await ctx.send(f'Emote set to {cosmetic.name}.')

            except FortniteAPIAsync.exceptions.NotFound:
                pass    
 
 
    @commands.command(aliases=['actual','actuel'])
    async def current(self, ctx: fortnitepy.ext.commands.Context, content = None) -> None:
        if content is None:
            await ctx.send(f"Missing argument. Try: !current (skin, backpack, emote, pickaxe, banner)")
        elif content.lower() == 'banner':
            await ctx.send(f'Banner ID: {self.party.me.banner[0]}  -  Banner Color ID: {self.party.me.banner[1]}')
        else:
            items = {
                "skin": self.party.me.outfit,
                "backpack": self.party.me.backpack,
                "emote": self.party.me.emote,
                "pickaxe": self.party.me.pickaxe,
            }
            id = items.get(content)
            info = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search?id={id}").json()
            cosmetic = info['data']
            try:
              await ctx.send(f"My current {content} is: {cosmetic['name']}  -  ID: {cosmetic['id']}")
            except KeyError:
              await ctx.send(f"I couldn't find a {content} name for that.")

 
    @commands.command(
      name="tier",
      aliases=[
        'bp',
        'battlepass'
      ]
    )
    async def tierx(self, ctx: fortnitepy.ext.commands.Context, tier: int) -> None:
        if tier is None:
            await ctx.send(f'No tier was given. Try: !tier (tier number)') 
        else:
            await self.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )
 
        await ctx.send(f'Battle Pass tier set to: {tier}')

 
 
    @commands.command(
      name="random",
      aliases=[
        'rdm'
      ]
    )
    async def randomx(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type = None) -> None:
        if cosmetic_type is None:
            await ctx.send("Missing argument. Try: !random (skin, emote)")
          
        elif cosmetic_type == 'skin':
            all_outfits = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaCharacter")
            random_skin = py_random.choice(all_outfits).id
            await self.party.me.set_outfit(asset=random_skin,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
            await ctx.send(f'Skin randomly set to {random_skin}.')
          
        elif cosmetic_type == 'emote':
            all_emotes = await self.fortnite_api.cosmetics.get_cosmetics(lang="en",searchLang="en",backendType="AthenaDance")
            random_emote = py_random.choice(all_emotes).id
            await self.party.me.set_emote(asset=random_emote)
            await ctx.send(f'Emote randomly set to {random_emote}.')


    @commands.command(
      name="pickaxe",
      aliases=[
        'pioche'
      ]
    )
    async def pickaxex(self, ctx: fortnitepy.ext.commands.Context, *, content: str) -> None:
        try:
            cosmetic = await self.fortnite_api.cosmetics.get_cosmetic(lang="en",searchLang="en",matchMethod="contains",name=content,backendType="AthenaPickaxe")
            await self.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to {cosmetic.name}.')

        except FortniteAPIAsync.exceptions.NotFound:
            pass
 
    @commands.command(aliases=['news'])
    @commands.cooldown(1, 10)
    async def new(self, ctx: fortnitepy.ext.commands.Context, cosmetic_type: str = 'skin') -> None:
        cosmetic_types = {'skin': {'id': 'cid_','function': self.party.me.set_outfit},'backpack': {'id': 'bid_','function': self.party.me.set_backpack},'emote': {'id': 'eid_','function': self.party.me.set_emote},}

        if cosmetic_type not in cosmetic_types:
            return await ctx.send('Invalid cosmetic type, valid types include: skin, backpack & emote.')

        new_cosmetics = await self.fortnite_api.cosmetics.get_new_cosmetics()

        for new_cosmetic in [new_id for new_id in new_cosmetics if
                             new_id.id.lower().startswith(cosmetic_types[cosmetic_type]['id'])]:
            await cosmetic_types[cosmetic_type]['function'](asset=new_cosmetic.id)

            await ctx.send(f"{cosmetic_type}s set to {new_cosmetic.name}.")

            await asyncio.sleep(3)

        await ctx.send(f'Finished equipping all new unencrypted {cosmetic_type}s.')      
 
    @commands.command()
    async def purpleskull(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_030_Athena_Commando_M_Halloween',variants=self.party.me.create_variants(clothing_color=1))
        await ctx.send(f'Skin set to Purple Skull Trooper!')
        
    @commands.command()
    async def pinkghoul(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_029_Athena_Commando_F_Halloween',variants=self.party.me.create_variants(material=3))
        await ctx.send('Skin set to Pink Ghoul Trooper!')
        
    @commands.command(aliases=['checkeredrenegade','raider'])
    async def renegade(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_028_Athena_Commando_F',variants=self.party.me.create_variants(material=2))
        await ctx.send('Skin set to Checkered Renegade!')
        
    @commands.command()
    async def aerial(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_017_Athena_Commando_M')
        await ctx.send('Skin set to aerial!')

    @is_owner()
    @commands.command()
    async def repl(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'{self.url}')

 
    @commands.command()
    async def hologram(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_outfit(asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG')
        await ctx.send('Skin set to Star Wars Hologram!')  

    @commands.command()
    async def cid(self, ctx: fortnitepy.ext.commands.Context, character_id: str) -> None:
        await self.party.me.set_outfit(asset=character_id,variants=self.party.me.create_variants(profile_banner='ProfileBanner'))
        await ctx.send(f'Skin set to {character_id}.')
 
 
    @commands.command()
    async def eid(self, ctx: fortnitepy.ext.commands.Context, emote_id: str) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset=emote_id)
        await ctx.send(f'Emote set to {emote_id}!')
        
    @commands.command()
    async def bid(self, ctx: fortnitepy.ext.commands.Context, backpack_id: str) -> None:
        await self.party.me.set_backpack(asset=backpack_id)
        await ctx.send(f'Backbling set to {backpack_id}!')


    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.clear_emote()
        await ctx.send('Stopped emoting.')
        
    @commands.command()
    async def point(self, ctx: fortnitepy.ext.commands.Context, *, content: Optional[str] = None) -> None:
        await self.party.me.clear_emote()
        await self.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pickaxe set & Point it Out played.')
        

    copied_player = ""


    @commands.command()
    async def stop(self, ctx: fortnitepy.ext.commands.Context):
        global copied_player
        if copied_player != "":
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return
        else:
            try:
                await self.party.me.clear_emote()
            except RuntimeWarning:
                pass
 

    @commands.command(aliases=['clone', 'copi', 'cp'])
    async def copy(self, ctx: fortnitepy.ext.commands.Context, *, epic_username = None) -> None:
        global copied_player

        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)

        elif 'stop' in epic_username:
            copied_player = ""
            await ctx.send(f'Stopped copying all users.')
            await self.party.me.clear_emote()
            return

        elif epic_username is not None:
            try:
                user = await self.fetch_user(epic_username)
                member = self.party.get_member(user.id)
            except AttributeError:
                await ctx.send("Could not get that user.")
                return
        try:
            copied_player = member
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants),partial(fortnitepy.ClientPartyMember.set_pickaxe,asset=member.pickaxe,variants=member.pickaxe_variants))
            await ctx.send(f"Now copying: {member.display_name}")
        except AttributeError:
            await ctx.send("Could not get that user.")

    async def event_party_member_emote_change(self, member, before, after) -> None:
        if member == copied_player:
            if after is None:
                await self.party.me.clear_emote()
            else:
                await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_emote,asset=after))                        
                
    async def event_party_member_outfit_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,asset=member.outfit,variants=member.outfit_variants))
            
    async def event_party_member_outfit_variants_change(self, member, before, after) -> None:
        if member == copied_player:
            await self.party.me.edit_and_keep(partial(fortnitepy.ClientPartyMember.set_outfit,variants=member.outfit_variants))
 
#///////////////////////////////////////////////////////////////////////////////////////////////////////////// PARTY/FRIENDS/ADMIN //////////////////////////////////////////////////////////////////////////////////////////////////////
 
    @commands.command()
    async def add(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: str) -> None:
        user = await self.fetch_user(epic_username)
        friends = self.friends

        if user.id in friends:
            await ctx.send(f'I already have {user.display_name} as a friend')
        else:
          try:
            await self.add_friend(user.id)
            await ctx.send(f'Done, friend request send to {user.display_name}.')
          except fortnitepy.FriendshipRequestAlreadySent:
            pass
          except fortnitepy.InviteeMaxFriendshipRequestsExceeded:
            pass
          except:
            pass
 
    @is_admin()
    @commands.command()
    async def restart(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'Restarting...')
        python = sys.executable
        os.execl(python, python, *sys.argv)    
 
    @is_admin()
    @commands.command()
    async def set(self, ctx: fortnitepy.ext.commands.Context, nombre: int) -> None:
        await self.party.set_max_size(nombre)
        await ctx.send(f'Set party to {nombre} player can join')
        
    @commands.command()
    async def ready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.READY)
        await ctx.send('Ready!')
    
    @commands.command(aliases=['sitin'],)
    async def unready(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
        await ctx.send('Unready!')
 
    @commands.command(
      name="level",
      aliases=[
        'niveau'
      ]
    )
    async def levelx(self, ctx: fortnitepy.ext.commands.Context, banner_level: int) -> None:
        await self.party.me.set_banner(season_level=banner_level)
        await ctx.send(f'Set level to {banner_level}.')
 
        
    @is_admin()
    @commands.command()
    async def sitout(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
        await ctx.send('Sitting Out!')
            
    @is_admin()
    @commands.command()
    async def leave(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await self.party.me.leave()
        await ctx.send(f'I Leave')
        await self.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
 
    @is_admin()
    @commands.command()
    async def version(self, ctx: fortnitepy.ext.commands.Context) -> None:
        await ctx.send(f'Version: {__version__}')
 
    @is_admin()
    @commands.command(aliases=['unhide', 'hihihiha', 'hey'])
    async def promote(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)
 
        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                await member.promote()
                await ctx.send(f"Promoted user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to promote {member.display_name}, as I'm not party leader...")
 
    @is_admin()
    @commands.command()
    async def kick(self, ctx: fortnitepy.ext.commands.Context, *, epic_username: Optional[str] = None) -> None:
        if epic_username is None:
            user = await self.fetch_user(ctx.author.display_name)
            member = self.party.get_member(user.id)
        else:
            user = await self.fetch_user(epic_username)
            member = self.party.get_member(user.id)

        if member is None:
            await ctx.send("Failed to find that user, are you sure they're in the party?")
        else:
            try:
                if not member.display_name in info['FullAccess']:
                    await member.kick()
                    await ctx.send(f"Kicked user: {member.display_name}.")
            except fortnitepy.errors.Forbidden:
                await ctx.send(f"Failed to kick {member.display_name}, as I'm not party leader.")

    async def set_and_update_party_prop(self, schema_key: str, new_value: str):
        prop = {schema_key: self.party.me.meta.set_prop(schema_key, new_value)}

        await self.party.patch(updated=prop)
 
 
    @commands.command(aliases=['ghost'])
    async def hide(self, ctx: fortnitepy.ext.commands.Context, *, user = None):
        if self.party.me.leader:
            if user != "all":
                try:
                    if user is None:
                        user = await self.fetch_profile(ctx.message.author.id)
                        member = self.party.get_member(user.id)
                    else:
                        user = await self.fetch_profile(user)
                        member = self.party.get_member(user.id)
 
                    raw_squad_assignments = self.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]
 
                    for m in raw_squad_assignments:
                        if m['memberId'] == member.id:
                            raw_squad_assignments.remove(m)
 
                    await self.set_and_update_party_prop('Default:RawSquadAssignments_j',{'RawSquadAssignments': raw_squad_assignments})
                    await ctx.send(f"Hid {member.display_name}")
                except AttributeError:
                    await ctx.send("I could not find that user.")
                except fortnitepy.HTTPException:
                    await ctx.send("I am not party leader!")
            else:
                try:
                    await self.set_and_update_party_prop('Default:RawSquadAssignments_j',{'RawSquadAssignments': [{'memberId': self.user.id,'absoluteMemberIdx': 1}]})
                    await ctx.send("Hid everyone in the party.")
                except fortnitepy.HTTPException:
                    await ctx.send("I am not party leader!")
        else:
            await ctx.send("I need party leader to do this!")


    @is_admin()
    @commands.command()
    async def id(self, ctx: fortnitepy.ext.commands.Context, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
        
        elif user is None:
            user = await self.fetch_profile(ctx.message.author.id)
        try:
            await ctx.send(f"{user}'s Epic ID is: {user.id}")
            print(Fore.GREEN + ' [+] ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
        except AttributeError:
            await ctx.send("I couldn't find an Epic account with that name.")

    @is_admin()
    @commands.command()
    async def user(self, ctx: fortnitepy.ext.commands.Context, *, user = None, hidden=True):
        if user is not None:
            user = await self.fetch_profile(user)
            try:
                await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
                print(Fore.GREEN + ' [+] ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
            except AttributeError:
                await ctx.send(f"I couldn't find a user that matches that ID")
        else:
            await ctx.send(f'No ID was given. Try: !user (ID)')

 
    async def invitefriends(self):
      try:
        while True:
          mins = 60
          send = []
          for friend in self.friends:
              if friend.is_online():
                  send.append(friend.display_name)
                  await friend.invite()
          await asyncio.sleep(mins*60)
      except:
        pass
 
    @is_admin()
    @commands.command()
    async def invite(self, ctx: fortnitepy.ext.commands.Context) -> None:
        try:
            self.loop.create_task(self.invitefriends())
        except Exception:
            pass       
 
    @commands.command(aliases=['friends'])
    async def epicfriends(self, ctx: fortnitepy.ext.commands.Context) -> None:
        onlineFriends = []
        offlineFriends = []

        try:
            for friend in self.friends:
                if friend.is_online():
                    onlineFriends.append(friend.display_name)
                else:
                    offlineFriends.append(friend.display_name)
            
            await ctx.send(f"Total Friends: {len(self.friends)} / Online: {len(onlineFriends)} / Offline: {len(offlineFriends)} ")
        except Exception:
            await ctx.send(f'Not work')
 
 
    @is_admin()
    @commands.command()
    async def whisper(self, ctx: fortnitepy.ext.commands.Context, message = None) -> None:
        try:
            for friend in self.friends:
                if friend.is_online():
                    await friend.send(message)

            await ctx.send(f'Send friend message to everyone')
            
        except: pass
    
    @is_owner()
    @commands.command()
    async def fixadmin(self, ctx: fortnitepy.ext.commands.Context):
        if ctx.author.display_name == 'MathyslolFN':
            try:
                info['FullAccess'].append('MathyslolFN')
                with open('info.json', 'w') as f:
                    json.dump(info, f, indent=4)
    
                await ctx.send('done, now restarting...')
                await asyncio.sleep(1)
                python = sys.executable
                os.execl(python, python, *sys.argv)    
            except:
                pass
        else:
            await ctx.send("You don't have perm.")
            



    @commands.command()
    async def say(self, ctx: fortnitepy.ext.commands.Context, *, message = None):
        if message is not None:
            await self.party.send(message)
            await ctx.send(f'Sent "{message}" to party chat')
        else:
            await ctx.send(f'No message was given. Try: ! say (message)')
 
    

 

 
    @is_admin()
    @commands.command()
    async def admin(self, ctx: fortnitepy.ext.commands.Context, setting = None, *, user = None):
        if (setting is None) and (user is None):
            await ctx.send(f"Missing one or more arguments. Try: ! admin (add, remove, list) (user)")
        elif (setting is not None) and (user is None):

            user = await self.fetch_profile(ctx.message.author.id)

            if setting.lower() == 'add':
                if user.display_name in info['FullAccess']:
                    await ctx.send("You are already an admin")

                else:
                    await ctx.send("Password?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == password:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")

            elif setting.lower() == 'remove':
                if user.display_name not in info['FullAccess']:
                    await ctx.send("You are not an admin.")
                else:
                    await ctx.send("Are you sure you want to remove yourself as an admin?")
                    response = await self.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if (content.lower() == 'yes') or (content.lower() == 'y'):
                        info['FullAccess'].remove(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send("You were removed as an admin.")
                            print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    elif (content.lower() == 'no') or (content.lower() == 'n'):
                        await ctx.send("You were kept as admin.")
                    else:
                        await ctx.send("Not a correct reponse. Cancelling command.")
                    
            elif setting == 'list':
                if user.display_name in info['FullAccess']:
                    admins = []

                    for admin in info['FullAccess']:
                        user = await self.fetch_profile(admin)
                        admins.append(user.display_name)

                    await ctx.send(f"The bot has {len(admins)} admins:")

                    for admin in admins:
                        await ctx.send(admin)

                else:
                    await ctx.send("You don't have permission to this command.")

            else:
                await ctx.send(f"That is not a valid setting. Try: ! admin (add, remove, list) (user)")
                
        elif (setting is not None) and (user is not None):
            user = await self.fetch_profile(user)

            if setting.lower() == 'add':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name not in info['FullAccess']:
                        info['FullAccess'].append(user.display_name)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                            print(Fore.GREEN + " [+] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                    else:
                        await ctx.send("That user is already an admin.")
                else:
                    await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
            elif setting.lower() == 'remove':
                if ctx.message.author.display_name in info['FullAccess']:
                    if user.display_name in info['FullAccess']:
                        await ctx.send("Password?")
                        response = await self.wait_for('friend_message', timeout=20)
                        content = response.content.lower()
                        if content == password:
                            info['FullAccess'].remove(user.display_name)
                            with open('info.json', 'w') as f:
                                json.dump(info, f, indent=4)
                                await ctx.send(f"{user.display_name} was removed as an admin.")
                                print(Fore.BLUE + " [+] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                        else:
                            await ctx.send("Incorrect Password.")
                    else:
                        await ctx.send("That person is not an admin.")
                else:
                    await ctx.send("You don't have permission to remove players as an admin.")
            else:
                await ctx.send(f"Not a valid setting. Try: ! -admin (add, remove) (user)")
 
 
    @is_admin()#this is a dangerous command (it ban bot more faster i think)
    @commands.command(aliases=['removeall'])
    async def removefriends(self, ctx: fortnitepy.ext.commands.Context) -> None:
      """Removes All Friends (made by pirxcy :0)"""
      total = 0
      online = 0
      offline = 0
      await ctx.send("Removing All Friends Please Wait...")
      for friend in self.friends:
        if friend.is_online():
          online += 1
        else:
          offline += 1
        total += 1
        await friend.remove()
        print(f"Removed {friend.id}")
      await ctx.send(
          f"""
Total Friends Removed: {total}
Online Friends Removed: {online}
Offline Friends Removed: {offline} 
          """
        )




        


#if u are here gg skid
 
#I spent time on this . pls dont skid ty !