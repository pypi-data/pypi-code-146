from pyChatGPTLoop import ChatGPT
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    while True:
        #session_token = input('Please enter your session token: ')
        session_token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..dOIee_4p63frKMuo.ai_DVIiW9N0aFvhMGp6zAuXtk0IQSexwwP3RpNNZ5jbE6OkNpXgWXagWrUVwu_UULNpotXbturouh45s3WXd6w1ICIdLyOroRoYuvXKbmhHbPBSUQyhdOgDr9qQ8hMsqk6VQqgZU6ZGJ3x8vI-oZDzo0XyRL17mCHqEWhmQ0zrSqmTgLcg5UYdel6OMC-T0_b90mw5ItyGFSfrPbupT54bpUfrbOAC52OXHgdHNtwPw-_3rA4VuaWCdgGrl_6oSyHyOOzXjwauMz1jw_wJsJM51boUlgpZ_avzv62W7HWi2envlQ59RyFfJ4Gsr3PxGiOAer_2-2wF6eC_wMYKYwOF_jaFzuq0mJjgPNaqJ0khpAKJNjrXjrPAOgSzUFX1J1RG4rAt4t_xl6olUlnfjlcMx2kJh3-8_hNE_-SIneXmXAV9H92hocndwrc4cq98CNtGKusTScSepkrpQMzoNaKIrVrl9tmHhEZz1FClOkyNudg-VxkRvYjw52VQTXpSITWHjMoomi-QyOqiyxibYMFfl6ymrRFEZOfQI1ahBbNDNvsxbZA4plkgCFa4njpKHFIuUk1-98ycJD5ZZeUDeNGAOUJU12xmKDvVNn8NxH29ZFOxNf1awnpvlogDsXP3Jn0R861lvkwwkLzdTdHvzIaGl76YaJ-mNUN8F7dQtYnt9lzBNVZLX91vyNf-cBf_BRksUFRC798IdYaRasb4vk_wzkeR2kyLCnht7gE_vGsv0H0RDdXYovCA6utEKzEiCxc-BxPEuLLckmybL55wXBDA371zqIliQ-IUaZJILteQ7bBosWY1hu1ErSubKWIvJMK7oiQG1Ut4EH-6D7zMJSmBVslP77JxjBfA0SFEjkKCkB2bgWmTn-7s0utrdkSqoa9IvdDa4mydjIquW9OhkEX0g5mv78hS9mbyyMG9mE5ECVLRYRv48ieYniMEIF0pqn1aav_PlBxa1_rGr4KkuBnXIJ-T4AGY09uyWjNLh8uMClTTzU2ZcJBhzKS4QJBf90FPJDHkqxYhHmpUlfI23DTfpWed7ZSfeVH7c5mVRCRbYDKNbIU2ew0i6xx30ksGyFp_vexh7-gVPH1AK5heSQwE01S_hm3oD_YhXIZ6j46JIhDnjcVClj2ZJ6Q7T-QAn4L-wzOwpwuS1g-tOLK0e4JcLzR4J_dksFk3IG80IJnI7_K9221g4NcIndWukN3oGzc7ctOdgyEzqA2QpBzCsVGgvp2DIHYXN6rg8nTP0WfboJ92BlEh08lpSVp9J1n-J7aTsLMEshS8goLh24GfuXJEwuldTaddCwYYTfC8_SLlK4YgvqexjWVXaEvjwB1wfngSnRIzkdT3LcE3VJrVSs8ONi5drE9dlharQEzUPXA8ywA6Bz4ZX2HZEm0nYE7HVLl5rEOcBsK7j7IBRRaBDYfeimMLj_s7AXapi3j44nFXCjxfYZwVISb1ocsjDilw9Y5amR0mWMcHI6EsfnbUJibigFwXWenOaXIl2xxgsdtHWG2Rl47JxcgLDV2b1jLyE5rdpfjf5RHU2AECRmxnhbgcUFmq91nUiE7DlmkVH01F5FfrkO6lL9cR2hhNRoSUQVgmKUDNES0IFr69l_o8UdBoMIB9jwgG3TYwqnc5Z1FJXzwKXkE1DBOdFwqeMDHQU1m1r4LZjQ6uluTlxOWAtM2nzSrgkxeCm5MBcs929inPRfTlzH9Es0AlxSLpCR3Yi-PL6tQnWcN2DYOjta1pVp0RZKWevawfgoR80J26sWyQxtV8gf1m4JU9td7vOocYyGG4NI5kbQMLxwaJS0XUmwvBkEfq8l3TfJAkqWRS1kT3MW-WjeapcvLLEcZ0bjiW4cTzNmqVh9XCIQw7N-21KB1urpIu6XgOdFMaMVQDp_h7TWeS05xPhHYtq46W6hfTcpcp0a9UeOWAcEijLxWmCeC98f_xurFTMGhg88xNiolbRM8JJebXkIlABz5K-ivQXBeXVgCYeKY89oWH6y4B1pQKB_SZ55sAS_vTAWyWxzkxUSZFYTH99UawKKw6BcY8emaJOqbokgSxpPqno1L0dPIMKkCiz8PCD5wKo1wek2V4WSvYP1-CcD7q5B9-IDRBn40d7kEK5r_2NqmKXc1slx8fQdLeAld31KBVEftY1z22fNvI8U3-DF4r2X5IOdhmVu_YS_aL8LjaAj1_AYzQO8QCE6MVooHauVWVUKXOI3NSa450vgjEJlY2OkZc76xloXB8nQPuOJNXjSKbGrTYG2jrOpecMdtnQ9hYgZRt-61TxIVjFzIzgWN1iJDWFb8AMbhaxG8j4ce_8tYVxXl1B8pe4vJh7S3aFX3wR4vQ-O-0LgdqQO9nVd1rU.9kH-KWhU-p_fTNd8TrpV8w"
        # conversation_id = input(
        #     'Please enter your conversation id (if you want to continue old chat): '
        # )
        conversation_id = "7116af01-860b-42a6-a875-eb5e8e7e5b7b"
        #proxy = input('Please enter your proxy if you have: eg: http://127.0.0.1:8080')
        proxy = "http://127.0.0.1:1090"
        #driver_path = input('Please enter your chromedriver path if you have: eg: D:\\chromedriver.exe')
        driver_path = "E:\\Path\\Python37\\chromedriver.exe"
        chat = ChatGPT(session_token, conversation_id,proxy=proxy,driver_path=driver_path)
        break

    clear_screen()
    print(
        'Conversation started. Type "reset" to reset the conversation.Type "back some words" to loop the conversation. Type "quit" to quit.\n'
    )
    words = [
        {
            "content":r'Now you are going to pretend to be a math teacher called "nothing" to help me with my math',
            "AI_verify":True
            },
        {
            "content":r"You will be very strict in pointing out my mistakes",
            "AI_verify":False
            }
    ]
    '''
    An example of initializing the vocabulary format, the vocabulary content is not representative
    '''
    
    while True:
        prompt = input('\nYou: ')
        if prompt.lower() == 'reset':
            chat.reset_conversation()
            #clear_screen()
            print(
                'Conversation started. Type "reset" to reset the conversation. Type "back some words" to loop the conversation.Type "quit" to quit.\n'
            )
            
        elif prompt.lower().split(' ')[0] == 'back':
            
            print('\nChatGPT: ', end='')
            loop_text = prompt.lower().split('back')[1][1:]
            response = chat.backtrack_chat(loop_text)
            if response:
                print("yes!", end='')
            else:
                print("error!", end='')
                
        elif prompt.lower() == 'quit':
            break
        
        elif prompt.lower() == "new":
            res = chat.init_personality(True,words)
            if res:
                print("yes!")
            else:
                print("no!")
                
        else:
            print('\nChatGPT: ', end='')
            response = chat.send_message(prompt)
            print(response['message'], end='')
