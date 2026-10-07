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

While ScurryPy itself may not offer these features by default, ScurryPy is capable of being extended to include these features.

> [!TIP]
> The following formats assume this [mindset](https://scurry-works.github.io/scurrypy/getting_started/mindset/).

## Reference

### API (Parts and Params)

For parts:
```python
from scurrypy.core.part import Part
from scurrypy.core.types import RequiredPartField, OptionalPartField, RequiredNullablePartField, OptionalNullablePartField

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

For parameters:
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
> If a Part is included, please use `scurrypy.core.part.serialize` before passing to `HTTPClient.request`.

> [!NOTE]
> By adding `total=False`, it is implied all fields are optional.
> PLEASE be careful here. Some Params are all optional and some are all optional AND nullable!

### Resources

```python
from dataclasses import dataclass
from scurrypy.resources import BaseResource

@dataclass
class YourResource(BaseResource):
    """Your resource's description."""

    # fields needed to fetch this resource

    # endpoints as functions
```

Then in the client class:

```python
from .resources.me import YourResource

def your_resource(self, some_id: int, etc...):
    """Creates an interactable resource.

    Args:
        some_id (int): ID of target resource

    Returns:
        (YourResource): the class resource
    """
    return YourResource(self.http, some_id, etc...)
```

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
