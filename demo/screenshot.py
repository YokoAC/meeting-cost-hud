"""Renders the README's controls picture: docs/controls.png.

The real meeting-cost.html in Chromium: the HUD mid-meeting, and above it the settings panel cut down to its
header and the hotkey list. Transparent background, 2x pixels. Run from the repository root after UI changes:

    uv run --no-project --with playwright demo/screenshot.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "controls.png"
URL = (ROOT / "meeting-cost.html").as_uri() + "?overlay&n=8&salary=70000&plan=30&pos=br"

# only the panel header and the hotkey list stay visible (no double rule under the header); no fade mid-screenshot
TRIM = ("#panel label, #panel .note, #panel .row, #fx { display: none !important; }"  # #fx: no labels or bursts from the jump in time
        "#panel { transition: none !important; } #panel .hint { margin-top: 0; border-top: 0; }")

# 12 min into a 30-minute meeting with 8 people: cost, time and the planned-length bar all show something
STATE = """() => {
  document.body.classList.remove('hidepanel');
  toggle();  // running, for the green dot
  acc = (12 * 60 + 34) * 1000; t0 = performance.now(); costAcc = 8 * 70000 * 1.2 / 1720 * (12 * 60 + 34) / 3600; tick();
}"""


def main():
    OUT.parent.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--lang=en-US"])
        page = browser.new_page(viewport={"width": 800, "height": 900}, device_scale_factor=2, locale="en-US")
        page.goto(URL)
        page.add_style_tag(content=TRIM)
        page.evaluate(STATE)
        page.wait_for_timeout(300)
        page.locator("#dock").screenshot(path=str(OUT), omit_background=True)
        browser.close()
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
