from kubernetes import client, config
import sys

current_namespace = sys.argv[1]
old_url = sys.argv[2]
new_url = sys.argv[3]

print(current_namespace, old_url, new_url)

config.load_kube_config()

v1 = client.NetworkingV1Api()
api_client = client.ApiClient()
ingresses = v1.list_namespaced_ingress(current_namespace)

template_server_snippet = """
location /metrics {{
    deny all;
}}
return 301 $scheme://{url}$request_uri;
"""

for item in ingresses.items:
    url = item.spec.rules[0].host.replace(old_url, new_url)

    item.metadata.annotations.update(
        {"nginx.ingress.kubernetes.io/server-snippet": f"{template_server_snippet.format(url=url)}"})

    try:
        v1.replace_namespaced_ingress(
            name=item.metadata.name,
            namespace=item.metadata.namespace,
            body=item
        )
        print(f"Аннотация обновлена для Ingress: {item.metadata.name} в пространстве имен {item.metadata.namespace}")
        print(item.metadata.annotations['nginx.ingress.kubernetes.io/server-snippet'])
        print('--------------------------')
    except client.exceptions.ApiException as e:
        print(f"Ошибка при обновлении Ingress {item.metadata.name} в пространстве имен {item.metadata.namespace}: {e}")

    host = item.spec.rules[0].host

    print("---------")
