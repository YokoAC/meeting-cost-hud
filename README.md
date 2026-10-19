# Meeting Cost HUD

Live meeting cost timer in a single HTML file. Works offline, no dependencies.

## Usage

Open `meeting-cost.html` in a browser. Settings start hidden: hover the overlay and click ⚙ (or press H). Enter participants, average annual salary, employer cost factor and working hours per year, then press **Start** or click the overlay. Settings are saved automatically.

Hotkeys: Space start/pause · R reset · `+`/`-` participants · I show/hide calculation details · B burn money · H or Esc show/hide panel. Click inside the page first so it receives key presses.

Mouse: click the overlay to start/pause; hover it to reveal the ⚙ (settings panel) and the corner grip.

Resize: hover the overlay and drag the corner grip, or set **Overlay size** in the panel. Double-click the grip to reset.

Burning money: press **Burn** in the panel (or B) to let banknotes fly across the screen and burn up, with the current cost per hour in the centre (e.g. "€272/h going up in flames"). The timer keeps running. A smaller burst plays each time the cost passes a multiple of **Burn every**: leave it empty for auto (about every 10 minutes at the current cost per hour, rounded to 1/2/5 × 10ⁿ, e.g. €50), enter an amount, or 0 to turn it off.

Planned length: a thin bar under the cost fills up over **Planned length (min)** (default 30). It turns amber at 80%; when the meeting runs over, the bar and the elapsed time turn red and the full burn plays once ("Overtime: €272/h going up in flames"). 0 turns it off.

URL parameters (browser only; OBS's **Local file** ignores them) override saved settings: `n`, `salary`, `factor`, `hours`, `cur` (EUR, USD, GBP, CHF), `pos` (br, bl, tr, tl), `scale` (0.4–4), `burn` (0 = off), `plan` (minutes, 0 = off), plus flags `overlay` (transparent background), `autostart` and `info` (show calculation details). Example: `meeting-cost.html?n=8&salary=70000&pos=tr&autostart`

## OBS + Teams

1. In OBS, add your webcam as a **Video Capture Device**.
2. Add a **Browser Source** above the webcam in the Sources list. Check **Local file** and select `meeting-cost.html`. Set width/height to your canvas size. The background is transparent automatically in OBS.
3. Right-click the source → **Interact**. Click inside the page, press H to open the settings and enter your values. Click the cost display (or press Space) to start/pause. Key presses in the main OBS window do not reach the page.
4. Click **Start Virtual Camera** in OBS.
5. In Teams, choose **OBS Virtual Camera** as your camera.

## License

[MIT](LICENSE)
