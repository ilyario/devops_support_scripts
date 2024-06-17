import gitlab
import logging
from typing import Dict

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    gitlab_url: str = Field(env='GITLAB_URL')
    gitlab_token: str = Field(env='GITLAB_TOKEN')
    topic_gitlab_group_id_mapping: Dict = Field(env='TOPIC_GITLAB_GROUP_ID_MAPPING')


def main():
  settings = Settings()
  gl = gitlab.Gitlab(settings.gitlab_url, private_token=settings.gitlab_token)
  logger = logging.getLogger(__name__)

  for topic, gitlab_group_id in settings.topic_gitlab_group_id_mapping.items():
      group = gl.groups.get(gitlab_group_id)
      projects = group.projects.list(sort='asc', include_subgroups=True, get_all=True)

      logger.info(f'gitlab {settings.gitlab_url} set to group "{group.name}" topics ["{topic}"]')

      for project in projects:
          gl_project = gl.projects.get(project.id)
          logger.info(project.name)
          gl_project.topics = [topic]
          gl_project.save()


if __name__ == '__main__':
    main()
