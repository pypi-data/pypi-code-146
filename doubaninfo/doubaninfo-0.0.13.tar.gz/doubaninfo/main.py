from doubaninfo.doubaninfo import *

def main():
    args = readargs()
    if args.json:
        if args.cookie:
            getdoubaninfo_json(url=args.url,cookie=args.cookie,cp=args.copy)
        else:
            getdoubaninfo_json(url=args.url,cp=args.copy)
    else:
        if args.cookie:
            getdoubaninfo(url=args.url,cookie=args.cookie,cp=args.copy)
        else:
            getdoubaninfo(url=args.url,cp=args.copy)


if __name__ == '__main__':
    main()