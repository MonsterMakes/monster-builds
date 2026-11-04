# monster-builds

Design and fabrication source for build projects. One package per project.

| Package | What |
|---|---|
| [`packages/joanie-steel`](packages/joanie-steel) | Exterior steel stairs, cable rail and master bath landing. Drawing set, shop guide and part guide, all generated from one geometry model. |

Each package is self-contained: its own source, its own build command, its own
output. Nothing is shared between packages yet; if that changes, shared code
goes in `packages/` too and is imported, not copied.
