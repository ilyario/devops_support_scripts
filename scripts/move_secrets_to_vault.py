import base64
import hvac
import os

from kubernetes import client, config

env = "dev1"
namespace = 'apps-dev'
secret_names = [
#     . . . 
]

config.load_kube_config()
v1 = client.CoreV1Api()

clientVault = hvac.Client(
    url=os.environ['VAULT_ADDR'],
    token=os.environ['VAULT_TOKEN'],
)

for secret_name in secret_names:
    print('-----------------')
    print(secret_name)
    secret = v1.read_namespaced_secret(secret_name, namespace)
    vault_secrets = {}
    for key in secret.data:
        vault_secrets[key] = base64.b64decode(secret.data[key]).decode("utf-8")

    secret_name_parts = secret_name.split("-")

    if secret_name_parts[3] in ['dev', 'qa', 'test', 'prod', 'demo']:
        secret_name_subparts = secret_name_parts[3:-1]
    else:
        secret_name_subparts = secret_name_parts[2:-1]
        
    application_name = "-".join(s for s in secret_name_subparts)
    
    secret_path = f"titan/{env}/{application_name}/env-vars"
    read_response = clientVault.secrets.kv.v2.create_or_update_secret(
        path=secret_path,
        secret=vault_secrets,
    )
    print(read_response)
