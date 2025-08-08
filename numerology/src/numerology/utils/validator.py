from typing import Callable, Union


def validate_int_range(
        *,
        min_value: int, max_value: int,
        param: Union[str, None] = None,
        # class_:bool = False,
        error_msg: Union[str, None] = None
):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            validate_param = kwargs.get(param) or args[1]
            if param and not validate_param:
                raise ValueError(f"Can not find parameter name:'{param}'")
            if not (isinstance(min_value, int) and isinstance(max_value, int)):
                raise TypeError("Parameters: min_value, max_value are not integer")
            if not (min_value <= validate_param <= max_value):
                err_msg = f"parameter::index is out of validation({min_value}~{max_value})"
                if error_msg and isinstance(error_msg, str):
                    err_msg = f"{error_msg}\n{err_msg}"
                raise IndexError(err_msg)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def convert_index(index: int, divisor: int) -> int:
    index = index % divisor
    return divisor if index == 0 else index


def convert_tian_gan_index(index: int) -> int:
    return convert_index(index=index, divisor=10)


def convert_di_zhi_index(index: int) -> int:
    return convert_index(index=index, divisor=12)


def check_gender_with_yinyang(gender: int, yinyang: str) -> bool:
    return (gender == 1 and yinyang == "阳") or (gender == 0 and yinyang == "阴")