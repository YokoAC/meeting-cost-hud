# AGENTS.md

`meeting-cost.html` is a live meeting cost timer, used as an OBS Studio Browser Source (Local file) over a webcam and sent to a video call app via OBS Virtual Camera (Windows; tested with Microsoft Teams, works with any app that accepts a webcam). User-facing usage lives in `README.md`, OBS setup and the importable scene in `obs/` (`obs/README.md`); keep them in sync with behaviour changes.

## Constraints

- Single self-contained HTML file. No build step, no external dependencies, no CDNs. Must work offline as a local file in OBS's Chromium.
- All UI text in English. Every control has a `title` tooltip; new controls get one too.
- Keep code compact and readable. Colours are CSS variables on `:root`.

## Rules that are easy to break

- Cost is **integrated over time**: `costAcc += perSec * dt`. Changing inputs mid-meeting only affects cost from that moment on. Never replace it with `elapsed * rate`.
- The overlay (`#pill`) must not change size between states (running, paused, not started; the Quiet display is a deliberate mode and may be smaller): the `#dot` state icon is a fixed 10px, and the hidden `#ghost` shares a grid cell with `#val`, reserving about 2 h of cost at the current rate (at least 9,999.99) in the current currency.
- Transparent background inside OBS (detected via `window.obsstudio`) or with `?overlay`. "Local file" passes no URL params, so OBS must work without them.
- `#gear` and `#grip` are hover-only (on stream only while hovering in OBS Interact) and stop click propagation so they don't toggle the timer.
- Space check uses `e.key===' '` too: OBS Interact may send an empty `e.code`. Hotkeys are ignored while an input or select has focus (except Esc).
- Settings persist in `localStorage` key `mc`; every storage access is wrapped in try/catch. URL params (see README) override them for that visit only: `save(...changed)` keeps the saved value of a field that still holds its URL value. Pass the changed field names to `save()`.
- Burn animations live in their own full-screen `#fx` layer (`pointer-events:none`), never inside `#pill`. A change of the burn threshold only moves the next mark; it must not fire a burst.
- Status colours (green running, amber paused) belong to `#status`; planned-length colours (amber at 80%, red over) only go on `#bar` and `#time`. `#bar` always keeps its space (`visibility:hidden` when off). Milestones (halfway, 5 min left, overtime) fire once while running when time crosses them; like the burn threshold, changing the planned length never fires them. All small labels go through `pop()`, which queues them so they never overlap.
- `demo/record.py` (README video, dev tooling only, see `demo/README.md`) drives the page through its globals `acc`, `costAcc`, `cfg`, `running` and `t0`, the hotkeys and URL params; re-record or adjust it when those change.
- Quiet display (`view=quiet`, `body.quiet`): cost keeps integrating; money animations are skipped but the burn mark still advances, so switching back fires no backlog. Time reminders stay; overtime pops a red label instead of `burnNow`.
- Position = anchor class on `#dock` (`tl tc tr bl bc br`) plus an optional drag offset `off` ("x,y" in % of the screen) applied by `place()`. Dropping a dragged HUD picks the anchor by thirds/halves and snaps onto it within the snap distance (at least 60 px, or half the HUD height; dashed `.snap` guides in `#fx` show the spots only while dragging); a click with less than 5 px movement still toggles the timer.
- Currency is a free ISO code checked against `Intl.supportedValuesOf('currency')`; `cur` holds the last valid one, an invalid entry is never saved.
- No native pop-up controls (`<select>` lists, `alert`/`confirm`): OBS Interact renders the page off-screen and never shows them. Panel `<select>`s are hidden data holders; their `.seg` button rows are the UI and dispatch the select's `input` event.
- Measure the HUD via `box()` (the unscaled `#hud` wrapper), never `#pill.getBoundingClientRect()`: OBS's Chromium (< 128) reports a `zoom`ed element's rect unscaled, which broke snapping and the burn origin at overlay sizes other than 1.
