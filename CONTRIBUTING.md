## Contributing to ScurryPy

*Thank you for your interest in contributing to ScurryPy*!

Contributions must adhere to ScurryPy’s existing architectural patterns.
ScurryPy is *feature-neutral* but *architecture-opinionated*. 
It doesn’t enforce how users must build bots, only how the library itself stays consistent.

## What's Needed

ScurryPy is in a stability-focused development phase: no feature expansion, only alignment with Discord API changes.

**Not Accepting:**

* Auto-caching (opt-in only. See `scurrypy.ext.cache`)
* Voice support and *Group* DM (out of scope)
* Sub-commands and automodding (lots of overhead for not enough gain)
* Auditing (includes many unsupported features)
* Endpoints with non-`bot` auth scopes, are unstable/experimental, or related to voice.
* Anything monetization based (e.g., entitlements and subscriptions)

While ScurryPy itself may not offer these features by default, you are more than welcome to extend ScurryPy to include these features.

> [!TIP]
> The following formats assume this [mindset](https://scurry-works.github.io/scurrypy/getting_started/mindset/).

## Reference

### API (Parts and Models)

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

from ..core.types import PresentModelField, OmittableModelField, PresentNullableModelField, OmittableNullableModelField

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: PresentModelField[type]
    """This field will always be present."""

    field_2: OmittableModelField[type]
    """This field might be omitted."""

    field_3: PresentNullableModelField[type]
    """This field will always be present, but can also be None."""

    field_4: OmittableNullableModelField[type]
    """This field might be omitted, but can also be None."""
```
> [!NOTE]
> Objects must be unique (no partial copies) with their fields replicating Discord's and be fully documented.

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
