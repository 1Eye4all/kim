# kim/pipelines/string.py
# Copyright (C) 2014-2015 the Kim authors and contributors
# <see AUTHORS file>
#
# This module is part of Kim and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from .base import Input, Output, get_data_from_source, update_output


def is_valid_string(field, data):
    """pipe used to determine if a value can be coerced to a string

    :param field: instance of :py:class:``~.Field`` being pipelined
    :param data: data being piplined for the instance of the field.
    """

    try:
        return str(data)
    except ValueError:
        raise field.invalid("field is not a valid string")


class StringInput(Input):

    input_pipes = [
        get_data_from_source,
    ]
    validation_pipes = [
        is_valid_string,
    ]
    output_pipes = [
        update_output,
    ]


class StringOutput(Output):

    input_pipes = [
        get_data_from_source,
    ]
    output_pipes = [
        update_output,
    ]
