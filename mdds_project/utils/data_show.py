#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 This file is only a demo to show the records in sqlite3,
 it will write the malicious records into the MALFILE,
 and write the good records into the GOODFILE.
"""

import env
import sqlite3
import os

DATABASE = r'G:\mdds_project\mdds\database\database.db'
MALFILE = r'G:\mdds_project\mdds\malicious_records.txt'
GOODFILE = r'G:\mdds_project\mdds\good_records.txt'

class DBManager:
    """
    database manager for record the result of the documents' check
    """
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.conn.text_factory = str
        self.curs = self.conn.cursor()
        self.results = []
            
            
    def get_records(self):
        self.curs.execute(''' SELECT * FROM Records; ''')
        result = self.curs.fetchall()
        return result
        
        
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    dbma = DBManager()
    result = dbma.get_records()

    with open(MALFILE, 'w') as f:
        for record in result:
            if record[2] == 'True':
                f.write(record[1] + ': ' + record[0] + '  describe:'+ record[3]+'\n')
                print 'bad %s: %s' %(record[1], record[0])
                
    with open(GOODFILE, 'w') as f:
        for record in result:
            if record[2] == 'False':
                f.write(record[1] + ': ' + record[0] + '\n')
                print 'good %s: %s' %(record[1], record[0])