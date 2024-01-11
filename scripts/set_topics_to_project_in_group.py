import gitlab
import os
import sys

url = sys.argv[1] 
group_id = sys.argv[2]
topic = sys.argv[3]
private_token = os.environ['GITLAB_TOKEN']

gl = gitlab.Gitlab(url, private_token=private_token)

group = gl.groups.get(group_id)
projects = group.projects.list(sort='asc', include_subgroups=True, get_all=True)

print(f'gitlab {url} set to group "{group.name}" topics ["{topic}"]')

for project in projects:
    p = gl.projects.get(project.id)
    print(project.name)
    p.topics = [topic]
    p.save()