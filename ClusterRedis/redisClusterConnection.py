from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "127.0.0.1", "port": "7001"}, {"host": "127.0.0.1", "port": "7002"}]
redisCluster = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

redisCluster.set("foo", "bar")

foo = redisCluster.get("foo")

print(f'result {foo}')

redisCluster.set("usuario", "Viernes")

usuario = redisCluster.get("usuario")

print(f'result {usuario}')

