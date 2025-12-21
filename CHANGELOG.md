# Changelog

This changelog documents all notable and breaking changes to ScurryPy.

## [0.10.0] - 2025-12

### Changes

Logging has been improved for finer grained control.

* Events not registered by the user are now `DEBUG` messages.

## [0.9.0] - 2025-12

### Breaking Changes

The handling of `application_id` has been refactored and is now passed explicitly to command registration APIs.

* `Client.__init__`
    * before: `Client(token, application_id, intents, logger)`
    * after: `Client(token, intents)`

* `BaseClient.register_guild_commands`
    * before: `register_guild_commands(commands, guild_ids)`
    * after: `register_guild_commands(application_id, commands, guild_ids)`

* `BaseClient.register_global_commands`
    * before: `register_global_commands(commands)`
    * after: `register_global_commands(application_id, commands)`

* `BaseClient.bot_emoji`
    * before: `bot_emoji()`
    * after: `bot_emoji(application_id)`

### Changed

* Scurrypy's Logger module has been replaced with Python's standard `logging` module.
    * Scurrypy no longer configures logging by default. Users may configure logging as needed.
    * See [Logging](https://scurry-works.github.io/scurrypy/logging) for details.

* New class: `EventTypes`. This class is a convenience class to prevent typos in event registration.
    * Ex.
        ```py
        from scurrypy import Client, EventTypes, MessageCreateEvent

        client = Client(...)

        async def on_message_create(event: MessageCreateEvent): ...

        client.add_event_listener(EventTypes.MESSAGE_CREATE, on_message_create)
        ```


## [0.8.8.2] - 2025-12

### Changed
* Corrected `FileUpload`: `component: LabelChild` is supposed to be `custom_id: str`.
See [FileUpload](https://scurry-works.github.io/scurrypy/api/ui_components/#scurrypy.parts.components_v2.FileUpload) for the updated version.
