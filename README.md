# JupyterHub Question Board

This JupyterHub service provides a simple board for users to record
questions for an instructor.  It is designed to store questions to be
addressed in an office hour at the Data Incubator.  Users can submit
questions, vote for questions they're interested in, and close their
questions if they desire.  Admins can close (and reopen) any question.

## Requirements

The service consists of a two parts: a server component written in
[Flask](https://flask.palletsprojects.com/), and a client component
using [Svelte](https://svelte.dev/).  The server needs Python 3.7 or
newer to run.  The client needs node.js 10 or newer to build.

## Building

Run `make svelte` to build the client components.  This requires `npm`
to be available.  Run `make wheel` to build a Python wheel, which
includes both the server and client components.

## Running

The question board will run only as a JupyterHub service, as it relies
on JupyterHub for user information.  Additionally, it uses the
environmental variable `JHQB_STORE` to determine where it should persist
the question data.  If the variable is not set, `/tmp` will be used.

### Locally

This repo includes a sample `jupyterhub_config.py` files for running the
question board in a local JupyterHub deployment.  Questions will be
persisted in `jhqb_store` in the current directory.  It is expected that
you will have to adapt this configuration file for any purpose other
than testing.

### On Kubernetes

The question board can run as a [hub-managed
service](https://zero-to-jupyterhub.readthedocs.io/en/latest/administrator/services.html#hub-managed-services-in-z2jh)
on Kubernetes.  You will need to install it in your hub image.  Then add
to your `config.yaml` file.
```yaml
hub:
  services:
    questions:
      url: 'http://hub:8123'
      command: ['flask', 'run', '--host=0.0.0.0', '--port=8123']
      environment:
        FLASK_APP: jhqb
        JHQB_STORE: /srv/jupyterhub
```
You may also need to adjust your `networkPolicy` or `extraPorts` to
expose port 8123 properly.  See the
[example](https://zero-to-jupyterhub.readthedocs.io/en/latest/administrator/services.html#example-service)
for how to do that on up-to-date Zero-to-JupyterHub.

The `extraPorts` config will not work in Z2JH 0.10.*.  In this case,
edit the hub service by hand (`kubectl edit svc hub`).  At the bottom of the file, in `spec.ports`, add an entry
```yaml
- port: 8123
  protocol: TCP
  targetPort: 8123
  name: questions
```
You may also need to add a `name` to the existing listing for port 8081.
