# hackwrap

A powerful decorator-based module to "hack" Python functions and classes — inject, modify, or protect behavior dynamically.

## Features

- 🔄 Convert functions between sync and async (`@asnc`, `@snc`)
- 🧠 Inspect and extract function metadata with `this`
- 🔒 Protect functions (`@private`, `@undeletable`, `@uncallable`)
- 🌍 Promote functions to global scope (`@globe`)
- ⚙ Inherit variables, modules, or class attributes (`@varinherit`, `@moduleinherit`, `@classinherit`)
- 🧵 Make functions threaded (`@threadify`) or endless (`@endless`)
- ⚠ Handle exceptions and warnings gracefully (`@handle`)
- 🧩 Expose **double underscored** functions (`@public`)
- 🎭 Treat functions like variables (`@variable`, `@paramvariable`)
- 🧬 Dynamic wrapper inheritance (`@inherit`)
- 🧰 Utility tools and decorators with full introspection and reflection

## Installation

```bash
pip install hackwrap
