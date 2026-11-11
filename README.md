# Companion Plot

Türkçe: [README.tr.md](README.tr.md)

**Companion Plot is a garden-bed puzzle: drop plants into a bed and watch which neighbours help each other and which ones fight, with a live score telling you how well your garden would do.**

It opens already full of plants, so you can start poking right away. Tap a plant, tap a square, and the bed lights up green (happy neighbours) or red (squabbling ones). Pick a sowing month and plants that are out of season get a snowflake. Stuck? Ask for a suggestion for any square.

No account, no install of extra packages, no settings. It runs on your own computer and nothing leaves it.

## Run it

You only need Python 3.8 or newer.

```
python3 -m companion_plot
```

Your browser opens on its own. If it does not, open the address printed in the terminal (usually `http://127.0.0.1:8765/`). Press Ctrl+C in the terminal to stop.

## Language

Use the **TR | EN** button at the top right of the page; the whole page switches instantly and remembers your choice. The first visit follows your browser language. In the terminal, pass `--lang tr` or `--lang en` (otherwise it follows your system language, falling back to English).

## How to play

1. Pick a plant from the row under the bed (or the eraser).
2. Tap squares in the bed to plant it. Tapping a square that already holds the same plant clears it.
3. Watch the score on the right. Green squares have friendly neighbours, red ones have enemies. The small number on a square is its mood.
4. Choose the sowing month. Plants that cannot be sown then get a dashed blue border and a snowflake, and cost you points.
5. Tap **Suggest for selected square** to get the crop that raises the whole bed's score the most.
6. The harvest calendar at the bottom shows when each plant in your bed can be sown and when the basket (🧺) is ready.

### How the score works

| Situation | Points |
| --- | --- |
| Two friendly plants side by side (up, down, left, right) | +2 |
| Two enemy plants side by side | -3 |
| Same plant side by side (pests spread) | -1 |
| A plant sown outside its season | -2 |
| Variety bonus, one per distinct plant, up to 6 | +1 each |

The total is averaged over the planted squares and scaled to 0-100.

## Command line options

```
python3 -m companion_plot [--lang tr|en] [--port 8765] [--no-browser] [--show]
```

- `--lang` terminal language.
- `--port` first port to try; if it is taken the next free one is used.
- `--no-browser` do not open the browser.
- `--show` print the sample bed and its score in the terminal, then exit.

## Project layout

- `companion_plot/data.py` the plants, sowing months and friend/enemy table.
- `companion_plot/engine.py` scoring, harvest months and square suggestions.
- `companion_plot/strings.py` every text in Turkish and English, in one table.
- `companion_plot/server.py` small standard-library HTTP server (JSON API plus the page).
- `companion_plot/web/` the page itself: HTML, CSS and plain JavaScript.
- `tests/` unit tests.

Run the tests with:

```
python3 -m unittest discover -s tests -t .
```

## Notes and limits

The plant pairings follow common gardening folklore and are meant as a game, not agronomic advice. Sowing months assume a northern-hemisphere temperate climate.

## About

Inspired by the idea of farm record keeping (such as farmOS), but it is its own small thing: a toy for thinking about who should sit next to whom. Parts of this project were developed with the help of AI tools (Claude).
