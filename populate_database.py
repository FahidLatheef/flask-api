tb1 = [
    ["Drew", "Barrymore", 37],
    ["Brad", "Horet", 38],
    ["Tim", "Howard", 47],
    ["Ravi", "Kumar", 48],
    ["Brock", "Taward", 50],
    ["Logan", "Paul", 57],
    ["Girija", "Drey", 67],
    ["String", "Barry", 77],
    ["Tru", "Stingman", 87],
    ["Bare", "Leeward", 97],
    ["Warren", "Buffer", 101],
    ["Ram", "Teja", 111],
    ["Tinker", "Bell", 113],
    ["Rorren", "Tuffer", 115],
    ["Garry", "Kasparob", 117],
    ["Wern", "Tofer", 119],
    ["Gret", "Stoner", 121],
    ["Sting", "Supara", 131],
    ["Jaya", "Lakshmi", 142],
]

secret_code = int(input())

# tb1
if secret_code == 109812121:
    from app import db, TABLE1
    for line in tb1:
        db.session.add(TABLE1(fname=line[0], lname=line[1], real_id=line[2]))
    db.session.commit()

tb2 = [['Tinker', 'Bell', 113],
['Logan', 'Paul', 57],
['Sting', 'Supara', 131],
['Tim', 'Howard', 47],
['String', 'Barry', 77],
['Ram', 'Teja', 111],
['Girija', 'Drey', 67],
['Rorren', 'Tuffer', 115],
['Tru', 'Stingman', 87],
['Ravi', 'Kumar', 48],
['Brad', 'Horet', 38],
['Brock', 'Taward', 50],
['Jaya', 'Lakshmi', 142],
['Warren', 'Buffer', 101],
['Gret', 'Stoner', 121],
['Drew', 'Barrymore', 37],
['Bare', 'Leeward', 97],
['Wern', 'Tofer', 119],
['Garry', 'Kasparob', 117]]

# tb2
if secret_code == 10991922:
    from app import db, TABLE2
    import random
    for line in tb2:
        db.session.add(TABLE2(fname=line[0], lname=line[1], customer_no=line[2], offer=1000*random.randint(50, 250)))
    db.session.commit()
