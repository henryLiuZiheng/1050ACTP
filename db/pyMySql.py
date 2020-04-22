import pymysql


class MySqlDataBase:
    def __init__(self,IP,user,password,dbName):
        self.db = pymysql.connect(IP, user, password, dbName)
        self.cursor = self.db.cursor()
        print(2)
    def pyInsertDataToMysql(self,tableName, freq, OIP3):
        sql = 'INSERT INTO ' + tableName + ' values(' + str(freq) + ',' + str(OIP3) + ');'
        return sql
    def pyInsertDataToTestInfo(self,tableName, chipName):

        reCheckSql = 'delete from '+tableName+' where id in (select id from (select id from '+tableName+' where expect in (select expect from '+tableName+' group by expect having count(expect) > 1) and id not in (select min(id) from '+tableName+' group by expect having count(expect) > 1)) as tmpresult);'

        sql = 'INSERT INTO ' + tableName + ' values(' + str(chipName) + ');'
        self.cursor.execute(sql)
        self.cursor.execute(reCheckSql)
        return sql
    def pyInsertDataToTestTemp(self,tableName, chipName, testTemp):
        reCheckSql = 'delete from '+tableName+' where id in (select id from (select id from '+tableName+' where expect in (select expect from '+tableName+' group by expect having count(expect) > 1) and id not in (select min(id) from '+tableName+' group by expect having count(expect) > 1)) as tmpresult);'

        sql = 'INSERT INTO ' + tableName + ' values(' + str(chipName) + ',' + str(testTemp) + ');'
        self.cursor.execute(sql)
        self.cursor.execute(reCheckSql)
        return sql
    def pyInsertDataToTestType(self,tableName, chipName, testTemp, testType):
        maxIDsql = 'select max(id) from '+tableName+';'
        self.cursor.execute(maxIDsql)
        maxID = self.cursor.fetchall()
        intMaxID = str(maxID).replace('(','')
        intMaxID = intMaxID.replace(')','')
        intMaxID = intMaxID.replace(',','')
        intMaxID = int(intMaxID)
        tempID = intMaxID+1
        reCheckSql = "DELETE FROM myactp_testtype WHERE id NOT IN(SELECT id FROM(SELECT MIN(id) id FROM myactp_testtype GROUP BY `ttemp`,`ttype`,`tchipname`)cc);"

        sql = 'INSERT INTO ' + tableName + ' values('+str(tempID)+','+"'"+str(testTemp)+"'"+','+"'"+str(testType)+"'"+','+'0'+','+"'"+str(chipName)+"'"+');'
        print(sql)
        print(reCheckSql)

        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.execute(reCheckSql)
        self.db.commit()


        return sql
    def pyInsertDataToChipInfo(self,tableName, chipName, testTemp, testType, chipNum):
        print(tableName)
        print(chipName)
        print(testTemp)
        print(testType)

        print(chipNum)
        maxIDsql = 'select max(id) from '+tableName+';'
        print(maxIDsql)
        self.cursor.execute(maxIDsql)
        maxID = self.cursor.fetchall()
        print(maxID)
        intMaxID = str(maxID).replace('(','')
        intMaxID = intMaxID.replace(')','')
        intMaxID = intMaxID.replace(',','')
        intMaxID = int(intMaxID)
        tempID = intMaxID+1
        reCheckSql = "DELETE FROM myactp_chipinfo WHERE id NOT IN(SELECT id FROM(SELECT MIN(id) id FROM myactp_chipinfo GROUP BY `chipname`,`chiptemp`,`chiptype`,`cnum`)cc);"

        sql = 'INSERT INTO ' + tableName + ' values(' +str(tempID)+ ',' + str(chipNum)+ ','+'0'+ ',' + "'"+str(chipName)+"'" + ',' + "'"+str(testTemp)+"'" + ',' + "'"+str(testType)+"'" +');'
        print(sql)
        print(reCheckSql)
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.execute(reCheckSql)
        self.db.commit()
        self.db.close()


        return sql

    def upDataOriData(self,strTableName,freqData,resultData):
        myTable = '''
        create table ''' + strTableName + '''(
                FREQ float primary key not null,
                Figure float not null
            )
            '''
        checkTable = '''drop table if exists ''' + strTableName + ''';'''
        print(myTable)
        numCnt = 0

        try:
            self.cursor.execute(checkTable)
            self.cursor.execute(myTable)
            for testCondition in freqData:
                saveSql = self.pyInsertDataToMysql(strTableName, testCondition, resultData[numCnt])
                print(saveSql)
                self.cursor.execute(saveSql)

                numCnt = numCnt + 1
            #findSql = 'SELECT * FROM ' + strTableName + ';'
            #outPut = self.cursor.execute(findSql)
            #results = self.cursor.fetchall()

            #print(results)
            #self.cursor.close()
            self.db.commit()
        except Exception as err:
            self.cursor.rollback()
            raise err
        #finally:
        #    # 关闭数据库连接
            #self.db.close()




