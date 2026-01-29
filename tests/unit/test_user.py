import pytest
from src.user import User

def test_create_valid_user():
    u = User( "jan@test.pl", 20, "PL")
    assert u.email == "jan@test.pl"
    assert u.age == 20
    assert u.region == "PL"
    assert u.is_premium is False

def test_create_user_underage():
    u = User( "jan@test.pl", 17)
    assert u.email == "invalid"

def test_create_user_bad_email():
    u = User("jantest.pl", 25)
    assert u.email == "invalid"

def test_premium_toggle():
    u = User("jan@test.pl", 30)
    assert u.is_premium is False
    
    u.toggle_premium()
    assert u.is_premium is True
    
    u.toggle_premium()
    assert u.is_premium is False