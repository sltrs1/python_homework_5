import sqlite3

# ======================================================

class ware:
    category = ""
    name = ""
    price = 0

    def __init__(self, category, name, price) -> None:
        self.category = category
        self.name = name
        self.price = price
    
    def getVatPrice(self):
        return self.price*1.2
    
    def getInfo(self):
        return str("Category: {}, Name: {}, Price: {}, VAT price: {:.2f}".format(self.category, self.name, self.price, self.getVatPrice()))
    
    def getCort(self):
        return (self.category, self.name, self.price)

class extraWare(ware):
    def __init__(self, category, name, price) -> None:
        super().__init__(category, name, price)
    
    def getVatPrice(self):
        return self.price*1.1

# ======================================================

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS goods(
   id INT,
   category TEXT
   name TEXT,
   price REAL);
""")
conn.commit()

# --------------------------------------------------

cur.execute("SELECT id FROM goods")
ids = cur.fetchall()

next_id = len(ids) + 1
print("Next id =", next_id)

cat = input("Enter Category: ")
nm = input("Enter Name: ")
while True:
    try:
        pr = int(input("Enter price: "))
    except ValueError:
        print("Wrong value")
    else:
        break

if cat == "food" or cat == "child":
    newWare = extraWare(cat, nm, pr)
else:
    newWare = ware(cat, nm, pr)

print("New ware is:", newWare.getInfo())

data_tuple = (next_id,) + newWare.getCort()

cur.execute("INSERT INTO goods VALUES (?, ?, ?, ?)", data_tuple)
conn.commit()

# --------------------------------------------------

cur.execute("SELECT * FROM goods")
all_goods = cur.fetchall()

all_list = []

for item in all_goods:
    if item[1] == "food" or item[1] == "child":
        all_list.append(extraWare(item[1], item[2], item[3]))
    else:
        all_list.append(ware(item[1], item[2], item[3]))

for w in all_list:
    print(w.getInfo())