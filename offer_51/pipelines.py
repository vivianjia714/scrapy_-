# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb

class Offer51Pipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="localhost",user="root",passwd="123456",db="51db",charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
#        sql = """insert ignore into t_uk(title, school_url, IELTS_grade, hotmajor,Timerank,QSrank) values(%s, %s, %s, %s,%s,%s)"""
        sql = """insert ignore into t_nz(title,englishtitle,enmajorname,cnmajorname,majortype,degreetype,officalurl) values(%s, %s, %s, %s,%s,%s,%s)"""
        param = (item['title'],item['englishtitle'], item['enmajorname'],item['cnmajorname'],item['majortype'],item['degreetype'],item['officalurl'])
        self.cursor.execute(sql,param)
        self.conn.commit()


#    def process_item(self, item, spider):
#        pass
    

    


    

    