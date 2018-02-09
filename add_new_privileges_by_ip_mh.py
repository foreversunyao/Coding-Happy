import time, os
import re
import MySQLdb
import sys

def connect_db(ip):
    db = MySQLdb.connect(host = ip,
                         read_default_file='~/.my.cnf',
                         port = 3306,
                         db = 'mysql',
                         connect_timeout = 60)
    cur = db.cursor()
    return db, cur
v_user=str(sys.argv[1])
print v_user

(db, cur) = connect_db("metadb_ip")

eg_host = 'ip1'
new_host=['ip2',
'ip3']

sql = "select master_ip from master_info where product_name like 'db-A%'"
cur.execute(sql)
result = cur.fetchall()
cur.close()
db.close()


sql2 = "select concat('''',user,'''@',host) from mysql.user where  user='%s'  and host like '%s' " % (v_user,eg_host)

for ip in result:
    (dd, cc) = connect_db(ip[0])
    try:
        cc.execute(sql2)
        userexists=cc.fetchall()
        if userexists:
            for user in userexists:
                cc.execute('show grants for %s'% user) 
                grants = cc.fetchall()
                for grule in grants:
                    ## just grant privileges, no add user
			        if str(grule).find('IDENTIFIED') == -1:
                    		for nhost in new_host:
                        		newuser = grule[0].replace(eg_host, nhost)+';'
					try:
     				             	cc.execute(newuser) 
        		                    dd.commit()
						print ""
					except:
						continue
                				print ip, 'ok'
			else:
				continue
    except:
        priv = 'no'
	print("Unexpected error:", sys.exc_info()[0])

	
	
