import sys

from kubernetes import client, config
from kubernetes import utils

config.load_kube_config()
v1 = client.CoreV1Api()

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'

namespaces = v1.list_namespace()


for ns in namespaces.items:
    namespace = ns.metadata.name

    total_cpu_limits = 0
    total_memory_limits = 0

    pods = v1.list_namespaced_pod(namespace)

    for pod in pods.items:
        for container in pod.spec.containers:
            limits = container.resources.limits
            if limits:
                if 'cpu' in limits:
                    total_cpu_limits += int(float(utils.parse_quantity(limits['cpu'])))
                if 'memory' in limits:
                    total_memory_limits += int(float(utils.parse_quantity(limits['memory'])))

    print(f"{namespace} Total CPU limits: {total_cpu_limits}")
    print(f"{namespace} Total Memory limits (in bytes): {format_bytes(total_memory_limits)}")
