from Jestor import Jestor
from filter.Filter import Filter
from filter import Operators
import os

# Set environment variables
os.environ['host'] = 'vieira.api.local.jestor.com'
os.environ['host_local'] = 'main_api'

token = '2f7c1281e2a404c36f06261a4b422535'
jestor = Jestor(token, 'vieira')

#insert record in table
#result = jestora.table('oe').insert({'name': 'testando pelo sdk python'})
#print(result)

filters = [
    Filter('name', 'testando', Operators.CONTAINS, 'string'),
]

result = jestor.table('oe').get(filters)
print(result)
#get records of a table
headers = {
    'Authorization' : 'Bearer NjM5NGMyMmJjYWEyZWNidba62b9f80MTY2Nzg1MTY5MWQyODZh', 
    'Host': 'vieira.api.local.jestor.com',
    'Content-Type': 'application/json'
}

#result = jestor.curlCall(['http://main_api/v3/low-code-webhook', headers, None])
#print(result)
#arguments = []
#result = jestor.generatePDF(arguments=arguments)
#print(result)

## update a record
#result = jestor.table('teste_tag').update({'id_teste_tag': 53, 'name': 'test update'})
#print(result['data'])

#filters = [
#	Filter('description', 'dasd', Operators.CONTAINS, 'string'),
#]

#result = jestor.user().get(filters=filters,sort='name asc')
#print(result['data'])
#result = jestor.fetchTasks([None, 1])
#print(result['data'])

#files = jestor.file('table_teste', 7, 'apenas_teste')

#files.add({'name': 'assdads', 'content': '<content string>', 'contentType': 'pdf'})
#print(files.files)
#files.add({'name': 'assdads', 'content': '<content string>', 'contentType': 'pdf'})
#files.add({'name': 'assdadsadasdasdas', 'content': '<content string>', 'contentType': 'pdf'})

#print(files.files)

#files.update('E0DOdSKgvkkMncI8Fnhst-2', {'name': 'alterado', 'content': '<content string>', 'contentType': 'pdf'})

#jestor.table('table_teste').update(7, {'name': 'testando pelo sdk python update asd', 'apenas_teste': files.toJson()})
#print(result)