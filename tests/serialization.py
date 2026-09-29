from scurrypy.core.model import DataModel, datamodel
from scurrypy.core.types import (
    ScurrypyStr, 
    ScurrypyInt, 
    ScurrypyBool, 
    ScurrypyFloat,
    PresentModelField,
    OmittableModelField
)

@datamodel
class MyInnerModel(DataModel):
    inner_str: PresentModelField[ScurrypyStr]
    inner_int: PresentModelField[ScurrypyInt]

@datamodel
class MaybeInnerModel(DataModel):
    maybe_str: OmittableModelField[ScurrypyStr]
    maybe_int: OmittableModelField[ScurrypyInt]

@datamodel
class MyModel(DataModel):
    my_str: PresentModelField[ScurrypyStr]
    my_int: PresentModelField[ScurrypyInt]
    my_bool: PresentModelField[ScurrypyBool]
    my_float: PresentModelField[ScurrypyFloat]
    my_list: PresentModelField[list[ScurrypyInt]]
    my_struct: PresentModelField[MyInnerModel]

    maybe_str: OmittableModelField[ScurrypyStr]
    maybe_int: OmittableModelField[ScurrypyInt]
    maybe_bool: OmittableModelField[ScurrypyBool]
    maybe_float: OmittableModelField[ScurrypyFloat]
    maybe_list: OmittableModelField[list[ScurrypyFloat]]
    maybe_struct: OmittableModelField[MaybeInnerModel]

my_model = MyModel.from_dict({
    'my_str': 'my string',
    'my_int': '123',
    'my_bool': 'false',
    'my_float': '0.15',
    'my_list': ['987', '654', '321'],
    'my_struct': {
        'inner_str': 'my string 2',
        'inner_int': '123456'
    },
    'maybe_struct': {}
})

assert my_model.my_str == 'my string'
assert my_model.my_int == 123
assert my_model.my_bool is False
assert my_model.my_float == 0.15
assert my_model.my_list == [987, 654, 321]
assert my_model.my_struct is not None
assert my_model.my_struct.inner_str == 'my string 2'
assert my_model.my_struct.inner_int == 123456
assert any([
    my_model.maybe_str, 
    my_model.maybe_int, 
    my_model.maybe_bool, 
    my_model.maybe_float
]) is False
assert my_model.maybe_list is None
assert my_model.maybe_struct is not None

serialized = my_model.to_dict()

assert serialized["my_str"] == "my string"
assert serialized["my_int"] == 123
assert serialized["my_bool"] is False
assert serialized["my_float"] == 0.15
assert serialized["my_list"] == [987, 654, 321]

assert "maybe_list" not in serialized
assert serialized["maybe_struct"] == {}
