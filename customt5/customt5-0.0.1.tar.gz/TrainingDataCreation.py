import pandas as pd
from num2words import num2words
import random
import string

#
# path = f"datasets/T5_training Data.csv"
#
# df = pd.read_csv(path).dropna()
# new_df = pd.DataFrame(data={"Sentences": [None], "UseCase": [None]})
# for d in range(1, len(df)):
#     try:
#         Sentences = df[d - 1:d]["Sentences"]
#         UseCase = df[d - 1:d]["UseCase"]
#         Sentences1 = Sentences[d].split()[0]
#         UseCase1 = UseCase[d].split()[0]
#         new_df=new_df.append({"Sentences": Sentences[d], "UseCase": UseCase[d].replace(UseCase1, Sentences1)},ignore_index=True)
#     except:
#         pass
# new_df.dropna().to_csv("datasets/T5_training Data new.csv")

df = pd.DataFrame(data={"Sentences": [None], "UseCase": [None]})


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def create_training_data():
    global df
    usecases = ["range", "is_null", "not_null", "is_date", "is_not_date", "is_number", "is_not_number"]
    for usecase in usecases:
        if usecase == "range":
            for i in range(0, 200):
                num1 = random.randint(0, 9999)
                num2 = random.randint(0, 99999)
                name = get_random_string(6)
                Sentences = ["%s should not be greater than %d ,but less than %d" % (name, num2, num1),
                             "%s must be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s could be greater than %d ,but less than %d" % (name, num1, num2),
                             "%s is more than %d ,but less than %d" % (name, num1, num2),
                             "%s is greater than %d,but less than %d" % (name, num1, num2),
                             "%s must be greater than %d,but less than  %d" % (name, num1, num2),
                             "%s exceeds %d,but does not exceeds %d" % (name, num1, num2),
                             "%s could be less than %d and more than %d" % (name, num1, num2),
                             "%s might be in between %d to %d" % (name, num1, num2),
                             "%s can be in range %d to %d" % (name, num1, num2),
                             "%s is with in %d to %d" % (name, num1, num2),
                             "%s must be in between %d to %d" % (name, num1, num2),
                             "%s is more than %d and also %s should not exceed %d" % (name, num1, name, num2),
                             "%s is comprised between %d, excluded, and %d" % (name, num1, num2),
                             "%s is strictly greater than %d and strictly lower than %d" % (name, num1, num2),
                             "%s IS LONGER THAN %s AND ALSO %s IS SMALL THAN %s" % (
                                 name, num2words(num1), name, num2words(num2)),
                             "%s lies between %s and %s" % (name, num2words(num1), num2words(num2)),
                             "%s equals a number under %d and over %d" % (name, num1, num2),
                             "%s shall be found somewhere between %d and %d" % (name, num1, num2)
                             ]
                if num1 > num2:
                    temp = num2
                    num2 = num1
                    num1 = temp
                for Sentence in Sentences:
                    UseCase = "Value is_within(%d,%d)" % (num1, num2)
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "not_null":
            for i in range(0, 200):
                name = get_random_string(6)
                Sentences = ["%s cannot be null" % name,
                             "%s is not null" % name,
                             "%s can not be equal to null" % name,
                             "%s can not be left empty" % name,
                             "%s cannot be empty" % name,
                             "%s is not empty" % name,
                             "%s can not be equal to empty" % name,
                             "%s can not be left blank" % name,
                             "%s cannot be blank" % name,
                             "%s is not blank" % name,
                             "%s can not be equal to blank" % name,
                             "%s could not be equal to blank" % name,
                             "%s must not be blank" % name,
                             "%s must not be empty" % name,
                             "%s must not be null" % name,
                             "%s should not be empty" % name,
                             "%s should not be null" % name,
                             "%s should not be blank" % name,
                             "%s could not be empty" % name,
                             "%s could not be null" % name,
                             "%s could not be blank" % name,
                             "%s would not be empty" % name,
                             "%s would not be null" % name,
                             "%s would not be blank" % name,
                             "%s isn't empty." % name,
                             "%s number should not be null." % name,
                             "%s depth must not be null" % name,
                             "%s is not null." % name,
                             "%s could not be null." % name,
                             "%s is not a null" % name,
                             "%s mustn't be null" % name,
                             "%s mustn't be empty." % name,
                             "%s mustn't be an empty string." % name,
                             "%s cannot be null." % name,
                             "%s can't be a null" % name,
                             "%s cannot be empty." % name,
                             "%s can't be a empty" % name,
                             "%s is expected to be not null" % name,
                             "%s is required to be not null" % name,
                             "%s is expected to be not empty" % name,
                             "%s is required to be not empty" % name,
                             "%s should have a expired indicator" % name,
                             "A business associate credit check has the source of the check",
                             "%s should have a lithology description." % name,
                             "%s must have a non-null loan number" % name,
                             "%s has some values." % name,
                             "%s cannot have any characters." % name,
                             "%s is always NOT NULL" % name,
                             "Lets say %s cannot have null values" % name,
                             "%s field cannot be blank or empty" % name,
                             "%s should contain something" % name,
                             "%s must be populated" % name,
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE not_equals to null"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "is_null":
            for i in range(0, 200):
                name = get_random_string(6)
                Sentences = ["%s can be null" % name,
                             "%s is null" % name,
                             "%s can be equal to null" % name,
                             "%s can be left empty" % name,
                             "%s canbe empty" % name,
                             "%s is empty" % name,
                             "%s can be equal to empty" % name,
                             "%s can be left blank" % name,
                             "%s canbe blank" % name,
                             "%s is blank" % name,
                             "%s can be equal to blank" % name,
                             "%s could be equal to blank" % name,
                             "%s must be blank" % name,
                             "%s must be empty" % name,
                             "%s must be null" % name,
                             "%s should be empty" % name,
                             "%s should be null" % name,
                             "%s should be blank" % name,
                             "%s could be empty" % name,
                             "%s could be null" % name,
                             "%s could be blank" % name,
                             "%s would be empty" % name,
                             "%s would be null" % name,
                             "%s would be blank" % name,
                             "%s is empty." % name,
                             "%s number should be null." % name,
                             "%s depth must be null" % name,
                             "%s is null." % name,
                             "%s could be null." % name,
                             "%s is a null" % name,
                             "%s must be null" % name,
                             "%s must be empty." % name,
                             "%s must be an empty string." % name,
                             "%s canbe null." % name,
                             "%s can be a null" % name,
                             "%s canbe empty." % name,
                             "%s can be a empty" % name,
                             "%s is expected to be null" % name,
                             "%s is required to be null" % name,
                             "%s is expected to be empty" % name,
                             "%s is required to be empty" % name,
                             "%s should not have a expired indicator" % name,
                             "%s should not have a lithology description." % name,
                             "%s must have a null loan number" % name,
                             "%s has not some values." % name,
                             "%s can not have any characters." % name,
                             "%s is always NULL" % name,
                             "Lets say %s have null values" % name,
                             "%s field can not be blank or empty" % name,
                             "%s should not contain something" % name,
                             "%s must not be populated" % name,
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE equals to null"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "is_date":
            for i in range(0, 200):
                name = get_random_string(6)
                Sentences = ["%s can have values of type DATE only" % name,
                             "%s can only be of type date" % name,
                             "%s consists of a DATE." % name,
                             "%s describes date." % name,
                             "%s is comprised of a DATE." % name,
                             "%s is equivalent to date" % name,
                             "%s represents a date." % name,
                             "%s represents a specific day, month and year." % name,
                             "%s shall be 'DATE'" % name,
                             "%s should contain the value of date" % name,
                             "%s is equal to the value of date" % name,
                             "%s may contain the value of date" % name,
                             "%s is of value date" % name,
                             "%s can only hold date data type" % name
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE is equal to DATE"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "is_not_date":
            for i in range(0, 200):
                name = get_random_string(6)
                Sentences = ["%s isn't a date" % name,
                             "%s is not a date" % name,
                             "%s must not be a date" % name,
                             "%s mustn't be date" % name,
                             "%s should not be date" % name,
                             "%s should not be of type date" % name,
                             "%s shouldn't be a date" % name,
                             "%s isn't of type date" % name,
                             "%s may not contain the value of date" % name
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE is not_equal to DATE"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "is_number":
            for i in range(0, 200):
                name = get_random_string(6)
                Sentences = ["%s must be of type integer" % name,
                             "%s should be of type integer" % name,
                             "%s must be a smallint" % name,
                             "%s is number" % name,
                             "%s must be of integer type" % name,
                             "%s must be a smallint" % name,
                             "%s Advances must be a whole number" % name,
                             "%s Before Modification must be an integer" % name,
                             "%s is number" % name,
                             "%s is a number" % name,
                             "%s should be a number" % name,
                             "%s is of type number" % name,
                             "%s must be of type number" % name,
                             "%s must be of a type number" % name,
                             "%s should be of type number" % name,
                             "%s should be of a type number" % name,
                             "%s needs to be of type number" % name,
                             "%s must be a smallint." % name,
                             "%s is a NUMBER" % name,
                             "%s is a type number" % name,
                             "The value of %s can only be number" % name,
                             "%s is a value which is numerical." % name,
                             "%s is always a number." % name,
                             "%s is comprised by a number" % name,
                             "%s must be numeric" % name,
                             "%s belongs to numeric" % name,
                             "%s is equal to numeric" % name,
                             "%s can be numeric values" % name,
                             "%s can have numerals" % name,
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE is equal to number"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
        elif usecase == "is_not_number":
            for i in range(0, 200):
                name = get_random_string(5)
                Sentences = ["%s isn't a number" % name,
                             "%s is not a number" % name,
                             "%s mustn't be a number" % name,
                             "%s should not be a number" % name,
                             "%s isn't of type number" % name,
                             "%s isn't of a type number" % name,
                             "%s is not of a type number" % name,
                             "%s must not be of type number" % name,
                             "%s should not be of a type number" % name,
                             "%s shouldn't be of type number" % name,
                             "%s is not of type integer" % name,
                             "%s shouldn't be of type number" % name,
                             "%s should not be of type number" % name,
                             "%s cannot contain numerals" % name,
                             "%s may not contain numeral" % name
                             ]
                for Sentence in Sentences:
                    UseCase = "VALUE is not_equal to number"
                    df1 = pd.DataFrame({"Sentences": [Sentence], "UseCase": [UseCase]})
                    if len(df.dropna()) == 0:
                        df = df1
                    df = df.append(df1, ignore_index=True)
    b_size_df = len(df)
    df.sort_values("Sentences", inplace=True)
    df.drop_duplicates(subset="Sentences", keep=False, inplace=True)
    df.to_csv("datasets/generated_training.csv", mode='w', index=False)
    a_size_df = len(df)
    print("before removing duplicate from df: %d and after removed duplicates size is : %d" % (b_size_df, a_size_df))
