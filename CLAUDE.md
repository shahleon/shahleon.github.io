# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm install       # install dependencies (first time)
npm run dev       # local dev server at http://localhost:3000
npm run build     # static export to out/
npm run lint      # ESLint
```

## Deployment

GitHub Actions deploys on every push to `main` (see `.github/workflows/deploy.yml`).
The build runs `next build`, which writes static files to `out/`.

Before the first deploy, enable Pages in the GitHub repo:
**Settings > Pages > Source: GitHub Actions**

The repo must be named `shahleon.github.io` for the site to be served at `shahleon.github.io`.

## Stack

- Next.js 14, App Router, TypeScript, Tailwind CSS v3
- Static export (`output: 'export'` in `next.config.js`)
- No runtime server; everything is HTML/CSS/JS

## Structure

```
src/
  app/
    layout.tsx        root layout and metadata
    page.tsx          imports and assembles section components
    globals.css       Tailwind directives + smooth scroll
  components/
    Nav.tsx           sticky navigation
    Hero.tsx          headshot, bio, contact links
    Research.tsx      four project cards (data defined inline)
    Publications.tsx  publication list (data defined inline)
    Experience.tsx    professional timeline (data defined inline)
    CVSection.tsx     CV download
    Footer.tsx        links
public/
  headshot-leon.jpg
  resume.pdf
  animations/
    l2n/              frame-01.svg … frame-10.svg
    pfis-t/           pfist-A01..A10.svg, pfist-B01..B04.svg
    collective/       collective-panel-1..3.svg, collective-pipeline.svg
animations-src/
  l2n/build.py        source scripts — edit these, then regenerate SVGs
  pfis-t/build.py
  collective/build.py
```

## Color palette

Defined in `tailwind.config.js` and used via Tailwind classes:

| Token        | Hex       | Use                        |
|---|---|---|
| `individual` | `#2E6DB4` | L2N project accent         |
| `social`     | `#7B3FB8` | Diets + PFIS-T accent      |
| `collective` | `#0E8A6A` | Collective priors accent   |
| `ink`        | `#1A1A1A` | Body text                  |
| `muted`      | `#5F6368` | Secondary text             |
| `line`       | `#D0D4D9` | Borders                    |
| `panel`      | `#F7F8F9` | Alternate section bg       |

## Research section

Project data lives in `src/components/Research.tsx` as the `projects` array.
Each card has a `placeholderLabel` field and a dashed placeholder box. When adding
an actual animation or figure:
1. Add the SVG files (or component) to the card
2. Replace the placeholder `<div>` with the actual content
3. If using an SVG stepper, see `public/animations/` and the L2N player pattern in
   `animations-src/l2n/` for reference

Animations with illustrative data (L2N, PFIS-T, Collective) must be labeled
"Illustrative" on the site when embedded. The scores and weights shown are
for explanation, not from actual runs on those specific inputs.

## Content updates

All section content (projects, publications, experience) is defined as plain
TypeScript arrays at the top of each component file. No CMS or external data source.
To update a publication or add a role, edit the array in the relevant file.

## Key constraints

- Do not link to the dissertation PDF until it is in the NC State repository.
- Do not add publications beyond the four listed without Leon confirming them.
- The VL/HCC paper's published camera-ready misstates the LLM results; use only
  the numbers in `Research.tsx` (sourced from the dissertation, not the paper).
