# Changelog

## TODO / Upcoming Features

- add: pipedreams

## [0.0.0-demo.1] - 2026-03-03

### Added
- add: release-dryrun.sh
- add: changelog & upd related release.sh
- add: commit-msg git-hook
- add: automated changelog

### Fixed
- fix: release.sh bugs
- fix: release bugs
- fix: resulting parts are now Part::Box
- fix: if temp opened by user, copy it and process the copy; prevents ux/ui issues where user opened templates are closed

### Updated
- upd: legacy changelog
- upd: release-dryrun.sh is now verbose

## Early Development / Legacy Commits

- add: assemble command
- add: cubinet - simple cabinet template
- add: cubinet double template
- add: cubinet drawer template
- add: standardise working on xy (top) plane.
- add: btn assembe
- add: btn cut list
- add: template cloning to prevent user opened templates to be closed by assembler
- add: ~~clone ojs from templates~~
- add: clone the whole template file (if opened by user) for processing
- add: freeze gui & progressbar during operations
- fix: error originating from in the freeze class. AHEM! not fixed, just disabled as not required in demo
- fix: tolerate templates with spaces in filenames
- add: ~~void as an empty parametric template document with width parameter~~ NO! creates more problems than anything
- add: void as a directive, not a template
- add: btn new sheet
- fix: parts cloned from template to remain cubes - Part::Box
