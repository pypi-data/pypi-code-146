import argparse
from .utils import configfile, find_ressource_id, get_uid, formattime
import datetime
from .create import login_create
from .updateres import login_update
from .fullall import reserve_all as killswitch
from . import __version__


def cli():
    parser = argparse.ArgumentParser(description="Create reservations at csfoy gym.")

    # set up
    parser.add_argument("-v", '--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(help='create/modify reservations', dest="cmd")
    
    # create
    parser_create = subparsers.add_parser('create', help='create a new reservation')
    parser_create.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")
    parser_create.add_argument("-u", "--userID", type=str, default=configfile.userID, help="userID used for reservations")
    parser_create.add_argument("-t", "--time", type=str, default=datetime.datetime.now().strftime("%H"), help="starting hour of the reservation")
    parser_create.add_argument("-r", "--resource", type=str, default="30", help="resource number (1-80)")
    parser_create.add_argument("-f", "--force", action="store_true", default=False, help="overwrite existing reservation")
    parser_create.add_argument("-s", "--scheduleId", type=str, default=configfile.gym_scheduleId, help="sport id (default is 64 for gym)")
    parser_create.add_argument("-v", "--verbose", action="store_true", default=False, help="prints the html response")

    # update
    parser_update = subparsers.add_parser('update', help='update an existing reservation')
    parser_update.add_argument("reference_number", type=str, help="reference number of the reservation to update")
    parser_update.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")
    parser_update.add_argument("-u", "--userID", type=str, default=configfile.userID, help="userID used for reservations")
    parser_update.add_argument("-t", "--time", type=str, default=datetime.datetime.now().strftime("%H"), help="starting hour of the reservation")
    parser_update.add_argument("-r", "--resource", type=str, default="30", help="resource number (1-80)")
    parser_update.add_argument("-s", "--scheduleId", type=str, default=configfile.gym_scheduleId, help="sport id (default is 64 for gym)")
    parser_update.add_argument("-v", "--verbose", action="store_true", default=False, help="prints the html response")

    # fullall
    parser_killswitch = subparsers.add_parser('killswitch', help='book all slots & overwrite existing ones (dangerous)')
    parser_killswitch.add_argument("-s", "--secret", type=str, help="secret passphrase")
    parser_killswitch.add_argument("-d", "--day", type=str, default=f"{datetime.date.today()}", help=f"day of reservation, format: {datetime.date.today()}")

    # config
    parser_config = subparsers.add_parser('config', help='current configuration and credentials')
    parser_config.add_argument("-s", "--show", action="store_true", default=False, help="shows the current configuration")
    parser_config.add_argument("--mat", type=str, dest="matricule", help="set matricule used for reservations")
    parser_config.add_argument("--pwd", type=str, dest="password", help="set password used for reservations")
    parser_config.add_argument("--uid", type=str, dest="uid", help="set userID used for reservations")
    parser_config.add_argument("--get-uid", dest="auto_uid", action="store_true", default=False, help="automatically finds & set your uid based on your matricule & password")


    args = parser.parse_args()
    

    
    

    if (args.cmd == None):
        parser.error("no arguments were passed, see documentation for more help")
        
    elif (args.cmd == "create"):

        starthour, endhour = formattime(args.time)

        # correcting resource id with the lease method
        # OG_resource_number = int(args.resource)
        # resource_number = OG_resource_number
        # if OG_resource_number > 25:
        #     resource_number += 208
        # if OG_resource_number > 60:
        #     resource_number += 144
        # resource_number = str(resource_number + 4745)

        rids = find_ressource_id(configfile.username, configfile.password, args.scheduleId, configfile.proxies)
        resource_number = rids[min(int(args.resource)-1, len(rids)-1)]

        print(f"\033[0;36mSending reservation request for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m")
        ref_num = login_create(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=resource_number, day=args.day, starthour=starthour, endhour=endhour, verbose=args.verbose, proxies=configfile.proxies)

        if (ref_num == None and args.force):
            print("Request did not work")
            try:
                print(
                    f"\033[0;36mSending \033[91mwith force\033[0;36m for {starthour}, {args.day}\nAt resource {args.resource}, using {args.userID}, for scheduleId {args.scheduleId}.\033[0m"
                )
                # using the last slot possible since it is rarely used
                last_rid = rids[-1]
                ref_num = login_create(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=last_rid, day=args.day, starthour=starthour, endhour=endhour, verbose=args.verbose, proxies=configfile.proxies)
                if (ref_num == None):
                    print(f"cgs couldn't reserve buffer at {last_rid}")
                    raise Exception
                print(f"successfully created with force a buffer reservation at {last_rid}")
            except:
                print("An internal cgs error happend")
        
    elif (args.cmd == "update"):

        # adds zero to single digits
        starthour, endhour = formattime(args.time)

        rids = find_ressource_id(configfile.username, configfile.password, args.scheduleId, configfile.proxies)
        resource_number = rids[int(args.resource)-1]

        login_update(configfile.username, configfile.password, uid=args.userID, scheduleId=args.scheduleId, resourceId=resource_number, day=args.day, starthour=starthour, endhour=endhour, referenceNumber=args.reference_number, verbose=args.verbose, proxies=configfile.proxies)
    
    elif (args.cmd == "killswitch"):
        if args.secret == "MyNameYo":
            killswitch(configfile.username, configfile.password, sport_id_range=[53, 64], days_list=[args.day], proxies=configfile.proxies)
        else:
            parser.error("wrong passphrase")
    
    elif (args.cmd == "config"):
        if (args.uid == None and args.matricule == None and args.password == None and args.show == False and args.auto_uid == False):
            parser.error("no arguments were passed, see documentation for more help")

        if (args.uid != None):
            configfile.mod("userID", args.uid)

        if (args.matricule != None):
            configfile.mod("username", args.matricule)

        if (args.password != None):
            configfile.mod("password", args.password)

        if (args.show):
            print(configfile)

        if (args.auto_uid):
            sp_id_list = [str(configfile.gym_scheduleId), '27']
            sp_id_list += [str(i) for i in range(100)]
            get_uid(configfile.username, configfile.password, sport_id=sp_id_list)
            
