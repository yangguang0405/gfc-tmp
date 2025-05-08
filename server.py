
from data.db import DB;
from flask import Flask;
from view.task_view import TaskView;

app = Flask(__name__)


class Server:
     def __init__(self, db: DB) -> None:
          self.db = db;
          TaskView.register(app, route_base = '/task', init_argument=db);

     def run(self):
          app.run(host='0.0.0.0', port=8080, debug=False);

   