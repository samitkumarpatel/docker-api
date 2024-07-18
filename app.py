from flask import Flask, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/ping')
def ping():
    return jsonify({"message": "PONG"})

@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = client.nodes.list()
    nodes_info = []
    for node in nodes:
        nodes_info.append(node.attrs)
    return jsonify(nodes_info)

@app.route('/containers', methods=['GET'])
def get_containers():
    containers = client.containers.list(all=True)
    containers_info = []
    for container in containers:
        containers_info.append({
            'id': container.id,
            'name': container.name,
            'image': container.image.tags,
            'status': container.status,
            'labels': container.labels
        })

    return jsonify(containers_info)

@app.route('/containers/<node_id>', methods=['GET'])
def get_containers_by_node(node_id):
    containers = client.containers.list(all=True)
    containers_info = []
    for container in containers:
        print( f'container label for container {container.name} are : {container.labels}')
        if 'com.docker.swarm.node.id' in container.labels:
            if container.labels['com.docker.swarm.node.id'] == node_id:
                if container.status == 'running':
                    containers_info.append({
                        'id': container.id,
                        'name': container.name,
                        'image': container.image.tags,
                        'status': container.status,
                        'labels': container.labels
                    })
    return jsonify(containers_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
