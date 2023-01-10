from cakework import Client

if __name__ == "__main__":
    client = Client("jessie")
    result= client.say_hello()
    print(result)
