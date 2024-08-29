import http.client

host = 'localhost'
port = 3000

client = http.client.HTTPConnection(host, port)

client.request('GET', '/saludo')

response = client.getresponse()

print(f'codigo de estado {response.status}')
print(f'Cuerpo de la respuesta: {response.read().decode("utf-8")}')

client.close()
