import mysql.connector as ms


def insblob(path):
    with open(path, "rb") as file:
        bdata = file.read()
    return bdata



try:
    mydb = ms.connect(host="localhost", user="root", passwd="mysql@!@");
    cu = mydb.cursor()
    cu.execute("use rent")
    # cu.query("set global connect_timeout=6000")

    # cu.execute("create table imgs(id int(10) not null primary key, pic longblob not null)")
    print("Table created")
    path=input("Enter file path of the img:")

    bd=insblob(path)
    # print("bd=",bd)
    cu.execute("insert into img values(%s,%s)", (1,bd,))
    print("Insertion complete")
    mydb.commit()
    print("Trying to retrieve...")
    cu.execute("select * from img where id=%s",(1,))
    myres=cu.fetchone()[1]
    storefilepath="static\img{0}.jpg".format(str(bd))
    print("My Result:-",myres)
    with open(storefilepath,"wb") as f:
        f.write(myres);f.close()

    cu.close()


except Exception as e:print("Facing fking error:-",str(e))




