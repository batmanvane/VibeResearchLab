# VibeResearchLab

A mathematical simulation comparing traditional academic research labs vs AI-augmented research labs. The model is grounded in published empirical data from independent studies.

## Overview

This project simulates 2 years of research activity in:
- **Traditional Lab**: 1 PI + 3 PhDs
- **Augmented Lab**: Same team with AI tools

The animation visualizes research directions, publications, and the productivity difference between both setups.

## Key Findings

The model predicts approximately **1.5x** productivity gain from AI augmentation — significantly lower than vendor claims of 10x+.

### Empirical Sources
| Study | Finding |
|-------|---------|
| Peng et al. 2023 | 55.8% faster on **simple** coding tasks (RCT) |
| METR Study | **0%** speedup for experienced developers |
| Noy & Zhang 2023 | +40% for below-median writers, ~0% for skilled |

**Key insight**: AI helps most with routine tasks (boilerplate code, drafting), not the hard problem-solving that moves research forward.

## Files

- `animation.html` — Interactive visualization
- `animation-concept.html` — Concept and guide explaining what the animation shows and how to read it
- `model-explanation.html` — Mathematical model with LaTeX equations
- `capture.js` — Puppeteer script to record animation as MP4
- `animation.mp4` — Pre-rendered video of the animation

## Running

Open the animation directly in your browser, or visit the live version:

**Live Demo**: https://batmanvane.github.io/VibeResearchLab/animation.html

### Generating the video

Requires Node.js, Puppeteer, and ffmpeg:

```bash
npm install
node capture.js
```

This captures 1440 frames at 16 fps (90 seconds) and encodes them to `animation.mp4`.

## Mathematical Model

The simulation uses per-task speedups rather than global multipliers:

$$\bar{s} = \sum_k f_k \cdot s_k$$

$$R(T) = \frac{1 + \eta_{aug}T/2}{1 + \eta_{trad}T/2} \cdot E[s_{eff}]$$

See `model-explanation.html` for full derivations.

## License

MIT License — See LICENSE file.

## Acknowledgments

- Mathematical model developed with assistance from Claude (Anthropic)
- Visualization built with vanilla HTML5 Canvas
- Grounded in published research from METR, Peng et al., Noy & Zhang, and Open Science Collaboration
