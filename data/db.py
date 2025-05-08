import sqlite3
from typing import OrderedDict;
from model.spot_type import SpotType;
from model.spot import Spot;
from model.city import City;
from model.nearby_spot import NearbySpot;
from model.post import Post;
from model.post_image import PostImage;
import datetime;
import time;
import math;
import threading;
import logging;
import os;
logger = logging.getLogger(__name__);

class DB:
    def __init__(self):
        self._lock = threading.RLock()
    
    def connect(self):
        """Create a database connection to the SQLite database specified by db_file"""
        try:
            self._conn = sqlite3.connect('database.db', check_same_thread=False);
            self._conn.row_factory = sqlite3.Row;
            self._cursor = self._conn.cursor;
            logger.info("Connection to SQLite DB successful");
        
            # self._create_crawled_city_table();
            # self._create_crawled_type_table();
            # self._create_crawled_spot_table();
            # self._create_spot_distance_table();
            # self._create_crawled_post_table();
            # self._create_post_spot_table();
            # self._create_post_image_table();
        except sqlite3.Error as e:
            logger.error(f"The error '{e}' occurred")

    def _create_crawled_city_table(self):
        self._conn.execute("""CREATE TABLE crawled_city
                (name                   VARCHAR(20)    NOT NULL,
                time_completed                 INT    NOT NULL,
                        PRIMARY KEY (name));""");
        logging.info ("'crawled_city' table created successfully");
    
    def _create_crawled_type_table(self):
        self._conn.execute("""CREATE TABLE crawled_type
                (name                   VARCHAR(20)    NOT NULL,
                 city                   VARCHAR(20)    NOT NULL,
                 time_completed           INT    NOT NULL,
                        PRIMARY KEY (name, city));""");
        logging.info ("'crawled_type' table created successfully");
    
    def _create_crawled_spot_table(self):
        self._conn.execute("""CREATE TABLE crawled_spot
                (id                   VARCHAR(32)     NOT NULL,
                name                  VARCHAR(100)    NOT NULL,
                creator               VARCHAR(100)    NOT NULL,
                city                  VARCHAR(20)    NOT NULL,
                type                  VARCHAR(20)    NOT NULL,
                navigation            TEXT,
                instruction           TEXT,
                instruction_detail    TEXT,
                address               VARCHAR(512),
                browse_count          INT,
                nearby_completed      INT,
                time_created          INT,
                time_completed        INT    NOT NULL,
                deleted               INT    NOT NULL,
                        PRIMARY KEY (name,creator,city,type));""");
        logging.info ("'crawled_spot' table created successfully");
    

    def _create_spot_distance_table(self):
        self._conn.execute("""CREATE TABLE spot_distance
                (spot_id                   VARCHAR(32)     NOT NULL,
                other_spot_id               VARCHAR(32)    NOT NULL,
                distance               VARCHAR(100)    NOT NULL,
                        PRIMARY KEY (spot_id, other_spot_id));""");
        logging.info ("'spot_distance' table created successfully");
    

    def _create_crawled_post_table(self):
        #self._conn.execute("""DROP TABLE crawled_post;""");
        self._conn.execute("""CREATE TABLE crawled_post
                (id                   VARCHAR(32)     NOT NULL,
                title                 VARCHAR(100)    NOT NULL,
                description           TEXT,
                creator               VARCHAR(100)    NOT NULL,
                city                  VARCHAR(20)    NOT NULL,
                type                  VARCHAR(20)    NOT NULL,
                like_count            INT,
                collect_count         INT,
                comment_count         INT,
                share_count           INT,
                time_created          INT,
                time_crawl_started    INT    NOT NULL,
                time_crawl_completed  INT    NOT NULL,
                time_completed        INT    NOT NULL,
                deleted               INT    NOT NULL,
                is_portrait           INT    NOT NULL,
                        PRIMARY KEY (title, creator, city, type));""");
        logging.info ("'file' table created successfully");


    def _create_post_spot_table(self):
        self._conn.execute("""CREATE TABLE post_spot
                (post_id                   VARCHAR(32)     NOT NULL,
                spot_id                   VARCHAR(32)     NOT NULL,
                        PRIMARY KEY (post_id, spot_id));""");
        logging.info ("'spot_distance' table created successfully");
    

    def _create_post_image_table(self):
        #self._conn.execute("""DROP TABLE post_image;""");
        self._conn.execute("""CREATE TABLE post_image
                (post_id                   VARCHAR(32),
                file_name                  VARCHAR(100) PRIMARY KEY  NOT NULL,
                file_hash                  VARCHAR(32),
                city                       VARCHAR(20)    NOT NULL,
                is_portrait                INT,
                is_portrait_auto_processed                INT,
                is_portrait_manual_processed                INT,
                time_completed                     INT    NOT NULL);""");
        logging.info ("'post_image' table created successfully");
    
    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            logger.info("SQLite connection is closed")


    def get_all_crawled_cities(self) -> list:
        sql = "SELECT * FROM crawled_city order by time_completed";
        cur = self._conn.execute(sql);
        cities = [];
        for row in cur:
            city = City(row["name"]);
            cities.append(city);
        return cities;

    def get_all_crawled_types(self) -> list:
        sql = "SELECT * FROM crawled_type order by time_completed";
        cur = self._conn.execute(sql);
        types = [];
        for row in cur:
            type = SpotType(row["city"], row["name"]);
            types.append(type);
        return types;


    def get_all_crawled_spots(self) -> list:
        sql = "SELECT * FROM crawled_spot order by time_completed";
        cur = self._conn.execute(sql);
        spots = [];
        for row in cur:
            spot = Spot(row["id"], row["name"], row["creator"], row["city"], row["type"], nearby_completed=row["nearby_completed"]);
            spots.append(spot);
        return spots;

    def get_all_crawled_posts(self) -> list:
        sql = "SELECT * FROM crawled_post order by time_completed";
        cur = self._conn.execute(sql);
        posts = [];
        for row in cur:
            post = Post(row["id"], row["creator"], row["title"], row["city"], row["type"]);
            posts.append(post);
        return posts;


    def create_crawled_city(self, city: City) -> bool:
        with self._lock:
            now = datetime.datetime.now();
            try:
                sql = f"INSERT INTO crawled_city(name, time_completed) VALUES(?, ?)";
                cur = self._conn.execute(sql, (city.get("name"), math.floor(now.timestamp())));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                return False;
    
        return cur.rowcount != 0;

    def create_crawled_type(self, type: SpotType) -> bool:
        with self._lock:
            now = datetime.datetime.now();
            try:
                sql = f"INSERT INTO crawled_type(name, city, time_completed) VALUES(?, ?, ?)";
                cur = self._conn.execute(sql, (type.get("name"), type.get("city"), math.floor(now.timestamp())));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                return False;
        return cur.rowcount != 0;

    def create_crawled_spot(self, spot: Spot) -> bool:
        with self._lock:
            now = datetime.datetime.now();
            try:
                sql = f"INSERT INTO crawled_spot(id, name, creator, city, type, instruction,instruction_detail, address, navigation, browse_count, nearby_completed, time_created, time_completed, deleted) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
                self._conn.execute(sql, (spot.get("id"), spot.get("name"), spot.get("creator"), spot.get("city"), spot.get("type"), spot.get("instruction"), spot.get("instruction_detail"), spot.get("address"), spot.get("navigation"), 
                                            spot.get("browse_count"), spot.get("nearby_completed"), spot.get("time_created"), math.floor(now.timestamp()), 0));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                if (spot.get("nearby_completed") == 1):
                    sql = f"UPDATE crawled_spot SET nearby_completed=1 WHERE name=? AND name=? AND city=? AND type=?";
                    self._conn.execute(sql, (spot.get("name"), spot.get("creator"), spot.get("city"), spot.get("type"),));
                    self._conn.commit();
                
            for s in spot.get("spots"):
                s["spot_id"] = spot.get("id");
                self.create_spot_distance(s);
        return True;

    def create_spot_distance(self, spot: NearbySpot) -> bool:
        with self._lock:
            try:
                sql = f"INSERT INTO spot_distance(spot_id, other_spot_id, distance) VALUES(?, ?, ?)";
                cur = self._conn.execute(sql, (spot.get("spot_id"), spot.get("other_spot_id"), spot.get("distance")));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                return False;

        return True;

    def create_crawled_post(self, post: Post) -> bool:
        with self._lock:
            now = datetime.datetime.now();
            try:
                sql = f"INSERT INTO crawled_post(id, title, description, creator, city, type, like_count, collect_count, comment_count, share_count, time_created, time_crawl_started, time_crawl_completed, time_completed, is_portrait, deleted) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
                cur = self._conn.execute(sql, (post.get("id"), post.get("title"), post.get("description"), post.get("creator"), post.get("city"), post.get("type"), post.get("like_count"), post.get("collect_count"), post.get("comment_count"),
                                            post.get("share_count"), post.get("time_created"), post.get("time_crawl_started"), post.get("time_crawl_completed"), math.floor(now.timestamp()), 0, 0));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                pass

            for s in post.get("spots"):
                self.create_post_spot(post.get("id"), s);
        return True;

    def create_post_spot(self, post_id, spot_id) -> bool:
        with self._lock:
            try:
                sql = f"INSERT INTO post_spot(post_id, spot_id) VALUES(?, ?)";
                cur = self._conn.execute(sql, (post_id, spot_id));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                return False;
        return cur.rowcount != 0;


    def create_post_image(self, file_name, city, time) -> bool:
        with self._lock:
            try:
                sql = f"INSERT INTO post_image(file_name, city, time_completed) VALUES(?, ?, ?)";
                cur = self._conn.execute(sql, (file_name, city, time));
                self._conn.commit();
            except sqlite3.IntegrityError as e:
                return False;
        return cur.rowcount != 0;

    