import sqlparse
import json

def parse_sql(raw):

    # i need table names, select column names and where json
    # Split a string containing two SQL statements:
    statements = sqlparse.split(raw)
    # print(statements)

    # Format the first statement and print it out:
    first = statements[0]
    # print(sqlparse.format(first, reindent=True, keyword_case='upper'))

    # Parsing a SQL statement:
    parsed = sqlparse.parse(first)[0]
    # print(parsed.tokens)
    counter=0
    # tokens_iter = iter(parsed.tokens)
    #TODO IMP NEED TO WRITE A BETTER STATE MACHINE
    STATE = 0
    IN_SELECT = 1
    IN_FROM = 2
    IN_WHERE = 3
    IN_LIMIT = 4

    table = ''
    column_list = []
    where_clause_dict = {}
    limit = -1
    for tok in parsed.tokens:
    # for tok in tokens_iter:
        counter =counter+1
        # print("counter="+str(counter))

        if tok.normalized == 'SELECT':
            STATE = IN_SELECT
        elif tok.normalized == 'FROM':
            STATE = IN_FROM
        elif tok.normalized == 'WHERE' or tok.normalized.startswith('where '):
            STATE = IN_WHERE
        elif tok.normalized == 'LIMIT' or tok.normalized.startswith('where '):
            STATE = IN_LIMIT
        # else:
        #     STATE = 0

        if STATE == IN_SELECT:
            if tok.is_group:
                #print("tok is SELECT group")
                #print(tok)
                for sub_tok in tok.tokens:
                    sub_tok.value = sub_tok.value.strip()
                    #re-check this 2 conditions below. it is very convoluted.
                    #a btter way is to check if they are not space and , and then add, we might not need this complication
                    #check when we have 1, 2,3+ columns
                    if sub_tok.is_group and sub_tok.ttype is None:
                        if not (sub_tok.value=='' or sub_tok.value==',') :
                            column_list.append(sub_tok.value)
                    elif not sub_tok.is_group:
                        if not (sub_tok.value=='' or sub_tok.value==',') :
                            column_list.append(sub_tok.value)
                    # else:
                    #     column_list.append(sub_tok.value)


            #elif tok.normalized == '*':
                #print("tok is SELECT *")
                #print(tok)
                # column_list.append("*")  # if * then no project so pass null to backend


        if STATE == IN_FROM:
            if tok.is_group:
                    #print("tok is FROM group")
                    #print(tok)
                    table = tok.value
                    #we support only 1 table fo r now get that and move to the beginning

        if STATE == IN_LIMIT:
            if (tok.value is not None or len(tok.value)>0)\
                    and tok.value.isnumeric():
                    limit = int(tok.value)

        if STATE == IN_WHERE:
            if tok.is_group:
                for sub_tok in tok.tokens:
                    #print("sub_token=" + str(sub_tok))
                    if sub_tok.normalized =='WHERE':
                        IN_WHERE_SUB_CLAUSE=True
                    if sub_tok.is_group:
                        #handle where clause
                        #print("sub_token||" + str(sub_tok))
                        #print("sub_token||" + str(sub_tok.value.replace('=',':')))
                        #strip quotes out
                        where_clause_dict[sub_tok.left.value] = sub_tok.right.value
                        for sub_sub_tok in sub_tok.tokens:
                            p=0
                            #print("sub_sub_tok=" + str(sub_sub_tok))
                            # pass

                STATE = 0

    where_clause_json_data = json.dumps(where_clause_dict)
    #print("+++++++++")
    output=[]
    output.append(table)
    output.append(column_list)
    output.append(where_clause_json_data)
    output.append(limit)
    #print(output)
    return output




def parse_nonsql(raw):

    #send it as is in the nativeSql portion of the queryrequestbody

    print("+++++++++")
    print(raw)

# [<DML 'select' at 0x7f22c5e15368>, <Whitespace ' ' at 0x7f22c5e153b0>, <Wildcard '*' … ]

raw1 = 'select name, address from foo where d=\'s\' and f=1 and t=\'fgsgdsyufg\' and name="ram"'
raw1 = 'select name, address from foo a, faa b where a.col21=b.col2 and d=\'s\' and f=1 and t=\'fgsgdsyufg\' and name="ram"'
raw1 = 'select name, address from foo a, faa b where a.col21=b.col2 and d=\'s\' and f in (\'abc\',\'def\',\'xyz\')  and t=\'fgsgdsyufg\' and name="ram"'
# raw1 = 'select name from foo where a.col21=b.col2 and d=\'s\' and f in (\'abc\',\'def\',\'xyz\')  and t=\'fgsgdsyufg\' and name="ram"'
# raw1 = 'select * from foo where a.col21=b.col2 and d=\'s\' and f in (\'abc\',\'def\',\'xyz\')  and t=\'fgsgdsyufg\' and name="ram"'
raw1 = 'select * from foo where a.col21=b.col2 and d=\'s\' and f in (\'abc\',\'def\',\'xyz\')  and t=\'fgsgdsyufg\' and name="ram" limit 10'
parse_sql(raw1)

