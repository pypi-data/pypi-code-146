from eel_quickstart import create_main, create_web

if __name__ == '__main__':
    print("Eel QuickStart 🐋 ...")
    main_web_path = input("Input⌨ -> Enter your main folder name : ")
    create_web(main_web_path)
    create_main(main_web_path)