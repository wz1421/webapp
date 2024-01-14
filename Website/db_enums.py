import enum

# Importing the 'enum' module to create enumerations
class Gender(enum.Enum):
    male = 0
    female = 1

    def __str__(self):
        return '%s' % self.name

class BabyCategory(enum.Enum):
    premature = 0
    diabetic_mother = 1
    small = 2

    def __str__(self):
        return '%s' % self.name

class UserCategory(enum.Enum):
    doctor = 0
    nurse = 1
    researcher = 2
    admin = 3

    def __str__(self):
        return '%s' % self.name