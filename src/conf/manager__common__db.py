import os
from db_utils.modules.db import DbConfig


db_config = DbConfig(
    uri=os.environ['SERVICE__DB__DB_URI'],
    track_mod=False
)

SERVICE__DB__SYS_USER_ID = os.environ['SERVICE__DB__SYS_USER_ID']
