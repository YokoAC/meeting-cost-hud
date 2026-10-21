"""Records the README demo video: demo/out/demo.mp4 (see demo/README.md).

Runs the real meeting-cost.html in Chromium over a stand-in webcam picture and
fast-forwards meeting time, so dragging, burn thresholds, halfway, "5 min left",
quiet display, a manual burn and overtime all fit into about 45 seconds.
Nothing is installed into the repository; uv fetches Playwright and a temporary
ffmpeg:

    uv run --no-project --with playwright playwright install chromium   # once
    uv run --no-project --with playwright --with imageio-ffmpeg demo/record.py
"""

import shutil
import subprocess
import time
from pathlib import Path

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo" / "out"
W, H = 1280, 720
# 10 people, a €40 burn threshold and a 12-minute plan put every event within 12 minutes of meeting time,
# with bursts at €40 (before halfway) and €80 (before overtime) that don't collide with the reminders
URL = (ROOT / "meeting-cost.html").as_uri() + "?overlay&n=10&salary=65000&burn=40&plan=12&pos=br&scale=1.15"

# Stand-in webcam (a person silhouette in a room), keycap hints and title cards. Injected before the
# page's own script; the page itself is not changed.
STAGE = """
document.addEventListener('DOMContentLoaded', () => {
  const css = document.createElement('style');
  css.textContent = `
    #cam { position: fixed; inset: 0; z-index: -1; overflow: hidden;
           background: radial-gradient(circle at 15% 30%, #6d7f95 0, transparent 45%),
                       linear-gradient(160deg, #4b5a6b, #232c36 70%); }
    #cam svg { position: absolute; left: 50%; bottom: 0; width: 640px; transform: translateX(-55%); }
    #key { position: fixed; left: 50%; bottom: 40px; transform: translateX(-50%); z-index: 7;
           display: flex; gap: 12px; align-items: center; opacity: 0; transition: opacity .2s;
           background: #000c; padding: 10px 16px; border-radius: 12px; border: 1px solid #333; }
    #key.on { opacity: 1; }
    #key .cap { font: 700 20px system-ui; color: #111; background: linear-gradient(#f4f4f4, #c9c9c9);
                border-radius: 8px; padding: 8px 12px; box-shadow: 0 3px 0 #888; min-width: 44px; text-align: center; }
    #key .what { font: 600 18px system-ui; color: #fff; }
    #card { position: fixed; inset: 0; z-index: 9; background: #0d0d10; color: #f2f2f2; display: flex;
            flex-direction: column; align-items: center; justify-content: center; gap: 14px;
            text-align: center; transition: opacity .35s; }
    #card.gone { opacity: 0; pointer-events: none; }  /* else the faded card swallows the mouse drag */
    #card h1 { font: 800 52px "Segoe UI", system-ui; margin: 0; }
    #card h1 span { color: #e3b341; }
    #card p { font: 22px "Segoe UI", system-ui; color: #aab; margin: 0; max-width: 900px; }
    #card .url { font: 600 20px Consolas, monospace; color: #58a6ff; }`;
  document.head.append(css);
  document.body.insertAdjacentHTML('afterbegin', `
    <div id="cam"><svg viewBox="0 0 640 520"><g fill="#1b2128">
      <circle cx="320" cy="170" r="110"/><path d="M60 520 C60 330 170 290 320 290 C470 290 580 330 580 520Z"/></g></svg></div>
    <div id="key"><span class="cap"></span><span class="what"></span></div>
    <div id="card"><h1>Meeting Cost <span>HUD</span></h1>
      <p>Live meeting cost overlay for OBS Studio and your video calls</p></div>`);
});
window.__key = (cap, what) => {
  const el = document.getElementById('key');
  el.querySelector('.cap').textContent = cap;
  el.querySelector('.what').textContent = what;
  el.classList.add('on');
  clearTimeout(window.__kt);
  window.__kt = setTimeout(() => el.classList.remove('on'), 1500);
};
window.__card = html => {
  const c = document.getElementById('card');
  if (html) { c.innerHTML = html; c.classList.remove('gone'); } else c.classList.add('gone');
};
"""

# Fast-forward to a meeting time: adds time and the cost for it in small steps, so milestones and burn
# thresholds fire on the way exactly as they would in real time. Uses the page's own globals.
FF = """([target, ms]) => new Promise(done => {
  const el = acc + (running ? performance.now() - t0 : 0);
  const steps = Math.max(1, Math.round(ms / 40)), d = Math.max(0, target * 1000 - el) / steps;
  let i = 0;
  const iv = setInterval(() => {
    const c = cfg();
    acc += d; costAcc += c.n * c.salary * c.factor / c.hours / 3600 * d / 1000;
    if (++i >= steps) { clearInterval(iv); done(); }
  }, 40);
})"""

END_CARD = """<h1>Meeting Cost <span>HUD</span></h1>
  <p>Single HTML file · works offline · burn animations · planned length and reminders</p>
  <div class="url">github.com/YokoAC/meeting-cost-hud</div>"""


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": W, "height": H},
                                      record_video_dir=str(OUT), record_video_size={"width": W, "height": H})
        page = context.new_page()
        page.add_init_script(STAGE)
        t0 = time.monotonic()
        page.goto(URL)
        page.wait_for_selector("#card")
        visible = time.monotonic() - t0  # video time at which the title card is on screen

        def key(cap, what, press, times=1, gap=0.25):
            page.evaluate("([c, w]) => window.__key(c, w)", [cap, what])
            for _ in range(times):
                # type() sends the character itself ("+" is a combination separator for press())
                page.keyboard.press(press) if press == "Space" else page.keyboard.type(press)
                time.sleep(gap)

        def ff(mm_ss, seconds):  # fast-forward to meeting time "mm:ss" within `seconds`
            m, s = map(int, mm_ss.split(":"))
            page.evaluate(FF, [m * 60 + s, seconds * 1000])

        def at(seconds):
            time.sleep(seconds)

        def drag_top_right():  # real mouse drag in small steps, so the snap guides show; released a bit off the spot
            page.evaluate("([c, w]) => window.__key(c, w)", ["Drag", "move the overlay"])
            x, y, w, h = page.evaluate("(() => { const r = box(); return [r.left + r.width / 2, r.top + r.height / 2, r.width, r.height] })()")
            tx, ty = W - 24 - w / 2 - 30, 24 + h / 2 + 20
            page.mouse.move(x, y)
            page.mouse.down()
            for i in range(1, 41):
                page.mouse.move(x + (tx - x) * i / 40, y + (ty - y) * i / 40)
                time.sleep(0.03)
            time.sleep(0.5)
            page.mouse.up()
            page.mouse.move(W / 2, H / 2)  # leave the HUD, so its hover-only gear and grip disappear again

        at(1.6)
        page.evaluate("window.__card(null)")
        at(0.8)
        key("H", "settings", "h")
        at(1.8)
        key("H", "hide settings", "h")
        at(0.8)
        drag_top_right()          # snap guides, snaps into the top-right spot
        at(1.6)
        key("Space", "start the meeting", "Space")
        at(2.2)
        ff("05:30", 2.5)          # cost climbing; €40 burst at ~05:18
        at(2.0)
        ff("06:00", 0.6)          # halfway reminder (4 s on screen)
        at(4.3)
        ff("07:00", 1.0)          # 5 min left
        at(2.0)
        key("+", "more people join", "+", times=3, gap=0.35)
        at(1.6)
        key("Q", "quiet display", "q")   # cost hidden, keeps counting
        at(2.6)
        key("Q", "full display again", "q")
        at(1.4)
        key("B", "burn money", "b")
        at(4.0)
        ff("10:00", 1.5)          # €80 burst at ~09:45
        at(2.2)
        ff("12:00", 1.2)          # overtime: bar and time turn red, the full burn plays
        at(4.3)
        page.evaluate("html => window.__card(html)", END_CARD)
        at(2.0)

        video = page.video
        context.close()
        browser.close()
        raw = video.path()

    mp4 = OUT / "demo.mp4"
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-y", "-ss", f"{visible + 0.1:.2f}",
                    "-i", raw, "-vf", "fps=30,format=yuv420p", "-an", "-c:v", "libx264", "-preset", "veryslow",
                    "-crf", "25", "-movflags", "+faststart", str(mp4)], check=True)
    Path(raw).unlink()
    print(f"wrote {mp4}")


if __name__ == "__main__":
    main()
