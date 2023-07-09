import redis
import json
import os

class RedisServer:
    def __init__(self):
        self.redisDatabase = None
    
    def startServer(self):
        self.redisDatabase = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def stopServer(self):
        self.redisDatabase.shutdown()

    def restartServer(self):
        print("\n--Servidor redis reiniciado--\n")
        os.system('systemctl restart redis.service')

    def takeSnapshot(self):
        print("\n--Snapshot guardado correctamente--\n")
        self.redisDatabase.save()

    def deleteSnapshots(self):
        os.system('sudo rm /var/lib/redis/dump.rdb')

database = RedisServer()
database.startServer()

id = 0

print("\n\n## Caso donde no hay persistencia en la base")

## caso donde no hay persistencia en la base
# creamos un usuario que contiene una lista de productos
productos =[{'name': 'arroz'}, {'name': 'carne'}]
database.redisDatabase.hset(f'user_{id+1}', mapping={'id': id+1, 'name': 'Carlos', 'products': json.dumps(productos)})
print(f"Se inserto el user_1 con los datos: {database.redisDatabase.hgetall(f'user_{id+1}')}")

# reiniciamos el server
database.restartServer()

# buscamos el usuario
# en este primer caso vemos que se pierden los datos
print(f"Datos del usuario user_{id+1},: {database.redisDatabase.hgetall(f'user_{id+1}')}") 

print("\n\n## Caso donde tomamos un snapshot de la base")

id = id+1
## caso donde si tomamos un snapshot de la base y no se pierden los datos
# creamos un usuario que contiene una lista de productos
productos =[{'name': 'arroz'}, {'name': 'carne'}]
database.redisDatabase.hset(f'user_{id+1}', mapping={'id': id+1, 'name': 'Gerardo', 'products': json.dumps(productos)})
print(f"Se inserto el user_2 con los datos: {database.redisDatabase.hgetall(f'user_{id+1}')}")

# tomamos un snapshot de la base de datos
database.takeSnapshot()

# reiniciamos el server
database.restartServer()

# buscamos el usuario
# en este primer caso vemos que se pierden los datos
print(f"Datos del usuario user_{id+1}: {database.redisDatabase.hgetall(f'user_{id+1}')}")

## caso donde se actualiza un dato y no se toma un snapshot
# creamos un usuario que contiene una lista de productos

print(f"\n\n## Caso donde actualizamos los datos del usuario: user_{id+1}")

# agregamos un producto al usuario
productos =[{'name': 'arroz'}, {'name': 'carne'}, {'name': 'leche'}]

# se lo insertamos al usuario
database.redisDatabase.hset(f'user_{id+1}', mapping={'products': json.dumps(productos)})
print(f"Datos atualizados del usuario user_{id+1}: {database.redisDatabase.hgetall(f'user_{id+1}')}")


# reiniciamos el server
database.restartServer()

# buscamos el usuario
# en este primer caso vemos que se pierden los datos
print(f"Datos del usuario user_{id+1}: {database.redisDatabase.hgetall(f'user_{id+1}')}")
print(f"Los datos se perdieron porque el snapshot se realizo antes de la actualizacion de los datos")

lista = database.redisDatabase.hget(f'user_2', 'products')
