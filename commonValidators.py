import numbers
from urllib.parse import urlparse

import numpy as np
import validators

from commonUtils import maybe_convert_bytes_to_string


class CommonValidators(object):
    EMPTY_STRING = ""
    EMPTY_NUMBER = 0
    EMPTY_BYTES = b""

    def __init__(self):
        raise RuntimeError(
            "This class should not be instantiated; call it instead as follows: CommonValidators.is_empty(variable)"
        )

    @classmethod
    def is_empty(cls, variable):
        if cls.is_none_or_undefined(variable):
            return True
        if cls.is_string(variable):
            return cls.is_empty_string(variable)
        if cls.is_number(variable):
            return cls.is_empty_number(variable)
        if cls.is_bytes(variable):
            return cls.is_empty_bytes(variable)
        if cls.is_list(variable):
            return cls.is_empty_list(variable)
        if cls.is_dict(variable):
            return cls.is_empty_dict(variable)
        if cls.is_set(variable):
            return cls.is_empty_set(variable)
        if cls.is_numpy_array(variable):
            return cls.is_empty_numpy_array(variable)
        return False

    @classmethod
    def is_none(cls, variable):
        return variable is None

    @classmethod
    def is_undefined(cls, variable):
        try:
            variable
            return False
        except NameError:
            return True

    @classmethod
    def is_none_or_undefined(cls, variable):
        if cls.is_undefined(variable):
            return True
        return cls.is_none(variable)

    @classmethod
    def is_local_variable_name(cls, variable_name: str):
        if not cls.is_string(variable_name):
            return False
        if variable_name in locals():
            return True
        return False

    @classmethod
    def is_global_variable_name(cls, variable_name: str):
        if not cls.is_string(variable_name):
            return False
        if variable_name in globals():
            return True
        return False

    @classmethod
    def variable_name_exists(cls, variable_name: str):
        return cls.is_local_variable_name(variable_name) or cls.is_global_variable_name(
            variable_name
        )

    @classmethod
    def is_list(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, list):
            return True
        return False

    @classmethod
    def is_empty_list(cls, variable):
        if not cls.is_list(variable):
            return False
        return len(variable) == 0

    @classmethod
    def is_non_empty_list(cls, variable):
        if not cls.is_list(variable):
            return False
        return len(variable) > 0

    @classmethod
    def is_tuple(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, tuple):
            return True
        return False

    @classmethod
    def is_empty_tuple(cls, variable):
        if not cls.is_tuple(variable):
            return False
        return len(variable) == 0

    @classmethod
    def is_non_empty_tuple(cls, variable):
        if not cls.is_tuple(variable):
            return False
        return len(variable) > 0

    @classmethod
    def is_dict(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, dict):
            return True
        return False

    @classmethod
    def is_empty_dict(cls, variable):
        if not cls.is_dict(variable):
            return False
        return len(variable) == 0

    @classmethod
    def is_non_empty_dict(cls, variable):
        if not cls.is_dict(variable):
            return False
        return len(variable) > 0

    @classmethod
    def is_non_empty_dict_and_has_key(cls, variable, key_name: str):
        if cls.is_non_empty_dict(variable):
            return key_name in variable
        return False

    @classmethod
    def get_key_value_from_dict_or_return_default_on_key_not_found(
            cls, dictionary, key_name, default_value=None
    ):
        if cls.is_non_empty_dict_and_has_key(dictionary, key_name):
            return dictionary[key_name]
        return default_value

    @classmethod
    def is_set(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, set):
            return True
        return False

    @classmethod
    def is_empty_set(cls, variable):
        if not cls.is_set(variable):
            return False
        return len(variable) == 0

    @classmethod
    def is_non_empty_set(cls, variable):
        if not cls.is_set(variable):
            return False
        return len(variable) > 0

    @classmethod
    def is_number(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, numbers.Number):
            return True
        return False

    @classmethod
    def is_empty_number(cls, variable):
        if not cls.is_number(variable):
            return False
        return variable == 0

    @classmethod
    def is_non_empty_number(cls, variable):
        if not cls.is_number(variable):
            return False
        return variable != 0

    @classmethod
    def is_integer(cls, variable):
        if cls.is_number(variable):
            return isinstance(variable, int)
        return False

    @classmethod
    def is_string(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, str):
            return True
        return False

    @classmethod
    def is_empty_string(cls, variable):
        if not cls.is_string(variable):
            return False
        return variable == cls.EMPTY_STRING

    @classmethod
    def is_non_empty_string(cls, variable):
        if not cls.is_string(variable):
            return False
        return variable != cls.EMPTY_STRING

    @classmethod
    def is_bytes(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, bytes):
            return True
        return False

    @classmethod
    def is_empty_bytes(cls, variable):
        if not cls.is_bytes(variable):
            return False
        return variable == cls.EMPTY_BYTES

    @classmethod
    def is_non_empty_bytes(cls, variable):
        if not cls.is_bytes(variable):
            return False
        return variable != cls.EMPTY_BYTES

    @classmethod
    def is_string_or_bytes(cls, variable):
        return cls.is_string(variable) or cls.is_bytes(variable)

    @classmethod
    def is_non_empty_string_or_bytes(cls, variable):
        return cls.is_non_empty_string(variable) or cls.is_non_empty_bytes(variable)

    @classmethod
    def is_numpy_array(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, np.ndarray):
            return True
        return False

    @classmethod
    def is_empty_numpy_array(cls, variable):
        if not cls.is_numpy_array(variable):
            return False
        return variable.size == 0

    @classmethod
    def is_non_empty_numpy_array(cls, variable):
        if not cls.is_numpy_array(variable):
            return False
        return variable.size > 0

    @classmethod
    def is_non_empty_object(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        if isinstance(variable, object):
            return True
        return False

    @classmethod
    def is_non_empty_object_and_has_attribute(cls, variable, attribute_name: str):
        if cls.is_non_empty_object(variable):
            return hasattr(variable, attribute_name)
        return False

    @classmethod
    def is_callable_method(cls, variable, return_false_for_class=False):
        if cls.is_none_or_undefined(variable):
            return False
        if return_false_for_class and cls.is_class(variable):
            return False
        try:
            if callable(variable):
                return True
            if cls.is_non_empty_object_and_has_attribute(variable, "__call__"):
                return True
        except Exception:
            pass
        return False

    @classmethod
    def is_class(cls, variable):
        if cls.is_none_or_undefined(variable):
            return False
        try:
            if isinstance(variable, type):
                return True
        except Exception:
            pass
        return False

    @classmethod
    def is_hexadecimal_string(cls, variable):
        if not cls.is_non_empty_string(variable) and not cls.is_non_empty_bytes(
                variable
        ):
            return False
        try:
            int(variable, 16)
            return True
        except ValueError:
            return False
        except TypeError:
            return False
        except Exception:
            return False

    @classmethod
    def is_url(cls, variable):
        if not cls.is_non_empty_string_or_bytes(variable):
            return False
        variable = maybe_convert_bytes_to_string(variable)
        try:
            result = urlparse(variable)
            return all([result.scheme, result.netloc])
        except Exception as e:
            print("Encountered error: ", str(e))
            return False

    @classmethod
    def is_relative_url(cls, variable):
        if not cls.is_non_empty_string_or_bytes(variable):
            return False
        variable = maybe_convert_bytes_to_string(variable)
        try:
            result = urlparse(variable)
            if cls.is_non_empty_object_and_has_attribute(
                    result, "scheme"
            ) and not cls.is_empty(result.scheme):
                return False
            if cls.is_non_empty_object_and_has_attribute(
                    result, "netloc"
            ) and not cls.is_empty(result.netloc):
                return False
            # Check if it's a valid path
            if cls.is_non_empty_object_and_has_attribute(
                    result, "path"
            ) and cls.is_non_empty_string_or_bytes(result.path):
                return True
        except Exception:
            pass
        return False

    @classmethod
    def is_email(cls, variable):
        if not cls.is_non_empty_string_or_bytes(variable):
            return False
        try:
            if cls.is_bytes(variable):
                variable = variable.decode("utf-8")
            result = validators.email(variable)
            if result:
                return True
        except Exception:
            pass
        return False

    @classmethod
    def is_primitive_type(cls, variable):
        return (
                cls.is_number(variable) or cls.is_string(variable) or cls.is_bytes(variable)
        )
