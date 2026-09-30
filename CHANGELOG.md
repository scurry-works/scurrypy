# Changelog

This changelog documents all notable and breaking changes to the ScurryPy PyPi package.

## [2.4.0.2] - 30 Sept 2026

* Bug Fix: `DiscordTypes` and `DiscordStr` error when a value isn't known

## [2.4.0.1] - 29 Sept 2026

* Bug Fix: Client wouldn't accept any event not in `EventType`
* Bug Fix: Added `BaseResource` to `scurrypy.resources` for easier reach

## [2.4.0] - 29 Sept 2026

* Removed the HTTP and Gateway Protocol classes and their respective tests
* Replaced resource tests with serialization tests
* Added custom event support
* Added more thorough debug logging
* Added shard ID support to `Client`
* Moved `ResolvedDataModel` from `scurrypy.api.interactions` to `scurrypy.api`
* Added explicit field semantics to event fields
* Added documentation to previously undocumented enums
* Added model field typing specifications (see `CONTRIBUTING`)
* Optimized deserialization (JSON to dataclass)
* Added subcommand support, including support in `ext.commands`
* Added `Timestamp` and timestamp formatting utilities
* Refactored `Embed` and its components into `Part`s and `Model`s

## [2.3.2] - 19 Sept 2026

* Typing cleanup
* DiscordError can represent more than just JSON

## [2.3.1] - 16 Sept 2026

ScurryPy now requires Python 3.12+

* Added new channel flags
* Added `file_types` to the `FileUpload` component and file filtering support to `ApplicationCommandOptionModel`
* Added `AttachmentFlags`
* Changed `AttachmentModel.flags` from `int` to `AttachmentFlags`
* Updated Params annotations. This change is reflected in CONTRIBUTING
    * Some editing params are optional, while others are optional and nullable
    * Optional params use `total=False` on the Param Object
    * Nullable params additionally use `type | None`
* Added explicit field semantics to Part and Model fields
* Added `UnfurledMediaPart`

## [2.3.0.1] - 14 Sep 2026

* Bug Patch: corrected attachment editing

## [2.3] - 21 Feb 2026

* Sanitized field types
    * ScurryPy now passes mypy --strict
* Added customized exceptions for easier debugging

## [2.2] - 20 Feb 2026

* Associated enum imports are also available under `scurrypy.api`
    * Ex.
    ```py
        from scurrypy.api.components import Button, ButtonStyle

        # OR

        from scurrypy.enums import ButtonStyle
        from scurrypy.api.components import Button
    ```
* Renamed `client.bot_emoji()` to `client.application_emoji()` to match the ApplicationEmoji class rename from 2.0

## [2.1.1] - 19 Feb 2026

* Fixed client resource creation

## [2.1] - 19 Feb 2026

* Error handling improvements new properties in `scurrypy.ext`

## [2.0] - 18 Feb 2026

ScurryPy 2.0 refines core architecture following 1.0 stabilization
This release simplifies flag handling, restructures interaction models,
and clarifies editing semantics for long-term API consistency

* Migrated flags and constants to `IntFlag` / `IntEnum`
* Simplified intent and permission handling
    ```py
        intents = Intents.DEFAULT | MESSAGE_CONTENT
        client = Client(TOKEN, intents)

        # to verify an intent exists
        if Intents.MESSAGE_CONTENT not in client.intents:
            raise ValueError("Missing the MESSAGE_CONTENT intent!")
    ```
* Overhauled interaction event model
* Clarified editing semantics
* Standardized HTTP exposure (`Client.http`, `BaseResource.http`)
* Python 3.11+ required
* Overhauled parts and models under `api/`
* Rewrote documentation
* Added `ext/`, a collection of addons and helpers for common needs

## [1.0 Summary] - 6 Feb 2026 to 14 Feb 2026

ScurryPy's core architecture and API surface are now officially *stable* 🎉

* All IDs are now of type `Snowflake` (and `Snowflake` is a child of `int`)
* `Client` has new optional parameters

## [Pre-1.0 Summary] - 13 Dec 2025 to 6 Feb 2026

During the 0.x cycle, ScurryPy underwent rapid architectural refinement and API stabilization. 

* Finalized endpoint scope (bot scope only)
* Migrated to Python’s standard logging module
* Stabilized DataModel hydration system
* Refined naming conventions across models and resources
* Extracted command registry from Client
* Standardized parts to default to Discord defaults or None
* Split channel parts into dedicated channel types
* Added and corrected numerous endpoints
* Improved and hardened gateway reconnection logic
