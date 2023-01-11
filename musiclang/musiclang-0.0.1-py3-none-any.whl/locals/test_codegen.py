

PREPROCESS = False
PREDICT = True

if PREPROCESS:
    config_file = []
    import os
    os.makedirs('data_clean', exist_ok=True)
    for file in os.listdir('dataset_score'):
        with open(os.path.join('dataset_score', file), 'r') as fd:
            data = fd.read().replace('\n', '').replace('\t', '').replace('(p', '(\np').replace(')+ (', ')+\n(').replace(', p', ',\np')

        new_file = str(os.path.join('data_clean', file))
        with open(new_file, 'w') as fd:
            fd.write(data)

        config_file.append("{" + f' "text": "{new_file}"' + "}")


    with open('config/mycode.json', 'w') as fd:

        fd.write("\n".join(config_file))



from transformers import AutoModelForCausalLM, AutoTokenizer


checkpoint = "model_ml_2"
model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

text ="""(I % II.b.M)(
piano__1=s0.o(-1).pp,
piano__2=s2.o(-1).pp,
piano__3=s4.o(-1).p,
piano__4=s0.o(-2).p)+
(IV % II.b.M)(
piano__1=s4.o(-2).pp,
piano__2=s0.o(-1).p,
piano__3=s2.o(-1).p,
piano__4=s0.o(-3).pp)+
(I % II.b.M)(
piano__1=s0.qd.o(-1).pp,
piano__2=s2.qd.o(-1).pp,
piano__3=s4.qd.o(-1).p,
piano__4=s0.qd.o(-2).pp)+
(II['65'] % II.b.M)(
piano__1=s6.e.o(-2).pp,
piano__2=s0.e.o(-1).pp,
piano__3=s4.e.o(-1).p,
piano__4=s2.e.o(-3).pp)+
(V % II.b.M)(
piano__1=s3.o(-2).pp,
piano__2=s4.o(-2).pp,
piano__3=s0.o(-1).p,
piano__4=s0.o(-3).pp)+
(V % II.b.M)(
piano__1=s2.o(-2).pp,
piano__2=s4.o(-2).pp,
piano__3=s0.o(-1).p,
piano__4=s0.ed.o(-2).pp + l.t + s6.t.o(-3).pp)
"""


for i in range(100):
    completion = model.generate(**tokenizer(text, return_tensors="pt"), temperature=0.01, min_length=100, do_sample=True, max_new_tokens=200)
    text = tokenizer.decode(completion[0])
    print(text)

# def hello_world():
#     print("Hello World")
#
# hello_world()