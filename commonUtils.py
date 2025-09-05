import base64
import hashlib
import imghdr
import math
import numbers
import os
import pickle
import random
import re
import struct
import time
import urllib
import uuid
from binascii import Error, unhexlify
from datetime import datetime

import cv2
import filetype
import numpy as np

import skymel_modelio_pb2


def is_number(value):
    """Checks if a value is a number (int, float, complex, etc.)."""
    return isinstance(value, numbers.Number)


def is_empty_string(value):
    return value is None or len(value) == 0


def make_topic_id(input_str):
    return "topic-" + input_str


def make_key_id(input_str):
    return "key-" + input_str


def load_image_from_url(image_url) -> None | np.ndarray:
    if not isinstance(image_url, str):
        return None
    try:
        request = urllib.request.urlopen(image_url)
        contents = np.asarray(bytearray(request.read()), dtype=np.uint8)
        image = cv2.imdecode(contents, cv2.IMREAD_UNCHANGED)
        return image
    except Exception as _:
        return None


def convert_to_bytes(input_str: bytes | str) -> bytes:
    if isinstance(input_str, str):
        return input_str.encode("utf8")
    return input_str


def convert_to_string(input_bytes: bytes | str) -> str:
    if isinstance(input_bytes, bytes):
        return input_bytes.decode("utf8")
    return input_bytes


def clean_base64_string(input_base64_str: str) -> str:
    input_base64_str = convert_to_string(input_base64_str)
    return re.sub("^data:image/.+;base64,", "", input_base64_str)


def load_image_from_base64_string(
        input_base64_str: bytes | str, check_image_header: bool = False
) -> None | np.ndarray:
    try:
        input_base64_str = clean_base64_string(input_base64_str)
        input_base64_str = convert_to_bytes(input_base64_str)
        image_bytes = base64.b64decode(input_base64_str)
    except Error as _:
        return None
    if check_image_header:
        extension = imghdr.what(None, h=image_bytes)
        if not extension or extension == "":
            return None
    try:
        numpy_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        return image
    except Exception as _:
        return None


def load_image_from_byte_string(
        image_bytes: bytes, check_image_header: bool = False
) -> None | np.ndarray:
    if check_image_header:
        extension = imghdr.what(None, h=image_bytes)
        if not extension or extension == "":
            return None
    try:
        numpy_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        return image
    except Exception as _:
        return None


def load_image_from_image_proto(
        image_proto: skymel_modelio_pb2.Image,
) -> None | np.ndarray:
    if image_proto is None or type(image_proto) is not skymel_modelio_pb2.Image:
        # raise ValueError("Image protobuf is not valid")
        return None
    if not is_empty_string(image_proto.image_url):
        return load_image_from_url(image_proto.image_url)
    if not is_empty_string(image_proto.image_base64):
        return load_image_from_base64_string(image_proto.image_base64)
    if not is_empty_string(image_proto.image_bytes):
        return load_image_from_byte_string(image_proto.image_bytes)
    return None


def get_human_readable_bytes_size(input_bytes_size: int) -> str:
    if input_bytes_size == 0:
        return "0 bytes"
    if input_bytes_size < 1024:
        return str(input_bytes_size) + " bytes"
    if input_bytes_size < 1024 * 1024:
        kilobytes = input_bytes_size // 1024
        return str(kilobytes) + " Kilobytes"
    if input_bytes_size < 1024 * 1024 * 1024:
        megabytes = input_bytes_size // (1024 * 1024)
        return str(megabytes) + " Megabytes"
    if input_bytes_size < 1024 * 1024 * 1024 * 1024:
        gigabytes = input_bytes_size // (1024 * 1024 * 1024)
        return str(gigabytes) + " Gigabytes"
    return str(input_bytes_size) + " bytes"


def get_array_made_by_repeating_rows(row_value, num_repeats):
    if len(row_value.shape) == 1:
        row_value = row_value.reshape((1, row_value.shape[0]))
    return np.repeat(row_value, repeats=num_repeats, axis=0)


def fnv64_hash(data: bytes) -> int:
    """
    Computes int64 Fowler–Noll–Vo hash of `data`.
    :param data: bytes string to hash
    :return: hash output as integer
    """
    hash_ = 0xCBF29CE484222325
    for b in data:
        hash_ *= 0x100000001B3
        hash_ &= 0xFFFFFFFFFFFFFFFF
        hash_ ^= b
    return hash_


def generate_salted_hash(input_data: str, salt: str, max_length: int | None = None):
    """
    Generates a hash string for `input_data` using `salt`.
    :param input_data: An ASCII string
    :param salt: An ASCII string to use as salt
    :param max_length: The maximum length of the hash string to return
    :return: An ASCII string
    """
    # Turn input_data into bytes with a salt, input_data is expected to be ascii encodable string
    data = salt.encode("ascii") + input_data.encode("ascii")
    # Get the FNV integer hash for data.
    integral_hash = fnv64_hash(data)
    # Pack the integral hash into a bytes string.
    hash_bytes = struct.pack("<Q", integral_hash)
    # Remove the terminal '=' common to all base64 encoded strings
    return_value = base64.urlsafe_b64encode(hash_bytes).rstrip(b"=").decode("ascii")

    return return_value if max_length is None else return_value[:max_length]


def generate_uuid(max_length: int | None = None):
    uuid_value = uuid.uuid4()

    return uuid_value.hex[:max_length] if max_length is not None else uuid_value.hex


def get_current_micro_seconds_string() -> str:
    current_micro_seconds = time.time() * 1000000
    return str(math.ceil(current_micro_seconds))


def remove_disallowed_characters_from_string(
        input_string: str, disallowed_characters: str
) -> str:
    is_character_allowed = [1 for x in range(256)]
    for character in disallowed_characters:
        is_character_allowed[ord(character)] = 0
    output_string = ""
    for character in input_string:
        if is_character_allowed[ord(character)] == 0:
            continue
        output_string += character
    return output_string


def generate_unique_string_key(
        max_length: int | None = None, disallowed_characters: str = None
):
    time_microseconds_salt_string = get_current_micro_seconds_string()
    uuid_value = generate_uuid()
    return_value = generate_salted_hash(
        uuid_value, time_microseconds_salt_string, max_length=None
    )
    if disallowed_characters is None:
        return return_value[:max_length] if max_length is not None else return_value
    return_value = remove_disallowed_characters_from_string(
        return_value, disallowed_characters
    )
    return return_value[:max_length] if max_length is not None else return_value


def is_path_relative(path: str, reference_path: str = None) -> bool:
    if reference_path is None:
        return path[0] == "." or path[0] == "/"
    if path.startswith(reference_path):
        return False
    return True


def has_len(obj):
    """Checks if an object has a length using hasattr()."""
    return hasattr(obj, "__len__")


def has_len_try_except(obj):
    """Checks if an object has a length using try-except."""
    try:
        len(obj)
        return True
    except TypeError:
        return False


def maybe_get_length_of_object(obj):
    """Returns the length of an object if it has one, otherwise returns -1."""
    if has_len(obj):
        return len(obj)
    return -1


def is_list_of_numbers(input_object):
    if input_object is None or not (
            isinstance(input_object, list) or isinstance(input_object, np.ndarray)
    ):
        return False
    if isinstance(input_object, list):
        for x in input_object:
            if not is_number(x):
                return False
    if isinstance(input_object, np.ndarray):
        if not np.issubdtype(input_object.dtype, np.number):
            return False
        if input_object.ndim > 1:
            return False
    return True


def is_array_of_numbers(input_object):
    if (
            input_object is None
            or not (isinstance(input_object, list) or isinstance(input_object, np.ndarray))
            or maybe_get_length_of_object(input_object) in {0, None}
    ):
        return False
    if isinstance(input_object, list):
        list_lengths = set()
        has_numbers = False
        has_lists = False

        def is_valid_array_of_numbers_based_on_indicators():
            if len(list_lengths) > 1 or (has_lists and has_numbers):
                return False
            return True

        for x in input_object:
            if isinstance(x, list):
                list_lengths.add(len(x))
                has_lists = True
                if not is_array_of_numbers(x):
                    return False
                if not is_valid_array_of_numbers_based_on_indicators():
                    return False
                continue
            if is_number(x):
                has_numbers = True
                if not is_valid_array_of_numbers_based_on_indicators():
                    return False
                continue
            return False
        if not is_valid_array_of_numbers_based_on_indicators():
            return False
    if isinstance(input_object, np.ndarray):
        if not np.issubdtype(input_object.dtype, np.number):
            return False
    return True


def is_string_or_bytes_string(input_object):
    if input_object is None:
        return False
    if isinstance(input_object, str):
        return True
    if isinstance(input_object, bytes):
        return True
    return False


def is_list_of_strings(input_object):
    if (
            input_object is None
            or not isinstance(input_object, list)
            or maybe_get_length_of_object(input_object) in {0, None}
    ):
        return False
    for x in input_object:
        if not (isinstance(x, str) or isinstance(x, bytes)):
            return False
    return True


def is_list_of_dicts(input_object):
    if (
            input_object is None
            or not isinstance(input_object, list)
            or maybe_get_length_of_object(input_object) in {0, None}
    ):
        return False
    for x in input_object:
        if not (isinstance(x, dict)):
            return False
    return True


def maybe_convert_bytes_to_string(input_object, encoding="utf8"):
    try:
        if isinstance(input_object, bytes):
            return input_object.decode(encoding)
    except UnicodeDecodeError:
        pass
    return input_object


def maybe_convert_string_to_bytes(input_object, encoding="utf8"):
    try:
        if isinstance(input_object, str):
            return input_object.encode(encoding)
    except UnicodeEncodeError:
        pass
    return input_object


def maybe_convert_integer_to_hex_string(input_object):
    if isinstance(input_object, int):
        return hex(input_object)
    return input_object


def maybe_convert_hex_string_to_integer(input_object):
    if isinstance(input_object, str):
        try:
            converted_integer = int(input_object, 16)
            return converted_integer
        except ValueError:
            pass
        except Exception:
            pass
    return input_object


def maybe_convert_float_to_hex_string(float_64_value):
    if isinstance(float_64_value, float):
        return hex(struct.unpack("<Q", struct.pack("<d", float_64_value))[0])
    return float_64_value


def __maybe_convert_bytes_to_float(input_bytes):
    if isinstance(input_bytes, bytes):
        byte_string_length = len(input_bytes)
        match byte_string_length:
            case 4:
                return struct.unpack("!f", input_bytes)[0]
            case 8:
                return struct.unpack("!d", input_bytes)[0]
            case _:
                raise TypeError("Unknown floating point type.")
    raise TypeError("Unknown floating point type.")


def maybe_convert_hex_string_to_float(input_object: str):
    if isinstance(input_object, str):
        try:
            hex_string = input_object[:]
            hex_string = hex_string.strip().replace("0x", "")
            byte_array = unhexlify(hex_string)
            print("Byte array length : ", len(byte_array))
            # float_value = struct.unpack("!f", byte_array)[0] if len(byte_array) == 4 else None
            float_value = __maybe_convert_bytes_to_float(byte_array)
            return float_value
        except ValueError as ve:
            print(
                "Encountered ValueError while converting hex string to float:", str(ve)
            )
        except Exception as e:
            print("Encountered Exception while converting hex string to float:", str(e))
    else:
        print(
            "Provided input to `maybe_convert_hex_string_to_float` is not of string type!"
        )
        print("Returning original input to `maybe_convert_hex_string_to_float`")
    return input_object


def maybe_serialize_value(value):
    try:
        output = pickle.dumps(value)
        return output
    except Exception as e:
        print("Error encountered while trying to serialize: ", str(e))
        return value


def maybe_deserialize_value(value):
    try:
        output = pickle.loads(value)
        return output
    except Exception as e:
        raise ("Error encountered while trying to de-serialize: ", str(e))
        # return value


def get_time_ago_string(past_datetime):
    """
    Calculates the time difference between a past datetime and the current time,
    and returns a human-readable string (e.g., "5 hours ago", "2 days ago").
    """
    now = datetime.now()
    time_difference = now - past_datetime

    seconds = time_difference.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    weeks = days / 7
    months = days / 30.44  # Approximate average days in a month
    years = days / 365.25  # Approximate average days in a year

    if years >= 1:
        return f"{int(years)} year{'s' if int(years) > 1 else ''} ago"
    elif months >= 1:
        return f"{int(months)} month{'s' if int(months) > 1 else ''} ago"
    elif weeks >= 1:
        return f"{int(weeks)} week{'s' if int(weeks) > 1 else ''} ago"
    elif days >= 1:
        return f"{int(days)} day{'s' if int(days) > 1 else ''} ago"
    elif hours >= 1:
        return f"{int(hours)} hour{'s' if int(hours) > 1 else ''} ago"
    elif minutes >= 1:
        return f"{int(minutes)} minute{'s' if int(minutes) > 1 else ''} ago"
    else:
        return "just now"


def maybe_convert_to_int(input_object):
    try:
        if isinstance(input_object, numbers.Number):
            if isinstance(input_object, int):
                return input_object

        return int(input_object)
    except Exception as e:
        print("Error encountered while trying to convert to int: ", str(e))
        return input_object


def roll_dice(
        number_of_sides: int = 6, win_on_landing_faces: set | tuple | list = (1, 2, 3)
):
    random_integer = np.random.randint(1, number_of_sides)
    win_on_landing_faces = set(win_on_landing_faces)
    return random_integer in win_on_landing_faces


def clean_any_base64_string(input_base64_str: str) -> str:
    input_base64_str = convert_to_string(input_base64_str)
    return re.sub("^data:[^;]+;base64,", "", input_base64_str)


def get_file_type_from_data(file_data):
    if isinstance(file_data, str):
        # Extract base64 data from data URL
        data_url_match = re.match(r"^data:(.+?);base64,(.+)$", file_data)
        if data_url_match:
            content = base64.b64decode(data_url_match.group(2))
            kind = filetype.guess(content)
            if kind:
                return kind
    return None


def get_full_path_from_relative_path(relative_path, path_for_relative_reference):
    if (
            isinstance(relative_path, str)
            and isinstance(path_for_relative_reference, str)
            and len(relative_path) > 0
            and len(path_for_relative_reference) > 0
    ):
        return os.path.join(path_for_relative_reference, relative_path)
    return None


def maybe_make_dir_including_intermediate_dirs(
        full_dir_path, raise_error_if_exists=False
):
    try:
        if raise_error_if_exists and os.path.exists(full_dir_path):
            raise IOError(f"{full_dir_path} already exists.")
        if not os.path.exists(full_dir_path):
            os.makedirs(
                full_dir_path, exist_ok=False if raise_error_if_exists else True
            )
            return True
    except Exception as e:
        print("Error encountered while trying to make dir: ", str(e))
        return False
    return False


def get_current_timestamp_based_unique_hash_string(return_as_bytes=False):
    current_timestamp = time.time()
    current_timestamp_hex_string = maybe_convert_float_to_hex_string(current_timestamp)
    random_int = random.randint(0, 2 ^ 32 - 1)
    random_int_hex_string = maybe_convert_integer_to_hex_string(random_int)
    concatenated_hex_strings = current_timestamp_hex_string + random_int_hex_string
    sha256_hash = hashlib.sha256(concatenated_hex_strings.encode("utf-8")).hexdigest()
    return sha256_hash if not return_as_bytes else sha256_hash.encode("utf-8")


def kilobytes(value):
    return value * 1024


def megabytes(value):
    return value * 1024 * 1024


def gigabytes(value):
    return value * 1024 * 1024 * 1024
