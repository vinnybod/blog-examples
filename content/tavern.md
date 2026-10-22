---
title: Tavern
---

## Roster

People whose `location` points at this note (the standard Obsidian back-reference filter):

```base
filters:
  and:
    - location.asFile().path == this.file.path
views:
  - type: table
    name: Roster
    order:
      - file.name
      - location
```

## Fixed by the patch

The other ways bases-page reads a link from a string:

```base
filters:
  and:
    - file.hasProperty("location")
formulas:
  as_file: location.asFile().asLink()
  link: link(location)
  contains: list(location).contains(this)
properties:
  formula.as_file:
    displayName: asFile()
  formula.link:
    displayName: link()
  formula.contains:
    displayName: contains(this)
views:
  - type: table
    name: Fixed
    order:
      - file.name
      - location
      - formula.as_file
      - formula.link
      - formula.contains
```

## Left for a follow-up

These need a link value type; the patch doesn't change them:

```base
filters:
  and:
    - file.hasProperty("location")
formulas:
  equals: location == this.file.asLink()
  file: file(location).path == this.file.path
properties:
  formula.equals:
    displayName: == asLink()
  formula.file:
    displayName: file().path
views:
  - type: table
    name: Follow-up
    order:
      - file.name
      - location
      - formula.equals
      - formula.file
```

## Bar

The heading that `person-carol` links to.
