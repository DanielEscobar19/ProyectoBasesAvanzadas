from rediscluster import RedisCluster
import redis
import time
import os

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
NOCOLOR = "\033[0m"

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]
redisCluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

## probamos que se pueda insertar y leer en el cluster
redisCluster.hset(f'user_1', mapping={'name': 'Gerardo', 'edad': 20})

print(f'{GREEN}Insertamos el usuario user_1:{NOCOLOR} {redisCluster.hgetall("user_1")}')

## probamos apagar un nodo y leer del cluster luego
nodeConnection = redis.Redis(host='localhost', port=7005, decode_responses=True)
nodeConnection.shutdown()
print(f"\n{RED}-Apagamos el nodo2 del puerto 7005-{NOCOLOR}\n")

print(f"\n{YELLOW}-Esperamos 5 segundos-\n{NOCOLOR}")
time.sleep(5)

print(f'Leemos desde el cluster los datos del usuario user_1: {redisCluster.hgetall("user_1")}\n')

## Insertamos un dato desde e nodo1 en el puerto 7000
print(f"{GREEN}Insertamos el usuario desdel el nodo1 del puerto 7000 user_2:{NOCOLOR} " + "{'name': 'Maria', 'edad': 25}")
os.system("redis-cli -p 7000 -c hset user_2 name Maria edad 25") 

# leemos los datos desde el nodo4 en el puerto 7004
# result = os.system("redis-cli -p 7003 -c hgetall user_2") 
# print(result)
with os.popen("redis-cli -p 7003 -c hgetall user_2") as f:
    line = f.readlines()
    print(f"Leemos desde el nodo4 7003 los datos del usuario user_2:" + f"'{line[0][:-1]}': '{line[1][:-1]}', '{line[2][:-1]}': {line[3][:-1]}" + "}")
