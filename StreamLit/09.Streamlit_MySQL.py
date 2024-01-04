import streamlit as st
import pymysql 

# 전역변수 선언부
conn, cur = None, None
data1, data2, data3, data4 = '', '', '', ''
row = None

# 메인 코드
conn = pymysql.connect(host='localhost', user='root', password='1111', db='world', charset='utf8')
cur = conn.cursor()
cur.execute('SELECT * FROM city')

while(True):
    row = cur.fetchone()
    if row == None:
        break

    st.write(row)
    
conn.close()