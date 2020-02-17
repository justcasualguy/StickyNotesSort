import sys
import sqlite3 as lite

class Record:
    word=""
    translation = ""
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
    def __str__(self):
        return str(self.word + "-" + self.translation)
    def __repr__(self):
        return self.word + "-" + self.translation



def findFirstOf(record,letter):
    i=0
    while(record[i]!=letter):
        i+=1
        if (i > len(record)-1):
            return -1
    return i

def ignoreId(item):
    return item[findFirstOf(item, ' ') + 1:len(item)]


dbPath = 'C:\\Users\\kubac\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite'
try:
    tablename = 'Note'
    con = lite.connect(dbPath)
    cur = con.cursor()

    noteId='AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0AHHJ0wHyifUi9ZChCujK5vAABiPgpQgAA'

    cur.execute("SELECT text from "+tablename+" where RemoteId = (?)",(noteId,))

    data = cur.fetchall()

    x=data[0][0]
    y=x.split('\n')

    records=[]

    for item in y:
         records.append(Record((ignoreId(item).split('-'))[0].lower(),(ignoreId(item).split('-'))[1].lower()))

    records.sort(key=lambda x: x.word)
    out=""

    for item in records:
        out+=str(item)+'\n'


    cur.execute("update Note set text = (?) where RemoteId = (?)",(out,noteId,))
    con.commit()


except lite.Error as e:

    print ("Error {}:".format(e.args[0]))

    sys.exit(1)

finally:
    if con:
        con.close()
    #print(data)