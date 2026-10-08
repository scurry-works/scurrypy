# ScurryPy Mindset
---

This section will guide you through the flow, setup, and role of each folder in the project.

!!! tip "tl'dr"
    Inbound payloads are queried; outbound payloads are constructed.

## What is a JSON query?
---
JSON payloads received from Discord are wrapped in [`JsonQuery`][scurrypy.core.json_query.JsonQuery] to support traversal and common operations.

For example, if you want an event user's ID:

```py
event.get('user.id', t=Snowflake).value
```
where:

1. `get` traverses the event data by getting `user > id` and interprets the resulting value as a `Snowflake`.
2. `value` is the resulting value of the entire chain. It should be the user's ID as a Snowflake!

Need to get a value from a list of objects?

```py
event.get('attachments.0.filename').value
```

Need a list of IDs?

event.get('member.roles', t=list[Snowflake]).value

!!! note
    If a list or dict is supplied, it must have arguments!

    e.g., `list[int]`, `dict[Snowflake, str]`

!!! tip "Keys Not Found"
    Keys that are not found return `None`. Keep an eye out for Omittable fields in event payloads as these fields are NOT always present!

## What is a resource?
---

Resources model Discord's resource objects.

*Q. How do I send a message?*

A: Use the [`Channel.send`][scurrypy.resources.channel.Channel.send] endpoint

Endpoints return *queries*, not resources! Resources and queries are split so you can cache, serialize, and inspect query data without the weight of methods.

## What is a Part?
---

Parts model the user's contract with *creation* endpoints. Use these classes when you want to create something.

*Q. How do I create a message?*

A: With the [`MessagePart`][scurrypy.api.messages.MessagePart]

*Q. How do I respond to an event?*

A: `Event > Resource > Request`. ScurryPy will never do this for you (unless you use `scurrypy.ext`).

## What is a Parameter?
---

Parameters model the user's contract with *modifying* endpoints. Use these classes when you want to modify something.

Parameters are `TypedDict`s that are meant to be `Unpack`ed by endpoint functions.
They are constructed via keyword arguments rather than manual instantiation.

## What is a context?
---

Contexts are part of the `scurrypy.ext` module. They group properties associated with the events the addon dispatches.

For example, [`ApplicationCommandContext`][scurrypy.ext.commands.ctx.ApplicationCommandContext] contains commonly needed properties from the [`INTERACTION_CREATE`][scurrypy.enums.events.EventType] event including bot, event, event data, and various helper properties.
