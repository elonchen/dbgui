#!/usr/bin/env python

import sys, os, time, uuid, sqlite3

# Store data for the DIBA bank

# Fields in no particular order

fields = ['lob',  'city', 'cname', 'zip', 'freetext', 'dob', 
        'country', 'numid', 'email2', 'county', 'phone', 'addr2',
        'comments', 'addr1', 'phone2', 'email', 'log', 'custid', 'cdate', 'udate' ]

# 'lob',  
# 'dob', 
#'city', 
#'cname', 
#'zip', 
#'freetext', 
#'country'
#'numid'
#'email2'
#'county'
#'phone'
#'addr2',
#'addr1'
#'comments'
#'phone2'
#'email'
#'log'
#'custid'
#'entryid'

# added by sql: p
    # 'pri' primary database key 
    # 'entryid' row id by the system

class dibasql():

    def __init__(self, file):
    
        try:
            self.conn = sqlite3.connect(file)
        except:
            print "Cannot open/create db:", file, sys.exc_info() 
            return            
        try:
            self.c = self.conn.cursor()
            
            # Create tables
            sqlstr = "create table if not exists clients \
                (pri INTEGER PRIMARY KEY, entryid string"
            for aa in fields:
                sqlstr += ", " + aa + " text"
            
            sqlstr +=  ")"
            
            #print "creation sql str: '" + sqlstr + "'"
            
            try:
                self.c.execute(sqlstr)
            except:
                print "Cannot initiate database", sys.exc_info()
                print "sql str: '" + sqlstr + "'"
                           
            '''self.c.execute("create table if not exists pos \
                       (pri INTEGER PRIMARY KEY, head text, xx integer, \
                            yy integer, ss integer)")
            self.c.execute("create index if not exists  ipos on pos (head)")            
            self.c.execute("create index if not exists  ppos on pos (pri)")'''
            
            # Save (commit) the changes
            self.c.execute("PRAGMA synchronous=OFF")
            self.conn.commit()            
        except:
            print "Cannot create sql tables", sys.exc_info() 
            print "sql str: '" + sqlstr + "'"
                 
        finally:    
            # We close the cursor, we are done with it
            #c.close()    
            pass
                            
    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   get(self, serial):
        #print "serial", serial
        ret = True; cnt = 0
        ddd = {}  
        try:      
            self.c.execute("select * from clients where custid == ?", (serial,))
            rr = self.c.fetchone()
            if rr == []:
                print "not found"
                return ddd
            else:
                
                for aa in self.c.description:
                    #print aa[0],
                    ddd[aa[0]] = rr[cnt]
                    cnt = cnt + 1
                return ddd
        except:
            print "Cannot get sql data", sys.exc_info()             
            print "sql str: '" + sqlstr + "'"
         
    # --------------------------------------------------------------------        
    # Return False if cannot rm data
    
    def   rm(self, serial):
        sqlstr = "delete from clients where custid == ?"
        try:      
            self.c.execute(sqlstr, (serial,))
            self.conn.commit()            
        except:
            print "Cannot delete sql data", sys.exc_info()             
            print "sql str: '" + sqlstr + "'", (serial,)
        
    # --------------------------------------------------------------------        
    # Return False if cannot put data
    
    def   put(self, datax):
    
        #got_clock = time.clock()         
        #print "datax", datax
        sqlstr = ""
        ret = True  
        try:      
            self.c.execute("select * from clients where custid == ?", (datax['custid'], ))
            rr = self.c.fetchall()
            if rr == []:
                entryid = uuid.uuid4()
                print "inserting", entryid
                sqlstr = "insert into clients (entryid, "
                for aa in datax:
                     sqlstr += aa + ", "
                # Erase last one    
                sqlstr = sqlstr[:-2]  
                sqlstr += ") values (?, "   # first value for rowid
                sqlstr += "?, " * len(datax)
                sqlstr = sqlstr[:-2]  
                sqlstr += ")"
                
                arr = []
                arr.append(str(entryid))
                for aa in datax:
                     strx = datax[aa]
                     arr.append(strx)
                
                #print "sql str", sqlstr, "arr", arr
                self.c.execute(sqlstr, arr)
            else:
                #print "updating"
                sqlstr = "update clients set "
                for aa in datax:
                     sqlstr += aa + " = '" + datax[aa] + "', "
                sqlstr = sqlstr[:-2]  
                sqlstr += " where custid = '" + datax['custid'] + "'" 
                #print "sql str:", sqlstr
                self.c.execute(sqlstr)
                
            self.conn.commit()          
        except:
            print "Cannot put sql data", sys.exc_info()             
            print "sqlstr", sqlstr
            ret = False  
        finally:
            #c.close     
            pass

        #self.take += time.clock() - got_clock        
          
        return ret
  
    # --------------------------------------------------------------------        
    # Get table names
    
    def   getnames(self):
    
        ss = "SELECT sql FROM sqlite_master WHERE type='table'"
        try:      
            self.c.execute(ss)
            rr = self.c.fetchall()
        except:
            print "getnames: Cannot get sql data", sys.exc_info() 
        finally:
            pass
        return rr
        
    # --------------------------------------------------------------------        
    # Get names
    
    def   getcustnames(self, cust = None):
        rr = []; ss = []; sqlstr = ""
        if cust:
            sqlstr = "select pri, cname, custid, comments, udate from clients where cname like '" + \
                    cust + "'"
        else:
           sqlstr = "select pri, cname, custid, comments, udate from clients order by udate desc  limit 100"
        try:      
            #print "sql", ccc
            self.c.execute(sqlstr)
            
            rr = self.c.fetchall()
        except:
            print "getcustnames: Cannot get sql data", sys.exc_info() 
            print "sql str: '" + sqlstr + "'"
            raise
        finally:
            pass
        return rr
    
    # --------------------------------------------------------------------        
    # Get All
    
    def   getall(self):
        rr = []; ss = []
        try:      
            self.c.execute("select * from clients")
            rr = self.c.fetchall()
            ss = self.c.description
        except:
            print "getall: Cannot get sql data", sys.exc_info() 
        finally:
            #c.close   
            pass
        return rr, ss
        
    # --------------------------------------------------------------------        
    # Return None if no data deleted
                                         
    def   rmall(self):
        try:      
            self.c.execute("drop table clients")
            #self.c.execute("delete from clients")
            rr = self.c.fetchone()
        except:
            print "rmall: Cannot delete sql data", sys.exc_info() 
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None

    # --------------------------------------------------------------------        
    # Return None if no data deleted

    def   rmone(self, kkk):
        try:      
            self.c.execute("delete from clients where head == ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print "rmone: Cannot delete sql data", sys.exc_info() 
        finally:
            #c.close   
            pass
        if rr:            
            return rr
        else:
            return None






























