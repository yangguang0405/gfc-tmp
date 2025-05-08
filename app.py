
from server import Server;
from data.db import DB;

class App:
   def __init__(self) -> None:
      self._db = DB();
      self._server = Server(self._db);

   def run(self):
      self._db.connect();
      self._server.run();