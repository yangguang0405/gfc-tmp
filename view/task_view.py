
from flask import Flask;
from flask import request;
from data.db import DB;
from view.base_view import BaseView;
from flask_classful import FlaskView,route;


class TaskView(BaseView):

    def __init__(self, db: DB) -> None:
       BaseView.__init__(self, db);
       

    @route('/crawled_type/list', methods=['GET'])
    def get_crawled_types(self):
      types = self.db.get_all_crawled_types();
      return types;


    @route('/crawled_type', methods=['POST'])
    def create_crawled_type(self):
      body = self.get_body();
      self.db.create_crawled_type(body);
      return self.created();


    @route('/crawled_city/list', methods=['GET'])
    def get_crawled_cities(self):
      types = self.db.get_all_crawled_cities();
      return types;


    @route('/crawled_city', methods=['POST'])
    def create_crawled_city(self):
      body = self.get_body();
      self.db.create_crawled_city(body);
      return self.created();


    @route('/crawled_spot/list', methods=['GET'])
    def get_crawled_spots(self):
      spots = self.db.get_all_crawled_spots();
      return spots;


    @route('/crawled_spot', methods=['POST'])
    def create_crawled_spot(self):
      body = self.get_body();
      self.db.create_crawled_spot(body);
      return self.created();


    @route('/crawled_post/list', methods=['GET'])
    def get_crawled_posts(self):
      posts = self.db.get_all_crawled_posts();
      return posts;


    @route('/crawled_post', methods=['POST'])
    def create_crawled_post(self):
      body = self.get_body();
      self.db.create_crawled_post(body);
      return self.created();


    @route('/crawled_image', methods=['POST'])
    def create_crawled_image(self):
      body = self.get_body();
      self.db.create_post_image(body.get('file'), body.get('city'), body.get('time'));
      return self.created();