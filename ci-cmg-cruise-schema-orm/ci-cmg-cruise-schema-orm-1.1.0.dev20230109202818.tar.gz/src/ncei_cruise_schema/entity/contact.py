from ..orm.entity import Entity, Column

class Contact(Entity):

  @staticmethod
  def _table():
    return "people_and_sources"

  def __init__(
      self, 
      id=None,
      name=None,
      position=None,
      organization=None,
      street=None,
      city=None,
      state=None,
      zip=None,
      country=None,
      phone=None,
      email=None,
      orcid=None,
      docucomp_uuid=None
  ):
    self.__id=id
    self.__name=name
    self.__position=position
    self.__organization=organization
    self.__street=street
    self.__city=city
    self.__state=state
    self.__zip=zip
    self.__country=country
    self.__phone=phone
    self.__email=email
    self.__orcid=orcid
    self.__docucomp_uuid=docucomp_uuid


  @property
  def id(self):
    return self.__id

  @id.setter
  def id(self, value):
    self.__id = value

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, value):
    self.__name = value

  @property
  def position(self):
    return self.__position

  @position.setter
  def position(self, value):
    self.__position = value

  @property
  def organization(self):
    return self.__organization

  @organization.setter
  def organization(self, value):
    self.__organization = value

  @property
  def street(self):
    return self.__street

  @street.setter
  def street(self, value):
    self.__street = value

  @property
  def city(self):
    return self.__city

  @city.setter
  def city(self, value):
    self.__city = value

  @property
  def state(self):
    return self.__state

  @state.setter
  def state(self, value):
    self.__state = value

  @property
  def zip(self):
    return self.__zip

  @zip.setter
  def zip(self, value):
    self.__zip = value

  @property
  def country(self):
    return self.__country

  @country.setter
  def country(self, value):
    self.__country = value

  @property
  def phone(self):
    return self.__phone

  @phone.setter
  def phone(self, value):
    self.__phone = value

  @property
  def email(self):
    return self.__email

  @email.setter
  def email(self, value):
    self.__email = value

  @property
  def orcid(self):
    return self.__orcid

  @orcid.setter
  def orcid(self, value):
    self.__orcid = value

  @property
  def docucomp_uuid(self):
    if self.__docucomp_uuid:
      return self.__docucomp_uuid.lower()
    return self.__docucomp_uuid

  @docucomp_uuid.setter
  def docucomp_uuid(self, value):
    self.__docucomp_uuid = value

  @classmethod
  def _columns(cls):
    return (
      Column("contact_id", cls.id, id=True, sequence="people_sources_seq"),
      Column("name", cls.name),
      Column("position", cls.position),
      Column("organization", cls.organization),
      Column("street", cls.street),
      Column("city", cls.city),
      Column("state", cls.state),
      Column("zip", cls.zip),
      Column("country", cls.country),
      Column("phone", cls.phone),
      Column("email", cls.email),
      Column("orcid", cls.orcid),
      Column("docucomp_uuid", cls.docucomp_uuid)
    )



