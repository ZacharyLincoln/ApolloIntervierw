from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator
from sqlalchemy.exc import ArgumentError
import re

class VIN(TypeDecorator):

    # underlying type
    impl = String

    def process_bind_param(self, value, dialect):
        if not value:
            return None
        
        value = value.upper()

        # check to make sure I O Q are not in the VIN and that it is 17 characters long
        if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', value):
            raise ArgumentError('Invalid VIN')
        return value

    def process_result_value(self, value, dialect):
        return value