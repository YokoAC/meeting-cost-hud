# AGENTS.md

`meeting-cost.html` is a live meeting cost timer, used as an OBS Studio Browser Source (Local file) over a webcam and sent to MS Teams via OBS Virtual Camera (Windows). User-facing usage and OBS setup live in `README.md`; keep it in sync with behaviour changes.

## Constraints

- Single self-contained HTML file. No build step, no external dependencies, no CDNs. Must work offline as a local file in OBS's Chromium.
- All UI text in English. Every control has a `title` tooltip; new controls get one too.
- Keep code compact and readable. Colours are CSS variables on `:root`.

## Rules that are easy to break

- Cost is **integrated over time**: `costAcc += perSec * dt`. Changing inputs mid-meeting only affects cost from that moment on. Never replace it with `elapsed * rate`.
- The overlay (`#pill`) must not change size between states: the `#dot` state icon is a fixed 10px, and the hidden `#ghost` (9,999.99) shares a grid cell with `#val`.
- Transparent background inside OBS (detected via `window.obsstudio`) or with `?overlay`. "Local file" passes no URL params, so OBS must work without them.
- `#gear` and `#grip` are hover-only (on stream only while hovering in OBS Interact) and stop click propagation so they don't toggle the timer.
- Space check uses `e.key===' '` too: OBS Interact may send an empty `e.code`. Hotkeys are ignored while an input or select has focus (except Esc).
- Settings persist in `localStorage` key `mc`; every storage access is wrapped in try/catch. URL params (see README) override them.
- Burn animations live in their own full-screen `#fx` layer (`pointer-events:none`), never inside `#pill`. A change of the burn threshold only moves the next mark; it must not fire a burst.
- Status colours (green running, amber paused) belong to `#status`; planned-length colours (amber at 80%, red over) only go on `#bar` and `#time`. `#bar` always keeps its space (`visibility:hidden` when off). Like the burn threshold, changing the planned length never fires the overtime burn.
