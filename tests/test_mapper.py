import pytest

from kim.exception import MapperError
from kim.mapper import Mapper
from kim.fields import Field


class TestType(object):
    pass


class TestField(Field):
    pass


def test_mapper_sets_declared_fields():
    """Ensure that on attributes inheriting from :class:`kim.fields.Field`
    are set in a mappers fields.
    """

    class MyTestMapper(Mapper):

        __type__ = TestType

        name = TestField()
        other = 'not a field'

    mapper_with_fields = MyTestMapper()
    assert 'name' in mapper_with_fields.declared_fields
    assert isinstance(mapper_with_fields.declared_fields['name'], TestField)
    assert 'other' not in mapper_with_fields.declared_fields
    assert not getattr(mapper_with_fields, 'name', False)


def test_mapper_must_define_mapper_type():
    """Ensure that a :class:`.MapperError` is raised if a :class:`.Mapper`
    fails to set its __type__ attr.
    """

    mapper = Mapper()
    with pytest.raises(MapperError):
        mapper.get_mapper_type()


def test_mapper_inheritance():
    """test inheriting from other mapper classes
    """

    class OtherField(Field):
        pass

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

    class NewMapper(MapperBase):

        __type__ = TestType

        id = OtherField()
        additional_field = TestField()

    mapper = MapperBase()
    other_mapper = NewMapper()

    assert len(mapper.declared_fields.keys()) == 2
    assert 'id' in mapper.declared_fields
    assert 'name' in mapper.declared_fields

    assert len(other_mapper.declared_fields.keys()) == 3
    assert 'id' in other_mapper.declared_fields
    assert 'name' in other_mapper.declared_fields
    assert 'additional_field' in other_mapper.declared_fields

    assert isinstance(other_mapper.declared_fields['id'], OtherField)


def test_get_mapper_type():
    """ensure the correct object is returned when acessing the Mapper.__type__
    via :meth:``get_mapper_type``
    """

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()

    mapper = MapperBase()
    assert mapper.get_mapper_type() == TestType


def test_order_of_fields():
    """ensure fields set by mapper metaclass are set in order
    using _creation_order
    """

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

    class MyMapper(MapperBase):

        email = TestField()

    class ThirdMapper(MyMapper):

        id = TestField()
        id._creation_order = 999

    mapper = MyMapper()
    assert ['id', 'name', 'email'] == list(mapper.declared_fields.keys())

    mapper = ThirdMapper()
    assert ['name', 'email', 'id'] == list(mapper.declared_fields.keys())


def test_override_default_role():

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

        __roles__ = {
            '__default__': ['id', ]
        }

    mapper = MapperBase()
    assert mapper.declared_roles == {'__default__': ['id', ]}


def test_inherit_parent_roles():

    class RoleMixin(object):

        __roles__ = {
            'id_only': ['id', ]
        }

    class Parent(Mapper, RoleMixin):

        __type__ = TestType

        id = TestField()
        name = TestField()

        __roles__ = {
            'parent': ['name'],
            'overview': ['id', 'name']
        }

    class Child(Parent):

        __type__ = TestType

        __roles__ = {
            'overview': ['name', ]
        }

    mapper = Child()
    assert mapper.declared_roles == {
        '__default__': ['id', 'name'],
        'overview': ['name', ],
        'parent': ['name', ],
        'id_only': ['id', ],
    }


def test_new_mapper_sets_roles():

    class MapperBase(Mapper):

        __type__ = TestType

        id = TestField()
        name = TestField()

    class MyMapper(MapperBase):

        email = TestField()

        __roles__ = {
            'overview': ['email', ]
        }

    class OtherMapper(MyMapper):

        __roles__ = {
            'private': ['id', ]
        }

    mapper = MapperBase()
    assert mapper.declared_roles == {'__default__': ['id', 'name']}

    mapper = MyMapper()
    assert mapper.declared_roles == {
        'overview': ['email', ],
        '__default__': ['id', 'name', 'email']}

    mapper = OtherMapper()
    assert mapper.declared_roles == {
        '__default__': ['id', 'name', 'email'],
        'overview': ['email'],
        'private': ['id', ]
    }
