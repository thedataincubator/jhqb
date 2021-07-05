c.JupyterHub.services = [
    {
        'name': 'questions',
        'url': 'http://127.0.0.1:8123',
        'command': ['flask', 'run', '--port=8123'],
        'environment': {'FLASK_APP': 'server/server.py'}
    }
]

c.JupyterHub.spawner_class = 'simple'
c.JupyterHub.authenticator_class = 'dummy'
c.JupyterHub.ip = '127.0.0.1'
