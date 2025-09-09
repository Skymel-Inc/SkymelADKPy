import time
import uuid
import hashlib
from .commonUtils import generate_unique_string_key


class CommonHashUtils:
    def __init__(self):
        raise RuntimeError("This class should not be instantiated; call it instead as follows: CommonHashUtils.generate_unique_id()")

    @staticmethod
    def generate_unique_id(max_length=None):
        """
        Generates a unique identifier string.
        
        Args:
            max_length (int, optional): Maximum length of the returned ID
            
        Returns:
            str: A unique identifier string
        """
        return generate_unique_string_key(max_length=max_length)

    @staticmethod
    def generate_salted_hash(input_data: str, salt: str, max_length=None):
        """
        Generates a salted hash of the input data.
        
        Args:
            input_data (str): Data to hash
            salt (str): Salt to use
            max_length (int, optional): Maximum length of returned hash
            
        Returns:
            str: Salted hash string
        """
        # Combine salt and data
        combined = salt + input_data
        
        # Create hash
        hash_object = hashlib.sha256(combined.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        
        if max_length is not None:
            return hash_hex[:max_length]
        return hash_hex

    @staticmethod
    def generate_uuid(max_length=None):
        """
        Generates a UUID string.
        
        Args:
            max_length (int, optional): Maximum length of returned UUID
            
        Returns:
            str: UUID string
        """
        uuid_str = str(uuid.uuid4()).replace('-', '')
        if max_length is not None:
            return uuid_str[:max_length]
        return uuid_str