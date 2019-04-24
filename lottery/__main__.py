import pysnooper
import requests
from bs4 import BeautifulSoup
from lottery.draws import Draws
from lottery.sqlalchemy_base import Session, engine, Base
from sqlalchemy import exc
from datetime import datetime
import re
import sys
Base.metadata.create_all(engine)

session = Session()


def insert_draw(date, newballs, luckystars):
    """
    Store historical draws in the database.

    This should be able to detect whether duplicate row is written.

    Date should be the primary key

    :return: True or False
    """

    draw = Draws(date, newballs[0], newballs[1], newballs[2], newballs[3], newballs[4], luckystars[0], luckystars[1])

    session.add(draw)

    try:
        session.commit()
        print("New record added - {0:s} {1:s} {2:s}.".format(str(date), str(newballs).strip('[]'),
                                                             str(luckystars).strip('[]')))
    except exc.IntegrityError as e:
        pattern = re.compile("pymysql.err.IntegrityError.*Duplicate entry.*")
        m = pattern.search(str(e))
        if m:
            print("New Draws has not been released yet, please try again later.\nExiting program .....")
            sys.exit()
    except:
        print("Unexpected error:", exc.SQLAlchemyError)
        raise
    finally:
        session.close()


def dump_lottery_hist():
    """
    Dump lottery historical data from https://www.euro-millions.com incrementally.

    Runs at 00:00 every Wednesday and Saturday.

    Data should be sent to database and Github.

    :return:
    """

    from dateutil.parser import parse

    current_year = datetime.now().year

    for i in range(current_year, 2003, -1):

        r = requests.get('https://www.euro-millions.com/results-archive-' + str(i))

        html_doc = r.text

        if r.status_code == 200:

            soup = BeautifulSoup(html_doc, 'html.parser')
            r_draws = soup.find_all("div", class_="archives")

            for r_draw in r_draws:
                r_date = r_draw.contents[1].contents[2]
                date = parse(r_date).date()

                current_date = datetime.today().date()

                if date <= current_date:
                    newballs = list(r_draw.contents[3].stripped_strings)[:5]
                    luckystars = list(r_draw.contents[3].stripped_strings)[5:]

                    insert_draw(date, newballs, luckystars)

        else:
            print("Connect to website failed, please check your network connectivity!")


def check_draw_existence(draw):
    """
    Returns True if draw appeared before.

    :return: True or False
    """
    q = session.query(Draws). \
        filter_by(newball1=draw[0][0],
                  newball2=draw[0][1],
                  newball3=draw[0][2],
                  newball4=draw[0][3],
                  newball5=draw[0][4],
                  luckystar1=draw[1][0],
                  luckystar2=draw[1][1]
                  )

    return q.count()


def generate_draw():
    """
    Generate a draw

    :return: [(new balls), (lucky stars)]
    """
    import random

    newballs = []
    luckystars = []
    draw = []


    while len(newballs) < 5:
        n = random.randint(1, 50)
        if n not in newballs:
            newballs.append(n)

    while len(luckystars) < 2:
        m = random.randint(1, 12)
        if m not in luckystars:
            luckystars.append(m)

    draw.append(newballs)
    draw.append(luckystars)

    return draw


def place_order():
    """
    Place an order in https://www.lottery.ie if no duplicate is found

    Print a message if order is placed successfully, by verifying the most recent order.

    :return: None
    """

    new_draw = generate_draw()

    while check_draw_existence(new_draw):
        new_draw = generate_draw()

    final_draw = new_draw

    newballs = str(sorted(final_draw[0])).strip('[]')
    luckystars = str(sorted(final_draw[1])).strip('[]')

    print("Newballs are {0:s}, Luckystars are {1:s}.".format(newballs, luckystars))


if __name__ == '__main__':
    place_order()
    # dump_lottery_hist()
