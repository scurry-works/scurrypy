## Contributing to ScurryPy

First and foremost, *thank you for your interest in contributing to ScurryPy*!

Future contributions should adhere to clean and understandable architecture. With this said, a lot of the infrastructure is already in place, it's just the matter of coverage and mimicking what's already there. 
ScurryPy is *feature-neutral* but *architecture-opinionated*. It doesn’t enforce how users must build bots, only how the library itself stays consistent.

The following sections will detail what's left and how it's expected to be filled out.

## Philosophy

ScurryPy prioritizes **clarity over magic**. When contributing:

* Every operation should be traceable
* No hidden behavior or side effects
* No attribute modification from outside the class
* Simple, explicit code over clever abstractions
* If you can't explain it in 3-6 steps, simplify it

## What's Needed

**High Priority:**
* Missing endpoints and resources (see [Discord API docs](https://discord.com/developers/docs))
* Documentation improvements

**Nice to Have:**
* Example bots
* Guide

**Not Accepting:**
* Auto-caching (architectural decision)
* Voice support (out of scope for now)

> **Important Note**: Throughout this document, Discord's payloads are called objects and ScurryPy's models are called data classes.

## Adding Models

All models and resources in ScurryPy are data classes themselves and inherit the `DataModel` base class. 

Please refer to the following template for how all of ScurryPy's objects are expected to be formatted:

```python
from dataclasses import dataclass
from .model import DataModel

from typing import Optional # only if you need it

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: type
    """This is a mandatory field. It needs to be filled NOW."""

    field_2: Optional[type] = None
    """This is an optional field. It can be omitted entirely."""

    field_3: type = None
    """This is a deferrable field. It can be filled out LATER."""
```
Notes:
* Fields must mimic objects verbatim. (e.g., if an object field is named `icon`, the dataclass field must also be called `icon`.)
* Descriptions are preferrably in your own words, but you can also just use Discord's docs.
* If an object appears that was already defined, use that model; don't create a new model! (e.g., the user object appears in many places. Always use the defined `UserModel`.)

For MODELS ONLY:
* Models should have NO helper functions. Functions in models will be removed!
* Models are NOT responsible for HTTP requests. Resources do this!

## Adding Resources
Resources are just like model, but with added functionality. All resources inherit the [`BaseResource`]((https://scurry-works.github.io/scurrypy/internals/model/#scurrypy.resources.base_resource.BaseResource)) class.

Please refer to the following example for how the resource is expected to be laid out:
```python
from dataclasses import dataclass
from .base_resource import BaseResource

@dataclass
class YourResource(BaseResource):
    """Your resource's description."""

    # fields needed to fetch this resource

    # endpoints as functions
```

Some fetches have JSON query strings attached. In this case you define them as follows:

    ```python
    from typing import TypedDict

    class YourParams(TypedDict, total=False):
        param_1: type
        param_2: type

    ...

    @dataclass
    class YourResource(DataModel):
        # the fields

        async def fetch_me(self, **kwargs: Unpack[YourParams]):
            # the logic...
    ```

[`BaseClient`](https://scurry-works.github.io/scurrypy/internals/base_client) provides a thin layer for requesting resources. If you implement a new resource, please also add it to the client as follows:

    ```python
    def fetch_me(self, some_id: int, ...):
        """Creates an interactable resource.

        Args:
            some_id (int): ID of target resource

        Returns:
            (YourResource): the class resource
        """
        from .resources.me import YourResource

        return YourResource(..., self._http)
    ```
    and PLEASE: document the function completely!

## Missing Endpoints
All endpoints should send requests through [`HTTPClient.request()`](https://scurry-works.github.io/scurrypy/internals/http/#scurrypy.core.http.HTTPClient.request) and be attached to their respective resource. Which resource gets the endpoint is a design decision for the contributor to make based on the criteria of the endpoint. The request function does the bulk of the heavy lifting; just return the data if it's a GET request.

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
