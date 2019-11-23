import sqlite3

# define a class whose instances you want to store with sqlite
class Member(object):
    def __init__(self, first_name, last_name, fidelity_credit, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.fidelity_credit = fidelity_credit

        # set all passed kwargs
        for key, val in kwargs.items():
            self._init_kwargs[key] = val

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"  # f-strings work from python 3.6 on

    def __repr__(self):
        return "Member('{}', '{}')".format(self.first_name, self.last_name)

# create a database connection
# connection = sqlite3.connect("members.db")  # store the database in a file

connection = sqlite3.connect(":memory:")  # hold the database on RAM only 
# -> will be erased after stopping the program 
# -> good for simple testing

# create a cursor to work on the database
c = connection.cursor()

# create a table in the database
c.execute("""CREATE TABLE members (
                first_name text,
                last_name text,
                fidelity_credit integer
                )""")

# function to add elements to the database
def insert_member(m):
    with connection:  # usage of context manager -> no need to commit manually the execution
        c.execute("INSERT INTO members VALUES (:first_name, :last_name, :fidelity_credit)", 
        {'first_name': m.first_name, 'last_name': m.last_name, 'fidelity_credit': m.fidelity_credit})

# function to read from the database
    # read only one element for the given argument
def get_single_member_by_lastname(last_name):
    c.execute("SELECT * FROM members WHERE last_name=:last_name", {'last_name': last_name})
    return c.fetchone()

    # read all elements for the given argument
def get_members_by_lastname(last_name):
    c.execute("SELECT * FROM members WHERE last_name=:last_name", {'last_name': last_name})
    return c.fetchall()

# function to update a field for certain database entries: fidelity credit in this case
def update_fidelity_credit(m, fidelity_credit):
    with connection:
        c.execute("""UPDATE members SET fidelity_credit = :fidelity_credit
                  WHERE first_name = :first_name AND last_name = :last_name""",
                  {'first_name': m.first_name, 'last_name': m.last_name, 'fidelity_credit': fidelity_credit})

# function to erase elements from the database
def remove_member(m):
    with connection:
        c.execute("DELETE from members WHERE first_name = :first_name AND last_name = :last_name",
                  {'first_name': m.first_name, 'last_name': m.last_name})

memb1 = Member('Max', 'Martin', 45)
memb2 = Member('Anne', 'Martin', 200)

insert_member(memb1)
insert_member(memb2)

membs = get_members_by_lastname('Martin')
print(membs)

memb = get_single_member_by_lastname('Martin')
print(memb)

update_fidelity_credit(memb2, 230)
remove_member(memb1)
membs = get_members_by_lastname('Martin')
print(membs)

connection.close()