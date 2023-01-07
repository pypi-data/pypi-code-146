# importing module
import sys
# appending a path
sys.path.append('../src')
import intents as it
def main():

    if len(sys.argv) > 3:
        if(sys.argv[1]) == 'make_intent_from_file':
            make_intent_from_file(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])


def make_intent_from_file(tag,filepath,response,intentsFilePath):
    it.addIntent(tag,filepath,response)
    it.createIntents(intentsFilePath)



if __name__ == "__main__":
    main()

