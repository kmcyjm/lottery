# TODO: 统计当次newballs跟上次重复一个数字的占比，重复两个数字的占比，直到5个数字的占比。done
# TODO: 统计当次newballs跟前十次重复一个数字的占比，重复两个数字的占比，直到5个数字的占比。
# TODO: 统计当次luckystar跟前次重复一个数字的占比，重复两个数字的占比。

from lottery.sqlalchemy_base import Session, engine, Base
from lottery.draws import Draws

session = Session()

# get total number of records
total_records = session.query(Draws).count()

c = session.query(Draws).order_by(Draws.date.desc()).limit(total_records)

# make c a list
c = c[::]

match_one, match_two, match_three, match_four, match_five, match_lucky_one, match_lucky_two = 0, 0, 0, 0, 0, 0, 0

for i in range(0, len(c) - 1):

    match = 0
    match_lucky = 0
    current_newballs = []
    current_luckystars = []
    prev_newballs = []
    prev_luckystars = []

    current_newballs.append(c[i].newball1)
    current_newballs.append(c[i].newball2)
    current_newballs.append(c[i].newball3)
    current_newballs.append(c[i].newball4)
    current_newballs.append(c[i].newball5)

    current_luckystars.append(c[i].luckystar1)
    current_luckystars.append(c[i].luckystar2)

    prev_newballs.append(c[i + 1].newball1)
    prev_newballs.append(c[i + 1].newball2)
    prev_newballs.append(c[i + 1].newball3)
    prev_newballs.append(c[i + 1].newball4)
    prev_newballs.append(c[i + 1].newball5)

    prev_luckystars.append(c[i+1].luckystar1)
    prev_luckystars.append(c[i+1].luckystar2)

    # print("current_newballs: {}, prev_newballs: {}".format(current_newballs, prev_newballs))

    for j in current_newballs:
        if j in prev_newballs:
            match += 1

    for m in current_luckystars:
        if m in prev_luckystars:
            match_lucky += 1

    if match == 0:
        print("0 " * 5, '\n')
    elif match == 1:
        match_one += 1
        print("1 " + "0 " * 4, '\n')
    elif match == 2:
        match_two += 1
        print("1 " * 2 + "0 " * 3, '\n')
    elif match == 3:
        match_three += 1
        print("1 " * 3 + "0 " * 2, '\n')
    elif match == 4:
        match_four += 1
        print("1 " * 4 + "0 ", '\n')
    elif match == 5:
        match_five += 1
        print("1 " * 5, '\n')

    if match_lucky == 0:
        pass
    elif match_lucky == 1:
        match_lucky_one += 1
    elif match_lucky == 2:
        match_lucky_two += 1

print('The percentage of matching one number from previous draw is {}\n, two number is {}\n, three number is {}\n, '
      'four number is {}\n, five number is {}\n. Match only one lucky number is {}\n, two lucky number is {}'.format(
    (match_one / total_records) * 100, (match_two / total_records) * 100, (match_three / total_records) * 100,
    (match_four / total_records) * 100, (match_five / total_records) * 100, (match_lucky_one/total_records) * 100,
    (match_lucky_one/total_records) * 100))
