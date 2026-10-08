# Changelog

This changelog documents all notable and breaking changes to the ScurryPy PyPi package.

## [3.1] - 7 Oct 2026

* Added helpers: `Mention`, `Cdn`
* `Embed.set_user_author` now handles animated avatars
* Cleaned up attachment creation and modification
* Message and interaction flags are no longer configurable during instantiation
    * Flags are now set by the resource endpoints
* Bug Fix: `JsonQuery.get` now correctly handles map keys

## [3.0] - 6 Oct 2026

ScurryPy 3.0 completes a major architectural rewrite.

* Replaced DataModel hydration with JsonQuery
* Separated inbound payload querying from outbound payload construction
* Reworked API into Parts, Params, and Resources
* Removed event payload classes in favor of raw JsonQuery payloads
* Reorganized documentation around API and Reference
* Simplified the core architecture

## [2.0 Summary] - 14 Feb 2026 - 30 Sept 2026

ScurryPy 2.0 refined the architecture established during 1.0, with a focus on
consistency, clearer API boundaries, and a more extensible addon system.

* Migrated flags and constants to `IntFlag` / `IntEnum`
* Overhauled interaction event models
* Clarified editing semantics
* Standardized HTTP exposure through `Client.http` and `BaseResource.http`
* Reworked Parts and Models under `api/`
* Added `ext/` for addons and common helpers
* Rewrote the documentation
* Raised the minimum Python version to 3.11

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
