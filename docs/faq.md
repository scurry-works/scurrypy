---
hide:
  - navigation
---

# Frequently Asked Questions (FAQ)
---

Below are some burning questions you might have about ScurryPy.

If you have a question, consult this page first. Not answered? Ask in the [support server](https://discord.gg/D4SdHxcujM)!

## Q. What is an addon?
Addons are modular extensions that subscribe to the client's event system to provide higher-level functionality.
Check out examples of addons [here](https://scurry-works.github.io/scurrypy/addons). 

## Q. Why don't events autocreate resources?
Events expose data, not capabilities. This separation keeps behavior explicit and avoids hidden side effects. If you prefer higher-level abstractions, see `scurrypy.ext`.

See the [addon example](getting_started/addons.md#upgrading-events-to-resources) for reference.

## Q. How do I use params?
When editing an object via Params, providing a field replaces the object's existing value with the value provided.

Omitting a field leaves the object's existing value unchanged.

## Q. Do I have to use `scurrypy.ext`?
No. The core client handles gateway and HTTP functionality. Extensions are entirely optional.

See [core examples](getting_started/core_examples.md) for examples on using ScurryPy without `scurrypy.ext`.

## Q. Is caching built-in?
No. Caching is provided as optional addons under `scurrypy.ext.cache`.
