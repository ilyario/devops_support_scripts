from kubernetes import client, config
from tabulate import tabulate
import sys

config.load_kube_config()

current_namespace = sys.argv[1]

apps_v1 = client.AppsV1Api()
deployments = apps_v1.list_namespaced_deployment(namespace=current_namespace)
data = []

for item in deployments.items:
    for container in item.spec.template.spec.containers:
        data.append([
            item.metadata.name,
            container.image.split(':')[0],
            container.image.split(':')[1]
        ])

print(tabulate(data, headers=['Application', 'Image', 'Tag']))
