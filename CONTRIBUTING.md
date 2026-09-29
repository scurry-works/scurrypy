## Contributing to ScurryPy

*Thank you for your interest in contributing to ScurryPy*!

Contributions must adhere to ScurryPy’s existing architectural patterns.
ScurryPy is *feature-neutral* but *architecture-opinionated*. 
It doesn’t enforce how users must build bots, only how the library itself stays consistent.

## What's Needed

ScurryPy is currently in a stability-focused development phase.
Development is primarily limited to keeping ScurryPy aligned with changes to Discord's API.

Contributions should therefore focus on:

* Discord API additions or changes within ScurryPy's supported scope
* Bug fixes
* Documentation improvements
* Typing and serialization improvements
* Architectural consistency

**Not Accepting:**

See [coverage](https://scurry-works.github.io/scurrypy/coverage/) for details on what ScurryPy is currently not accepting.

While ScurryPy itself may not offer these features by default, ScurryPy is capable of being extended to include these features.

> [!TIP]
> The following formats assume this [mindset](https://scurry-works.github.io/scurrypy/getting_started/mindset/).

## Reference

### API (Parts and Models)

For parts:
```python
from ..core.types import RequiredPartField, OptionalPartField, RequiredNullablePartField, OptionalNullablePartField

@dataclass
class YourPart(DataModel):
    """Your model's description."""

    field_1: RequiredPartField[type] = None
    """This is a field that must be filled out at some point."""

    field_2: OptionalPartField[type] = None
    """This is an optional field and can be omitted."""

    field_3: RequiredNullablePartField[type] = None
    """This field must be filled out at some point. This field accepts None."""

    field_4: OptionalNullablePartField[type] = None
    """This is an optional field and can be omitted. This field accepts None."""
```

For models:
```py
from ..core.types import PresentModelField, OmittableModelField, PresentNullableModelField, OmittableNullableModelField
from ..core.serialization import ScurrypyStr, ScurrypyInt, ScurrypyBool, ScurrypyFloat, ScurrypyPrimitive

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: PresentModelField[ScurrypyType]
    """This field will always be present."""

    field_2: OmittableModelField[ScurrypyType]
    """This field might be omitted."""

    field_3: PresentNullableModelField[ScurrypyType]
    """This field will always be present, but can also be None."""

    field_4: OmittableNullableModelField[ScurrypyType]
    """This field might be omitted, but can also be None."""
```

Model field types must ultimately be compatible with ScurrypyType. 
Built-in primitive types include `ScurrypyStr`, `ScurrypyInt`, `ScurrypyBool`, `ScurrypyFloat`, and `ScurrypyPrimitive`.

Lists are `list[ScurrypyType]`.

Maps must be `dict[Snowflake, ScurrypyType]`.

> [!NOTE]
> Objects must be unique (no partial structures) with their fields replicating Discord's and be fully documented.
> For example, Discord frequently documents "partial emojis." `EmojiModel` is the single source of truth for all emoji structures.

### Resources

```python
from dataclasses import dataclass
from .base_resource import BaseResource

@dataclass
class YourResource(BaseResource):
    """Your resource's description."""

    # fields needed to fetch this resource

    # endpoints as functions
```

Then in the client class:

```python
def your_resource(self, some_id: int, etc, *, context = None):
    """Creates an interactable resource.

    Args:
        some_id (int): ID of target resource

    Returns:
        (YourResource): the class resource
    """
    from .resources.me import YourResource

    return YourResource(self._http, some_id, etc...)
```

### Parameters

```python
from typing import TypedDict

class MyParams(TypedDict, total=False):
    """Your params description."""

    field_1: type
    """This field can only be type."""

    field_2: type | None
    """This field can be type or set to None."""
```
> [!NOTE]
> If a DataModel is included, please use `scurrypy.core.serialization.serialize` before passing to `HTTPClient.request`.

> [!NOTE]
> By adding `total=False`, it is implied all fields are optional.
> PLEASE be careful here. Some Params are all optional and some are all optional AND nullable!

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
