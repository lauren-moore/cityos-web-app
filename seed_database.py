"""Script to seed database."""

import os
import json
import re

from model import db, connect_to_db
import server

os.system("dropdb videos")
os.system("createdb videos")

connect_to_db(server.app)
db.create_all()