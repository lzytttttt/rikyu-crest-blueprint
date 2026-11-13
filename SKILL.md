---
name: rikyu-crest-blueprint
description: Convert uploaded images, photos, statues, animals, or design concepts into Rikyu-style geometric crest and Japanese kamon construction blueprint posters in pure SVG. Use when the user uploads an image to turn into an SVG geometric sketch, or asks to replicate or create a Rikyu-style emblem poster, compass-and-straightedge logo blueprint, or golden-ratio geometric grid illustration with construction circles and extended tangent rays.
---
# Rikyu Crest Blueprint

Transform uploaded reference images or text concepts into minimalist heraldic crests and Japanese kamon emblems presented as architectural compass-and-straightedge construction sheets in pure SVG. Each output combines a central translucent silhouette overlaid with its synchronized geometric construction circles and extended tangent rays, a fading millimeter grid, a concise design concept note, and a finished solid emblem preview in the bottom-right corner.

## Bundled Resources

- `assets/rikyu_origami_crane_kamon.svg`: Complete reference SVG poster demonstrating the Origami-Inspired Soaring Crane Kamon (Orizuru and Maizuru crest), including the fading 10px/50px millimeter grid, `<defs><g id="crest-shape">` dual-state instantiation, synchronized osculating circles with radius callouts, extended straightedge rays, Rikyu header mark, and editorial concept footer.
- `scripts/build_crane_svg.py`: Reference Python generator script showing how to compute exact circular arc endpoints (`x = cx + r * cos(theta)`, `y = cy + r * sin(theta)`), true continuous spiral cutouts, and extended tangent/secant line projections (`P1 +/- 1200 * u`) from a single Primitive Construction Registry.

## When to Use

- The user uploads an image (photo, statue, animal, object, or reference poster) and asks to convert or replicate it as a Rikyu-style SVG geometric sketch or construction blueprint.
- The user wants a Rikyu-style geometric construction poster, Japanese kamon blueprint, or golden-ratio logo sheet in SVG.
- The user asks to design an animal, mythological creature, botanical motif, or abstract symbol with visible compass-and-straightedge construction lines and circles.

## Steps

### 1. Deconstruct the Input Image or Concept into Geometric Primitives

Before writing SVG paths, extract the underlying mathematical skeleton from the uploaded image or subject:

- **Select Framing Archetype**:

  - **Enclosed Circular Kamon**: Wrap the subject inside an outer circular ring (`r="165"` to `r="185"`), ideal for winged, coiled, swirling, or rotational motifs (such as the Nihonbashi winged kirin or the origami soaring crane in `assets/rikyu_origami_crane_kamon.svg`).
  - **Freestanding Heraldic Crest**: Anchor the subject on a strong horizontal baseline (`y="120"` relative to center) and build around a dominant diagonal axis, ideal for standing beasts, statues, or architectural forms (such as the roaring lion on a rock).

- **Distill into Flat Minimal Masses**: Convert photographic shading and complex textures into 4 to 8 high-contrast, flat geometric silhouette islands separated by uniform negative-space channels (`6px` to `10px` wide at full scale) rather than internal sketch lines.
- **Build a Primitive Construction Registry**: Define every primary contour curve using explicit circular arcs (`cx, cy, r`) and every straight edge, baseline, or posture axis using line endpoints (`x1, y1, x2, y2`) in a local coordinate space centered at `(0, 0)` spanning `[-185, 185]`. Record these coordinates first so the silhouette `<path>` and the construction overlay share identical geometry.

### 2. Set Up the SVG Canvas and Fading Millimeter Grid

Use a vertical poster aspect ratio (`viewBox="0 0 800 1000"`):

- **Color Tokens**:

  - Background paper: `#F4F1EA`
  - Sub-grid (`10px`): `#E2DDD3` (`stroke-width="0.6"`)
  - Major grid (`50px`): `#D2CCC0` (`stroke-width="0.9"`)
  - Outer frame and preview border hairlines: `#C6C0B4` (`stroke-width="1"`)
  - Translucent central motif: `fill="#8C877E" fill-opacity="0.38" stroke="#4A463F" stroke-width="1.25"`
  - Construction circles and extended rays: `stroke="#5C574F" stroke-width="0.75" stroke-opacity="0.72"`
  - Solid final emblem and header mark: `#3A3631`
  - Concept body text: `#6E6A63`

- **Grid Fade Mask**: Apply a `<linearGradient>` mask (`y1="0"` to `y2="1"`) to the grid layer so the millimeter grid covers the upper blueprint area (`y="40"` to `y="740"`) and softly fades into the plain paper background between `y="640"` and `y="750"`.

### 3. Build the Reusable Emblem `<g id="crest-shape">`

Define the emblem geometry inside `<defs>` as `<g id="crest-shape">` centered at `(0, 0)` so it can be instantiated twice without geometric drift:

1. **Central Blueprint Instance**: Instantiate via `<use href="#crest-shape" transform="translate(400, 385)" fill="#8C877E" fill-opacity="0.38" stroke="#4A463F" stroke-width="1.25"/>`.
2. **Bottom-Right Finished Emblem Instance**: Instantiate inside the preview box via `<use href="#crest-shape" transform="translate(660, 860) scale(0.32)" fill="#3A3631" stroke="none"/>`.

Construct all `<path>` elements using exact circular arc commands (`A r r 0 large-arc-flag sweep-flag x y`) and straight segments (`L x y`) calculated directly from the Primitive Construction Registry (`x = cx + r * cos(theta)`, `y = cy + r * sin(theta)`). Use compound paths (`fill-rule="evenodd"`) or `<mask>` cutouts for negative-space channels and inner spiral scrolls so both the translucent central state and the solid preview render cleanly.

### 4. Render Synchronized Construction Circles and Extended Rays

Clip all construction geometry to the inner frame (`<clipPath id="blueprint-clip"><rect x="40" y="40" width="720" height="720"/></clipPath>`) and group them under `transform="translate(400, 385)"`:

- **Osculating Construction Circles**: For every circular arc in the Primitive Construction Registry (typically 14 to 24 circles with radii from `r="10"` to `r="240"`), draw `<circle cx="..." cy="..." r="..." fill="none" stroke="#5C574F" stroke-width="0.82" stroke-opacity="0.76"/>`.
- **Center Crosshairs and Radius Callouts**: At each circle center `(cx, cy)`, render a `7px` crosshair (`M cx-3.5 cy H cx+3.5 M cx cy-3.5 V cy+3.5`) with `stroke="#4A463F" stroke-width="0.85"`, and add horizontal radius callout lines (`(cx, cy)` to `(cx+r, cy)`) with a `6px` vertical end-tick on key primary circles.
- **Extended Secant and Tangent Rays**: For each straight edge, baseline, and primary posture axis (typically 12 to 20 lines), project the line direction vector `(dx, dy)` across the entire canvas (`P1 - 1200 * u` to `P1 + 1200 * u`, where `u` is the unit vector) so `clip-path="url(#blueprint-clip)"` trims every ray cleanly at the frame border.

### 5. Compose the Editorial Header and Footer Layout

- **Outer Frame**: Draw `<rect x="40" y="40" width="720" height="920" fill="none" stroke="#C6C0B4" stroke-width="1"/>`.
- **Top Header (`y="85"`)**: Center the minimal silhouette icon and serif brand title (`Rikyu` by default, or user-specified title) around `x="400"`.
- **Bottom-Left Concept Block (`x="76", y="810"`)**:

  - Render `CONCEPT` in uppercase sans-serif (`font-size="13"`, `letter-spacing="2.8"`, `font-weight="600"`, `fill="#4A463F"`).
  - Below it (`y="846"`), place 3 to 4 lines of `<text>` explaining how the uploaded image's posture, primary axis, and flat geometric masses were distilled into the emblem (in Chinese, Japanese, or English matching the user's preference).

- **Bottom-Right Preview Box**:

  - Draw the inset square `<rect x="560" y="760" width="200" height="200" fill="#F4F1EA" stroke="#C6C0B4" stroke-width="1"/>`.
  - Render the solid scaled `#crest-shape` centered at `(660, 860)`.

## Gotchas

- **Never draw arbitrary decorative circles**: Every construction circle and extended ray must be mathematically tangent or secant to an actual curve or edge of the silhouette. Derive path arc endpoints directly from `(cx, cy, r)` so the construction circles hug the silhouette contours accurately.
- **Avoid opaque paper-colored strokes inside translucent groups**: If you use `#F4F1EA` strokes to carve negative space, applying `fill-opacity="0.38"` to the group reveals the stroke over the grid. Instead, use separate closed `<path>` islands, compound paths (`fill-rule="evenodd"`), or an SVG `<mask>` for negative-space channels.
- **Maintain legible negative-space width and open background balance**: Keep gaps between `6px` and `10px` at full scale (`[-185, 185]`) so they do not close up when scaled down to `0.32` in the bottom-right preview box, and preserve generous open negative space around the head and tail so the emblem reads as an iconic crest rather than a radial wheel.
