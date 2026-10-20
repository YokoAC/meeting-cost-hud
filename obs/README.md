# OBS setup for video calls

Puts the Meeting Cost HUD over your webcam in OBS Studio and sends it via OBS Virtual Camera to any app that accepts a webcam: Microsoft Teams, Zoom, Google Meet, Webex, … Tested on Windows with OBS 32.2.2 and the new Microsoft Teams; the Zoom and Google Meet steps are untested. OBS's menus are the same on macOS and Linux; the NVIDIA filter and the Teams folder paths are Windows-only.

Files in this folder:

- `meeting-cost-hud.json`: ready-made OBS scene collection (HUD, webcam with NVIDIA Background Removal, test background).
- `test-background.png`: 1920x1080 test background. Square grid and round circle mean the aspect ratio is correct; the blue corner marks sit at the HUD's 24 px margin.

## Option A: import the ready-made scene

1. **Canvas first:** OBS → Settings → Video: Base and Output resolution **1920x1080**, 30 FPS. The scene is laid out for this size.
2. **Import:** Scene Collection → **Import** → select `obs/meeting-cost-hud.json`, then Scene Collection → **Meeting Cost HUD**.
3. **Missing files:** OBS asks for `meeting-cost.html` and `obs/test-background.png` unless the repository is at `C:\Development\meeting-cost-hud`. Point each entry to the file in your copy.
4. **Webcam:** double-click **Webcam** → Device → pick your camera. Resolution is preset to 1280x720 (Custom).
5. **Background removal:** the webcam has the **NVIDIA Background Removal** filter, which needs Windows, an NVIDIA RTX card and the NVIDIA Video Effects SDK (see [Background](#background-optional)). Without it, remove the filter (right-click Webcam → Filters); the webcam then covers the background image.
6. Continue with [Use it in a video call](#use-it-in-a-video-call).

## Option B: set it up by hand

1. **Canvas:** OBS → Settings → Video: Base and Output resolution 1280x720 (or 1920x1080), 30 FPS. Keep it 16:9: video call tiles are 16:9, so a 4:3 canvas looks stretched.
2. **Webcam:** Sources → + → **Video Capture Device**. Properties → Resolution/FPS Type = **Custom**, pick a 16:9 resolution. Right-click → Transform → **Reset Transform**, then **Fit to screen**.
3. **HUD:** Sources → + → **Browser**, above the webcam. Check **Local file** and select `meeting-cost.html`.
   - Width/Height in the canvas aspect ratio, e.g. 1280x720. A smaller page makes the HUD larger on the canvas; a different ratio gets letterboxed and the HUD floats off the edge.
   - Uncheck **Shutdown source when not visible** and **Refresh browser when scene becomes active**, otherwise the timer resets.
   - Right-click → Transform → **Reset Transform**, then **Fit to screen**.
   - The background is transparent automatically in OBS.

## Use it in a video call

1. **Settings and control:** right-click the browser source → **Interact**, click inside the page, press H and enter your values. Click the cost display (or press Space) to start/pause. Key presses in the main OBS window do not reach the page.
2. **Virtual camera:** click **Start Virtual Camera** in OBS. Stop it before changing the canvas resolution.
3. **Call app:** pick **OBS Virtual Camera** as your camera and turn background effects off (they cut out the HUD, see [Background](#background-optional)). Restart the app, or reload the browser tab for Google Meet, if the camera is missing or shows an old picture.

| App | Camera | Background effects | Your own preview |
|---|---|---|---|
| Microsoft Teams (tested) | Settings → Devices → Camera | Video effects → **None** | Mirrored; turn off **Mirror my video** to see it as others do |
| Zoom (untested) | Settings → Video → Camera | Settings → Background & effects → **None** | Mirrored; turn off **Mirror my video** in Settings → Video |
| Google Meet (untested) | ⋮ → Settings → Video → Camera | Apply visual effects → off | Always mirrored for you, no setting |

Others always see the HUD the right way round, whatever your own preview shows.

## Background (optional)

Background effects of the call app (Teams, Zoom, Meet, …) cut out everything except you, including the HUD. Turn them off and do the background in OBS instead:

1. Source order, top to bottom: **Browser** (HUD) → **Webcam** with a background-removal filter → **Image** (your background, Transform → **Stretch to screen**). The imported scene already has this order.
2. Background removal on an NVIDIA RTX card (Windows): install the **NVIDIA Video Effects SDK** redistributable for your GPU series (NVIDIA Broadcast SDK resources page), restart OBS, then webcam → Filters → Effect Filters → **NVIDIA Background Removal**.
3. To reuse a background you uploaded to Teams (Windows), look in `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\Backgrounds\Uploads` (new Teams) or `%APPDATA%\Microsoft\Teams\Backgrounds\Uploads` (classic Teams). Backgrounds pushed by your company may be stored elsewhere.
