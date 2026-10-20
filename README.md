# Meeting Cost HUD

Live meeting cost overlay for OBS Studio and Microsoft Teams, in a single HTML file. Works offline, no dependencies.

**[Try it in your browser](https://yokoac.github.io/meeting-cost-hud/meeting-cost.html)**, or download `meeting-cost.html` and open it locally.

## Usage

Open `meeting-cost.html` in a browser. Settings start hidden: hover the overlay and click ⚙ (or press H). Enter participants, average annual salary, employer cost factor and working hours per year, then press **Start** or click the overlay. Settings are saved automatically and used next time; **Restore default settings** in the panel sets them back (the timer keeps running).

Hotkeys: Space start/pause · R reset · `+`/`-` participants · I show/hide calculation details · B burn money · H or Esc show/hide panel. Click inside the page first so it receives key presses.

Mouse: click the overlay to start/pause; hover it to reveal the ⚙ (settings panel) and the corner grip.

Resize: hover the overlay and drag the corner grip, or set **Overlay size** in the panel. Double-click the grip to reset.

Burning money: press **Burn** in the panel (or B) to let banknotes fly across the screen and burn up, with the current cost per hour in the centre (e.g. "€272/h going up in flames"). The timer keeps running. A smaller burst plays each time the cost passes a multiple of **Burn every**: leave it empty for auto (about every 10 minutes at the current cost per hour, rounded to 1/2/5 × 10ⁿ, e.g. €50), enter an amount, or 0 to turn it off.

Planned length: a thin bar under the cost fills up over **Planned length (min)** (default 30). It turns amber at 80%; when the meeting runs over, the bar and the elapsed time turn red and the full burn plays once ("Overtime: €272/h going up in flames"). Short reminders pop up at halfway ("Halfway · 15 min left") and, for meetings over 10 minutes, at "5 min left · time to wrap up". 0 turns all of this off.

URL parameters (browser only; OBS's **Local file** ignores them) override saved settings for that visit only, so a bookmark like `?n=20` does not change your saved defaults: `n`, `salary`, `factor`, `hours`, `cur` (EUR, USD, GBP, CHF), `pos` (br, bl, tr, tl), `scale` (0.4–4), `burn` (0 = off), `plan` (minutes, 0 = off), plus flags `overlay` (transparent background), `autostart` and `info` (show calculation details). Example: `meeting-cost.html?n=8&salary=70000&pos=tr&autostart`

## OBS + Microsoft Teams

Put the HUD over your webcam in OBS Studio and send it to Microsoft Teams via OBS Virtual Camera. Step-by-step guide, a ready-made OBS scene and a test background: [obs/README.md](obs/README.md).

## Demo video

`demo/record.py` re-records the demo video into `demo/out/demo.mp4` (gitignored): the real page in Chromium over a stand-in webcam, with meeting time fast-forwarded. It needs [uv](https://docs.astral.sh/uv/), which fetches Playwright and a temporary ffmpeg; nothing is installed into the repository.

```bash
uv run --no-project --with playwright playwright install chromium
```

```bash
uv run --no-project --with playwright --with imageio-ffmpeg demo/record.py
```

## License

[MIT](LICENSE)
