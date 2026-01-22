---
description: All decision checklists consolidated for final review before committing Python changes.
---

# Decision Checklists Reference

**Read when**: Final review before committing Python code, need quick lookup of requirements

---

## Before Writing `try/except`

- [ ] Is this at an error boundary? (CLI/API level)
- [ ] Can I check the condition proactively? (LBYL)
- [ ] Am I adding meaningful context, or just hiding?
- [ ] Is third-party API forcing me to use exceptions? (No LBYL check exists—not even format validation)
- [ ] Have I encapsulated the violation?
- [ ] Am I catching specific exceptions, not broad?
- [ ] If catching at error boundary, am I logging/warning? (Never silently swallow)

**Default: Let exceptions bubble up**

---

## Before Path Operations

- [ ] Did I check `.exists()` before `.resolve()`?
- [ ] Did I check `.exists()` before `.is_relative_to()`?
- [ ] Am I using `pathlib.Path`, not `os.path`?
- [ ] Did I specify `encoding="utf-8"`?

---

## Before Using `typing.cast()`

- [ ] Have I added a runtime assertion to verify the cast?
- [ ] Is the assertion cost trivial (O(1))? If yes, always add it.
- [ ] If skipping, is it because I just performed an isinstance check (redundant)?
- [ ] If skipping for performance, have I documented the measured overhead?

**Default: Always add runtime assertion before cast when cost is trivial**

---

## Before Defining an Interface (ABC or Protocol)

- [ ] Do I own all implementations? -> Prefer ABC
- [ ] Am I wrapping a third-party library? -> Prefer Protocol
- [ ] Do I need runtime isinstance() validation? -> Use ABC
- [ ] Is this a minimal interface (1-2 methods)? -> Protocol may be simpler
- [ ] Do I need shared method implementations? -> Use ABC

**Default for erk internal code: ABC. Default for external library facades: Protocol.**

---

## Before Preserving Backwards Compatibility

- [ ] Did the user explicitly request it?
- [ ] Is this a public API with external consumers?
- [ ] Have I documented why it's needed?
- [ ] Is migration cost prohibitively high?

**Default: Break the API and migrate callsites immediately**

---

## Before Inline Imports

- [ ] Is this to break a circular dependency?
- [ ] Is this for TYPE_CHECKING?
- [ ] Is this for conditional features?
- [ ] If for startup time: Have I MEASURED the import cost?
- [ ] If for startup time: Is the cost significant (>100ms)?
- [ ] If for startup time: Have I documented the measured cost in a comment?
- [ ] Have I documented why the inline import is needed?

**Default: Module-level imports**

---

## Before Importing/Re-Exporting Symbols

- [ ] Is there already a canonical location for this symbol?
- [ ] Am I creating a second import path for the same symbol?
- [ ] If this is a shim module, am I importing only what's needed for this module's purpose?
- [ ] Have I avoided `__all__` exports?

**Default: Import from canonical location, never re-export**

---

## Before Declaring a Local Variable

- [ ] Is this variable used more than once?
- [ ] Is this variable used close to where it's declared?
- [ ] Would inlining the computation hurt readability?
- [ ] Am I extracting object fields into locals that are only used once?

**Default: Inline single-use computations at the call site; access object attributes directly**

---

## Before Adding a Default Parameter Value

- [ ] Do 95%+ of callers actually want this default?
- [ ] Would forgetting to pass this parameter cause a subtle bug?
- [ ] Is there a safer design that makes the choice explicit?
- [ ] If the default is never overridden anywhere, should this parameter exist at all?

**Default: Require explicit values; eliminate unused defaults**

---

## Before Adding a Function with 5+ Parameters

- [ ] Have I added `*` after the first (or ctx) parameter?
- [ ] Is only `self`/`ctx` positional?
- [ ] Is this an ABC/Protocol method? (exempt from rule)
- [ ] If using ThreadPoolExecutor.submit(), am I using a lambda wrapper?

**Default: All parameters after the first should be keyword-only**

---

## Before Writing Module-Level Code

- [ ] Does this involve any computation (even `Path()` construction)?
- [ ] Does this involve I/O (file, network, environment)?
- [ ] Could this fail or raise exceptions?
- [ ] Would tests need to mock this value?

If any answer is "yes", wrap in a `@cache`-decorated function instead.
