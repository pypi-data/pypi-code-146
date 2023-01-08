"""Load questions from q: a: txt file."""


def load_qa_file(file_name, debug=False):
    """Load qa file.

    Text file with sentences started with 'q: ' and 'a: '

    Args:
        file_name: text file to pen
        debug: debug

    Result:
        array of dict
    """
    my_question = None
    mode = 0
    # mode = 0   line for line
    # mode = 1   q: """   so add lines to question until """
    # mode = 2   a: """   so add lines to answer until """
    questions = []
    try:
        with open(file_name, "r") as file1:
            for line in file1:
                if line.startswith('q:"""'):
                    my_question = line[5:]
                    if my_question == "\n":
                        my_question = ""
                    mode = 1
                    continue
                if line.startswith('a:"""'):
                    my_answer = line[5:]
                    if my_answer == "\n":
                        my_answer = ""
                    mode = 2
                    continue
                if line.strip() == '"""':
                    if mode == 1:
                        mode = 0
                        continue
                    if mode == 2:
                        line = "a: "+my_answer
                        mode = 0
                if mode == 1:
                    my_question += line
                    continue
                if mode == 2:
                    my_answer += line
                    continue
                if line.startswith("q: "):
                    my_question = line[3:].strip()
                if line.startswith("a: "):
                    my_answer = line[3:].strip()
                    if my_question is not None:
                        if debug is True:
                            print(my_question + "  //  " + my_answer)
                        question = {"q": my_question, "a": my_answer}
                        questions.append(question)
                        my_question = None
                        mode = 0
    except FileNotFoundError:
        print(f"can't open qa file: {file_name}")
    return questions
