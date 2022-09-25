import json
import keyword


class AttrSetter:
    """
    Basic class to convert dictionaries into class objects with attributes.
    Hierarchy of nested dictionaries can be accesed as class attributes.
    Example: {'value1':{'value2':1}} -> obj_name.value1.value2
    Note that keyword names are replaced with 'word_'.
    Example: {'class':'dog'} -> obj_name.class_
    """
    def __init__(self, dictionary: dict):
        for key in dictionary.keys():
            if type(dictionary[key]) is dict:
                self.__setattr__(key, AttrSetter(dictionary[key]))
            elif keyword.iskeyword(key):
                self.__setattr__(f'{key}_', dictionary[key])
            else:
                self.__setattr__(key, dictionary[key])


class ColorizeMixin:
    """
    Mixin to have a fancy colorful print(ClassName).
    To change the color set repr_color_code attribute to a desired number.
    Note that by default the __repr__ returns a single char | of chosen color.

    To implement ColorizeMixin in your class you should use the following code
    try:
        color_start, color_end = super().__repr__().split('|')
    except ValueError:
        color_start, color_end = '',''
    string = <string you want to print as __repr__>
    return color_start+string+color_end
    """
    repr_color_code = 33

    def __repr__(self):
        return f'\033[0;0{self.repr_color_code};40m|\033[0;037;40m'


class Advert(ColorizeMixin, AttrSetter):
    """
    Class to contain info from given dictionary.
    Note that your dict must contain title value, price >= 0.
    Price value may not be specified, in that case price=0.
    """

    def __init__(self, json_file: dict):
        super().__init__(json_file)
        if not hasattr(self, 'title'):
            raise AttributeError('Object must have a title')
        if not hasattr(self, 'price'):
            self.price = 0
        elif self.price < 0:
            raise ValueError('Price must be >= 0')

    def __repr__(self):
        try:
            color_start, color_end = super().__repr__().split('|')
        except ValueError:
            color_start, color_end = '', ''
        string = f'{self.title} | {self.price} ₽'
        return color_start+string+color_end


if __name__ == '__main__':
    print('TEST1')
    iphone_str = """{
    "title": "iPhone X",
    "price": 100,
    "location": {
    "address": "город Самара, улица Мориса Тореза, 50",
    "metro_stations": ["Спортивная", "Гагаринская"]
    }
    }"""
    iphone = json.loads(iphone_str)
    iphone_ad = Advert(iphone)
    print(iphone_ad)
    print(iphone_ad.price)
    print('')

    print('TEST2')
    corgi_str = """{
    "title": "Вельш-корги",
    "price": 1000,
    "class": "dogs",
    "location": {
    "address": "сельское поселение Ельдигинское, поселок санатория Тишково, 25"
    }
    }"""
    corgi = json.loads(corgi_str)
    corgi_ad = Advert(corgi)
    print(corgi_ad)
    print(corgi_ad.class_)
    print('')

    print('TEST3')
    lesson_str = """{
    "title": "python",
    "location": {
    "address": "город Москва, Лесная, 7",
    "metro_stations": ["Белорусская"]
    }
    }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    print(lesson_ad)
    print(lesson_ad.location.metro_stations)
