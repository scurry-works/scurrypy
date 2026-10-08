# JsonQuery Examples
---

The following examples demonstrate how to use [`JsonQuery`][scurrypy.core.json_query.JsonQuery].

`JsonQuery` works by traversing its data using a dot-separated path.
The resulting query is stored in `JsonQuery.value`.

## Basic Use
---
Demonstrates getting `username` from a payload.

```py
example = JsonQuery({
    'user': {
        'username': 'foo-bar'
    }
})

example.get('user.username').pprint() # 'foo-bar'
```

## Value Conversion
---
Demonstrates getting `id` from a payload and converting it to an `int`.

```py
example = JsonQuery({
    'user': {
        'id': '1234567890123456',
    }
})

example.get('user.id', t=int).pprint() # 1234567890123456
```

!!! tip
    You can also use custom callables such as [`Snowflake`][scurrypy.core.snowflake.Snowflake] and [`Timestamp`][scurrypy.core.timestamp.Timestamp]!

## Parametric Type Conversion
---
Demonstrates getting a list of IDs from a payload and converting it to `list[int]`.

```py
example = JsonQuery({
    'user': {
        'roles': ['1234567890123456', '6543210987654321', '1324354657687980']
    }
})

example.get('user.roles', t=list[int]).pprint() # [1234567890123456, 6543210987654321, 1324354657687980]
```

## List Indexing
---
Demonstrates getting `filename` from the second element in a list.

```py
example = JsonQuery({
    'attachments': [
        {
            'id': '123',
            'filename': 'foo_file.png'
        },
        {
            'id': '456123',
            'filename': 'bar_file.jpg'
        }
    ]
})

example.get('attachments.1.filename').pprint() # 'bar_file.jpg'
```

## Map Indexing
---
Demonstrates getting a user from a map of IDs to users.

```py
example = JsonQuery({
    'users': {
        '123': {
            'username': 'foo-bar'
        },
        '456': {
            'username': 'spam-tuna'
        }
    }
})

example.get('users.456.username').pprint() # 'spam-tuna'
```
