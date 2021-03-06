import pprint
from fabric.api import task, local
from node import Node


@task
def launch(name, ami='ami-762d491f', instance_type='m1.small', key_name='amazon2', 
           zone='us-east-1d', security_group='quicklaunch-1', user='ubuntu', job=None):
    """ Launch a node """
    node = Node(name=name, ami=ami, instance_type=instance_type, key_name=key_name, 
            zone=zone, security_group=security_group, user=user, job=job )
    node.launch()


@task
def mock_launch(name, ami='ami-3d4ff254', instance_type='t1.micro', key_name='amazon2', 
           zone='us-east-1d', security_group='quicklaunch-1', user='ubuntu', job=None):
    """ Simulate a node launch for dev purposes """
    node = Node(name=name, ami=ami, instance_type=instance_type, key_name=key_name, 
            zone=zone, security_group=security_group, user=user, job=job )
    node.mock_launch()

@task
def terminate(name):
    """ Terminate a node and remove from remote """
    node = Node.get_node(name)
    if node:
        node.terminate()
    else:
        print "Not found"

@task
def list():
    """ List configured nodes """
    for node in Node.get_all_nodes():
        print node.name, node.ip_address, node.jobs    

@task
def show(name):
    """ List configured nodes """
    node = Node.get_node(name)
    if node:
        pprint.pprint(node.to_dict()) 
    else:
        print "Not Found"


@task
def add_job(name, job):
    """ Give an existing node a job """
    node = Node.get_node(name)
    node.add_job(job)
    node.refresh_jobs()


@task
def update(name):
    """ Update node config """
    node = Node.get_node(name)    
    node.refresh_jobs()


@task
def ssh(name):
    """ Connect to a given node """
    node = Node.get_node(name)
    local("ssh %s@%s" % (node.user, node.ip_address))
