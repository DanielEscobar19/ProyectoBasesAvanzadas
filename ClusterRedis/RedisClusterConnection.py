from rediscluster import RedisCluster
import redis
import time
import os

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
redisCluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

## probamos que se pueda insertar y leer en el cluster
redisCluster.hset(f'user_1', mapping={'name': 'Gerardo', 'edad': 20})

print(f'Insertamos el usuario user_1 {redisCluster.hgetall("user_1")}')

## probamos apagar un nodo y leer del cluster luego
nodeConnection = redis.Redis(host='localhost', port=7005, decode_responses=True)
nodeConnection.shutdown()
print("\n-Apagamos el nodo2 del puerto 7005-\n")

print("\n-Esperamos 5 segundos-\n")
time.sleep(5)

print(f'Leemos desde el cluster los datos del usuario user_1 {redisCluster.hgetall("user_1")}')

## Insertamos un dato desde e nodo1 en el puerto 7000
print("Insertamos el usuario user_2 {'name': 'Maria', 'edad': 25}")
os.system("redis-cli -p 7000 -c hset user_2 name Maria edad 25") 

# leemos los datos desde el nodo4 en el puerto 7004
# result = os.system("redis-cli -p 7003 -c hgetall user_2") 
# print(result)
with os.popen("redis-cli -p 7003 -c hgetall user_2") as f:
    line = f.readlines()
    print("Leemos desde el nodo 7003 los datos del usuario user_2 {" + f"'{line[0][:-1]}': '{line[1][:-1]}', '{line[2][:-1]}': {line[3][:-1]}" + "}")
