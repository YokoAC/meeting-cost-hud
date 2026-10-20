# OBS + Microsoft Teams setup (Windows)

Puts the Meeting Cost HUD over your webcam in OBS Studio and sends it to Microsoft Teams via OBS Virtual Camera. Tested with OBS 32.2.2 and the new Microsoft Teams.

Files in this folder:

- `meeting-cost-hud.json`: ready-made OBS scene collection (HUD, webcam with NVIDIA Background Removal, test background).
- `test-background.png`: 1920x1080 test background. Square grid and round circle mean the aspect ratio is correct; the blue corner marks sit at the HUD's 24 px margin.

## Option A: import the ready-made scene

1. **Canvas first:** OBS → Settings → Video: Base and Output resolution **1920x1080**, 30 FPS. The scene is laid out for this size.
2. **Import:** Scene Collection → **Import** → select `obs/meeting-cost-hud.json`, then Scene Collection → **Meeting Cost HUD**.
3. **Missing files:** OBS asks for `meeting-cost.html` and `obs/test-background.png` unless the repository is at `C:\Development\meeting-cost-hud`. Point each entry to the file in your copy.
4. **Webcam:** double-click **Webcam** → Device → pick your camera. Resolution is preset to 1280x720 (Custom).
5. **Background removal:** the webcam has the **NVIDIA Background Removal** filter, which needs an NVIDIA RTX card and the NVIDIA Video Effects SDK (see [Background](#background-optional)). Without it, remove the filter (right-click Webcam → Filters); the webcam then covers the background image.
6. Continue with [Use it in Teams](#use-it-in-teams).

## Option B: set it up by hand

1. **Canvas:** OBS → Settings → Video: Base and Output resolution 1280x720 (or 1920x1080), 30 FPS. Keep it 16:9: Teams tiles are 16:9, so a 4:3 canvas looks stretched.
2. **Webcam:** Sources → + → **Video Capture Device**. Properties → Resolution/FPS Type = **Custom**, pick a 16:9 resolution. Right-click → Transform → **Reset Transform**, then **Fit to screen**.
3. **HUD:** Sources → + → **Browser**, above the webcam. Check **Local file** and select `meeting-cost.html`.
   - Width/Height in the canvas aspect ratio, e.g. 1280x720. A smaller page makes the HUD larger on the canvas; a different ratio gets letterboxed and the HUD floats off the edge.
   - Uncheck **Shutdown source when not visible** and **Refresh browser when scene becomes active**, otherwise the timer resets.
   - Right-click → Transform → **Reset Transform**, then **Fit to screen**.
   - The background is transparent automatically in OBS.

## Use it in Teams

1. **Settings and control:** right-click the browser source → **Interact**, click inside the page, press H and enter your values. Click the cost display (or press Space) to start/pause. Key presses in the main OBS window do not reach the page.
2. **Virtual camera:** click **Start Virtual Camera** in OBS. Stop it before changing the canvas resolution.
3. **Teams:** Settings → Devices → Camera → **OBS Virtual Camera**. Restart Teams if the camera is missing or shows an old picture. Your own preview is mirrored; turn off **Mirror my video** to see it as others do.

## Background (optional)

Teams background effects cut out everything except you, including the HUD. Set Teams effects to **None** and do the background in OBS instead:

1. Source order, top to bottom: **Browser** (HUD) → **Webcam** with a background-removal filter → **Image** (your background, Transform → **Stretch to screen**). The imported scene already has this order.
2. Background removal on an NVIDIA RTX card: install the **NVIDIA Video Effects SDK** redistributable for your GPU series (NVIDIA Broadcast SDK resources page), restart OBS, then webcam → Filters → Effect Filters → **NVIDIA Background Removal**.
3. To reuse a background you uploaded to Teams, look in `%LOCALAPPDATA%\Packages\MSTeams_8wekyb3d8bbwe\LocalCache\Microsoft\MSTeams\Backgrounds\Uploads` (new Teams) or `%APPDATA%\Microsoft\Teams\Backgrounds\Uploads` (classic Teams). Backgrounds pushed by your company may be stored elsewhere.
