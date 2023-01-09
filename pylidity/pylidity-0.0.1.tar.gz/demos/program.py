from pylidator.validators import contains

def check_contains_word():
    subject =  "Hello there, my name is yaa baby, I'm from Ghana"
    seed = "gHana"
    options = {
        "ignore_case": True
    }
    it_contains_ghana = contains(subject, seed, options)

    if it_contains_ghana:
        print('The statement contains Ghana')
    else:
        print('Keyword: "Ghana" was not found')




if __name__ == '__main__':
    check_contains_word()