#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
from mdds.lib.configMgr import config

DATABASE = config.DATABASE


class DBMgr:
    """
    database manager for record the result of the documents' check
    """
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE,check_same_thread= False)
        self.curs = self.conn.cursor()
        self.init_record_table()
        self.results = []
        
        
    def init_record_table(self):
        self.curs.execute(''' CREATE TABLE IF NOT EXISTS Records(
                                              filename text,
                                              filetype text,
                                              tag text,
                                              describe text,
                                              primary key(filename)); ''')
        self.conn.commit()
        
        
    def has_record(self, record):
        query = 'SELECT * FROM Records where filename = \"%s\";' %(record[0])
        self.conn.text_factory = str

        result = self.curs.execute(query)

        all = result.fetchall()
        if all != []:
            #print 'true'
            return True
        return False   
        
    def insert_record(self, record):
        if not self.has_record(record):
            query = 'INSERT INTO Records (filename, filetype, tag, describe)\
                     Values (\"%s\",  \"%s\", \"%s\",\"%s\");' %(record[0], record[1], record[2],record[3])
            self.curs.execute(query)
        self.conn.commit()
            
    def save_record(self, record):
        self.results.append(record)
        #if len(self.results) % 2 == 0:
        for i in self.results:
            self.insert_record(i)
        self.results = []
        
        
    def force_save_records(self):
        for record in self.results:
            self.insert_record(record)
        self.conn.commit()
        self.results = []


    def get_records(self):
        self.curs.execute(''' SELECT * FROM Records; ''')
        result = self.curs.fetchall()
        return result
        
        
    def clear_record_table(self):
        self.curs.execute(''' DELETE FROM Records; ''')
        self.conn.commit()
        
    
    def close(self):
        self.conn.close()
        