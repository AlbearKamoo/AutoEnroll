class Course:
    def __init__(self, course_codes: ['str']):
        self.lecture_code = course_codes[0]
        self.auxiliary_codes = course_codes[1:]

    def get_course_as_list(self):
        return [self.lecture_code] + self.auxiliary_codes

    def __str__(self):
        return str(self.get_course_as_list())
    
    def __setattr__(self, name, value):
        assert name == "lecture_code" or name == "auxiliary_codes" ,"Attributes can only be set from __init__() method."
        assert 'lecture_code' not in self.__dict__ or 'auxiliary_codes' not in self.__dict__ ,"Attributes cannot be overwritten"
        self.__dict__[name] = value


