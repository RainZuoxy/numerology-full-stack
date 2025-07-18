from enum import IntEnum


class Gender(IntEnum):
    MALE = 1
    FEMALE = 0

    @classmethod
    def get_gender_in_cn(cls, value: int) -> str:
        match value:
            case cls.MALE.value:
                return '男'
            case cls.FEMALE.value:
                return '女'
            case _:
                return 'invalid gender'
