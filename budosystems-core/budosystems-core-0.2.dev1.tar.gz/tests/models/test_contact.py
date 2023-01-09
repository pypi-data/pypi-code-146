import pytest

from budosystems.models.contact import Contact, ContactList, Contactable, MissingContact

class TestContact:
    def test_missing_label(self):
        with pytest.raises(TypeError) as err:
            c = Contact(value="Value Only")
        assert err is not None

    def test_label_value(self):
        c = Contact(label="phone", value="123-123-1234")
        assert c.label == "phone"
        assert c.value == "123-123-1234"

class TestEmailAddress:
    def test_valid(self):
        pass

    def test_invalid(self):
        pass

class TestPhoneNumber:
    def test_valid(self):
        pass

    def test_invalid(self):
        pass

class TestPhysicalAddress:
    def test_(self):
        pass

class TestContactList:
    def test_setitem(self):
        pass

    def test_getitem(self):
        pass

    def test_iter(self):
        pass
