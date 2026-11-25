# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/4orky/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/4orky/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up Thursday, 26 November 2026 in a single image. The lead is the day's own event: the 100th Macy's Thanksgiving Day Parade marches through New York on Thanksgiving Day, with a record 100 balloons and a nor'easter threatening to ground them. Around it, the world as reported that morning: troops free all 20 hostages from a Cartagena supermarket after a 17-hour siege; Australia and Solomon Islands sign a sweeping security treaty; leaked Russian statistics put the war dead in Ukraine at nearly 500,000; Malaysia sues Google for $146 million; Bangladesh garment workers win a 36% pay rise; and India marks Constitution Day.

## Run it

```sh
python3 main.py
```

This writes the entry image to `/output/entry.png` (1024×1024 PNG, 131,355 bytes, deterministic — every run produces byte-identical output).

`render.py` is the program that drew the front page (Pillow, render time only); `main.py` is the standard-library-only entrypoint that copies the finished image into place.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
