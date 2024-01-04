import streamlit as st
import pymysql 

# 전역변수 선언부
conn, cur = None, None
data1, data2, data3, data4 = '', '', '', ''
sql = ''

name = st.text_input('이름')
button = st.button('저장')

if button:
    conn = pymysql.connect(host='localhost', user='root', password='1111', db='test', charset='utf8')
    cur = conn.cursor()
    st.write(name)
    # cur.execute('INSERT INTO test VALUES(1, {0}'.format(name))
    cur.execute(f'INSERT INTO test VALUES(3, "{name}")')
    
    conn.commit()
    conn.close()
    
    st.write(':blue 저장되었습니다. :sparkles:')