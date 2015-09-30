# kim/pipelines/string.py
# Copyright (C) 2014-2015 the Kim authors and contributors
# <see AUTHORS file>
#
# This module is part of Kim and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from .base import (Input, Output, marshal_input_pipe, marshal_output_pipe,
                   serialize_input_pipe, serialize_output_pipe)
from kim.utils import attr_or_key


def is_list(field, data):
    """pipe used to determine if a value can be iterated.

    :param field: instance of :py:class:``~.Field`` being pipelined
    :param data: data being piplined for the instance of the field.
    """

    if not isinstance(data, list):
        raise field.invalid(error_type='type_error')


def marshall_collection(field, data, output):
    """iterate over each item in ``data`` and marshal the item through the
    wrapped field defined for this collection

    """
    wrapped_field = field.opts.field
    existing_value = attr_or_key(output, field.opts.source)

    output = []

    for i, datum in enumerate(data):
        _output = {}
        # If the object already exists, try to match up the existing elements
        # with those in the input json
        if existing_value is not None:
            try:
                _output[wrapped_field.opts.source] = existing_value[i]
            except IndexError:
                pass
        wrapped_field.marshal(datum, _output)
        result = _output[wrapped_field.opts.source]
        output.append(result)

    return output


def serialize_collection(field, data):
    """iterate over each item in ``data`` and serialize the item through the
    wrapped field defined for this collection

    """
    wrapped_field = field.opts.field
    output = []

    for datum in data:
        _output = {}
        wrapped_field.serialize(datum, _output)
        result = _output[wrapped_field.name]
        output.append(result)

    return output


class CollectionInput(Input):

    input_pipes = marshal_input_pipe
    validation_pipes = [
        is_list,
    ]
    output_pipes = [marshall_collection] + marshal_output_pipe


class CollectionOutput(Output):

    input_pipes = serialize_input_pipe
    validation_pipes = [
        is_list,
    ]
    process_pipes = [
        serialize_collection,
    ]
    output_pipes = serialize_output_pipe
