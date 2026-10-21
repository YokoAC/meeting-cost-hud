# Demo video

`record.py` records the demo video shown in the main README into `demo/out/demo.mp4` (gitignored): the real `meeting-cost.html` in Chromium over a stand-in webcam, with meeting time fast-forwarded through the features.

It needs [uv](https://docs.astral.sh/uv/), which fetches Playwright and a temporary ffmpeg; nothing is installed into the repository. From the repository root:

```bash
uv run --no-project --with playwright playwright install chromium
```

```bash
uv run --no-project --with playwright --with imageio-ffmpeg demo/record.py
```

To publish a new recording: drag `demo/out/demo.mp4` into a pull request comment or description on GitHub, copy the `https://github.com/user-attachments/assets/…` link it inserts, and replace the video link in the main `README.md`. The MP4 itself is not committed.
