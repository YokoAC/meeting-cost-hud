# Meeting Cost HUD

Live meeting cost timer in a single HTML file. Works offline, no dependencies.

## Usage

Open `meeting-cost.html` in a browser. Settings start hidden: hover the overlay and click ⚙ (or press H). Enter participants, average annual salary, employer cost factor and working hours per year, then press **Start** or click the overlay. Settings are saved automatically.

Hotkeys: Space start/pause · R reset · `+`/`-` participants · I show/hide calculation details · H or Esc show/hide panel. Click inside the page first so it receives key presses.

Mouse: click the overlay to start/pause; hover it to reveal the ⚙ (settings panel) and the corner grip.

Resize: hover the overlay and drag the corner grip, or set **Overlay size** in the panel. Double-click the grip to reset.

URL parameters (browser only; OBS's **Local file** ignores them) override saved settings: `n`, `salary`, `factor`, `hours`, `cur` (EUR, USD, GBP, CHF), `pos` (br, bl, tr, tl), `scale` (0.4–4), plus flags `overlay` (transparent background), `autostart` and `info` (show calculation details). Example: `meeting-cost.html?n=8&salary=70000&pos=tr&autostart`

## OBS + Teams

1. In OBS, add your webcam as a **Video Capture Device**.
2. Add a **Browser Source** above the webcam in the Sources list. Check **Local file** and select `meeting-cost.html`. Set width/height to your canvas size. The background is transparent automatically in OBS.
3. Right-click the source → **Interact**. Click inside the page, press H to open the settings and enter your values. Click the cost display (or press Space) to start/pause. Key presses in the main OBS window do not reach the page.
4. Click **Start Virtual Camera** in OBS.
5. In Teams, choose **OBS Virtual Camera** as your camera.

## License

[MIT](LICENSE)
