from data.db import DB;
from flask_classful import FlaskView,route;
from flask import request;
import logging;
logger = logging.getLogger(__name__);



class BaseView(FlaskView):

    def __init__(self, db: DB) -> None:
       self.db = db;

    def pagination_params(self):
        page = request.args.get('page');
        page_size = request.args.get('page_size');
        if page is None:
            page = 1;
        else:
            page = int(page);
        if page_size is None:
            page_size = 100;
        else:
            page_size = int(page_size);
        return page, page_size;

    def get_param(self, param):
        return request.args.get(param);

    def get_list_param(self, param):
        return request.args.getlist(param);

    def get_body(self):
        return request.get_json();

    def bad_request(self, msg, code=1):
        return {"code": code, "msg": msg}, 400;
    
    def not_found(self, msg, code=1):
        return {"code": code, "msg": msg}, 404;

    def error(self, msg, code=1):
        return {"code": code, "msg": msg}, 500;

    def success(self, data):
        return {"code": 0, "msg": "success", "data": data};


    def created(self):
        return {"code": 0, "msg": "success"};