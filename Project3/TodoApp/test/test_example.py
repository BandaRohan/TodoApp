import pytest


def test_equal_or_not_equal():
    assert 3==3


def test_is_instance():
    assert isinstance("thios is str", str)
    assert not isinstance('10',int)

def test_bool():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False

def test_type():
    assert type('HEllo' is str)
    assert type('World' is not str)

def test_value():
    assert 7>3
    assert 4<10

def test_list():
    lst = [1,2,3,4,5]
    lst2 = [False,False]
    assert 1 in lst
    assert 7 not in lst
    assert all(lst)
    assert not any(lst2)

class Student:
    def __init__(self, first_name: str,last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

def test():
    p = Student('Rohan','Banda',"IT",3)
    assert p.first_name == 'Rohan', 'First name should be Rohan'
    assert p.last_name == 'Banda', 'Last name should be Banda'
    assert p.major == 'IT'
    assert p.years == 3

@pytest.fixture
def default_employee():
    return Student("Rohan","Banda",'IT',3)