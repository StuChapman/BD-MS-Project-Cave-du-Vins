import re


# test password validation
def PasswordVal(passVal):

    SpecialSym = ['$', '@', '#', '%', '!']

    if len(passVal) < 6 and len(passVal) > 10 and not any(char.isdigit() for char in passVal) and not any(char.isupper() for char in passVal) and not any(char.islower() for char in passVal) and not any(char in SpecialSym for char in passVal):
        return False
    else:
        return True


# test wine_name validation
def WineNameVal(winename):

    if not re.match("^[a-zA-Z0-9* ]+$", winename):  # change to: "^[a-zA-Z0-9 ]+$"
        return True
    else:
        return False


# test wine_name validation
def WineNameVal_two(winename):

    if not re.match("^[a-zA-Z0-9* ]+$", winename):
        return True
    else:
        return False


def test_PasswordVal():
    passVal = "Admin1!"
    assert PasswordVal(passVal) == True


def test_WineNameVal():  # test failed
    winename = "*"
    assert WineNameVal(winename) == True


def test_WineNameVal_two():  # test passed
    winename = "&"
    assert WineNameVal(winename) == True