import enum

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

    def __str__(self):
        return '%s' % self.name