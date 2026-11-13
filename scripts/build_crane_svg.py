import math
import os

# Output goes to <repo>/output/ so the script works from any checkout location.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "output")
INT_DIR = os.path.join(OUT_DIR, "intermediate")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(INT_DIR, exist_ok=True)

SVG_PATH = os.path.join(OUT_DIR, "rikyu_origami_crane_kamon.svg")

def pt_on_circle(cx, cy, r, deg):
    rad = math.radians(deg)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))

def fmt(val):
    return f"{val:.2f}"

def arc_cmd(r, end_pt, large_arc=0, sweep=1):
    return f"A {fmt(r)} {fmt(r)} 0 {large_arc} {sweep} {fmt(end_pt[0])} {fmt(end_pt[1])}"

def line_cmd(pt):
    return f"L {fmt(pt[0])} {fmt(pt[1])}"

def move_cmd(pt):
    return f"M {fmt(pt[0])} {fmt(pt[1])}"

def build_true_spiral_cutout(cx, cy):
    """
    Constructs a true continuous compass-arc spiral cutout (渦巻) using semicircular
    arcs of decreasing radii so it renders as an authentic kamon scroll rather than a bullseye.
    """
    # Outer spiral boundary going clockwise, then inner boundary returning counter-clockwise
    # Center around (cx, cy)
    # Using exact semicircular arcs:
    p0 = (cx - 24.0, cy + 4.0)
    p1 = (cx + 20.0, cy + 4.0)   # r = 22
    p2 = (cx - 12.0, cy + 4.0)   # r = 16
    p3 = (cx + 8.0,  cy + 4.0)   # r = 10
    p4 = (cx + 2.0,  cy + 4.0)   # inner tip cap r = 3
    p5 = (cx - 6.0,  cy + 4.0)   # r = 4
    p6 = (cx + 14.0, cy + 4.0)   # r = 10
    p7 = (cx - 18.0, cy + 4.0)   # r = 16
    return " ".join([
        move_cmd(p0),
        arc_cmd(22.0, p1, large_arc=0, sweep=1),
        arc_cmd(16.0, p2, large_arc=0, sweep=1),
        arc_cmd(10.0, p3, large_arc=0, sweep=1),
        arc_cmd(3.0,  p4, large_arc=0, sweep=1),
        arc_cmd(4.0,  p5, large_arc=0, sweep=0),
        arc_cmd(10.0, p6, large_arc=0, sweep=0),
        arc_cmd(16.0, p7, large_arc=0, sweep=0),
        arc_cmd(3.0,  p0, large_arc=0, sweep=1),
        "Z"
    ])

def build_crest_and_geometry():
    paths = []
    circles = []   # (cx, cy, r, has_radius_callout)
    rays = []      # (x1, y1, x2, y2)
    vertices = []  # (vx, vy)

    # ------------------------------------------------------------------
    # 1. OUTER KAMON RING (丸輪)
    # Outer r=176, Inner r=154.
    # Continuous elegant kamon ring with two crisp dynamic notches where the
    # crane's primary left wingtip and lower tail tip break into the ring border.
    # ------------------------------------------------------------------
    circles.append((0.0, 0.0, 176.0, True))
    circles.append((0.0, 0.0, 154.0, False))

    # Main Ring Segment 1: From deg -112 (top-left wingtip break) clockwise all the way to deg 126 (bottom-left tail break)
    r1_out_s = pt_on_circle(0, 0, 176, -110)
    r1_out_e = pt_on_circle(0, 0, 176, 124)
    r1_in_e  = pt_on_circle(0, 0, 154, 124)
    r1_in_s  = pt_on_circle(0, 0, 154, -110)
    paths.append(" ".join([
        move_cmd(r1_out_s),
        arc_cmd(176.0, r1_out_e, large_arc=1, sweep=1),
        line_cmd(r1_in_e),
        arc_cmd(154.0, r1_in_s, large_arc=1, sweep=0),
        "Z"
    ]))

    # Left Ring Segment 2: From deg 130 clockwise to deg -115 (framing the left wing)
    r2_out_s = pt_on_circle(0, 0, 176, 129)
    r2_out_e = pt_on_circle(0, 0, 176, -115)
    r2_in_e  = pt_on_circle(0, 0, 154, -115)
    r2_in_s  = pt_on_circle(0, 0, 154, 129)
    paths.append(" ".join([
        move_cmd(r2_out_s),
        arc_cmd(176.0, r2_out_e, large_arc=0, sweep=1),
        line_cmd(r2_in_e),
        arc_cmd(154.0, r2_in_s, large_arc=0, sweep=0),
        "Z"
    ]))

    # ------------------------------------------------------------------
    # 2. SCULPTED CRANE HEAD, SLENDER ARCHED NECK, BEAK & CENTRAL TORSO
    # Built as a unified, iconic crane body-and-neck silhouette with a sharp
    # origami diamond chest, crowned head, long pointed beak, eye cutout,
    # and true kamon spiral scroll cutout in the breast!
    # ------------------------------------------------------------------
    # Neck outer circle: C_neck_out = (56, -24, r=78)
    # Neck inner circle: C_neck_in  = (78, -28, r=58)
    # Head crown circle: C_crown    = (36, -86, r=20)
    # Breast curve:      C_breast   = (-8, 18, r=68)
    # Belly lower curve: C_belly    = (-14, 12, r=74)
    circles.append((56.0, -24.0, 78.0, True))
    circles.append((78.0, -28.0, 58.0, True))
    circles.append((36.0, -86.0, 20.0, False))
    circles.append((-8.0, 18.0, 68.0, True))
    circles.append((-14.0, 12.0, 74.0, False))

    # Key points along the unified Head-Neck-Torso silhouette:
    p_shoulder_L  = (-20.0, -8.0)                        # Base of back neck
    p_head_back   = pt_on_circle(56, -24, 78, -118)      # (19.4, -92.9)
    p_crest_notch = (12.0, -98.0)                        # Sharp origami red-crown crest tip!
    p_crown_top   = pt_on_circle(36, -86, 20, -64)       # (44.8, -104.0)
    p_beak_tip    = (126.0, -92.0)                       # Long iconic origami crane beak tip!
    p_throat      = pt_on_circle(78, -28, 58, -86)       # (82.0, -85.9)
    p_chest_in    = pt_on_circle(78, -28, 58, -152)      # (26.8, -55.2)
    # Origami faceted breast step:
    p_chest_prow  = (58.0, -14.0)                        # Sharp origami breast prow!
    p_belly_low   = pt_on_circle(-8, 18, 68, 62)         # (23.9, 78.0)
    p_tail_notch  = (-16.0, 84.0)                        # Lower origami body vertex
    p_hip_L       = (-48.0, 44.0)                        # Left origami hip facet
    p_wing_pocket = (-12.0, 18.0)                        # Concave origami fold where left wing tucks in

    # Eye ring cutout at (38, -88, r=4.5)
    ex, ey, er = 38.0, -88.0, 4.5
    circles.append((ex, ey, er, False))
    circles.append((ex, ey, 13.0, False))
    eye_cut = (
        f"M {fmt(ex - er)} {fmt(ey)} "
        f"A {fmt(er)} {fmt(er)} 0 1 0 {fmt(ex + er)} {fmt(ey)} "
        f"A {fmt(er)} {fmt(er)} 0 1 0 {fmt(ex - er)} {fmt(ey)} Z"
    )

    # True continuous spiral scroll cutout centered at (8, 28)
    spiral_cut = build_true_spiral_cutout(8.0, 28.0)
    circles.append((8.0, 28.0, 22.0, True))
    circles.append((4.0, 28.0, 16.0, False))
    circles.append((8.0, 28.0, 10.0, False))

    paths.append(" ".join([
        move_cmd(p_shoulder_L),
        arc_cmd(78.0, p_head_back, large_arc=0, sweep=1),
        line_cmd(p_crest_notch),
        line_cmd(p_crown_top),
        line_cmd(p_beak_tip),
        line_cmd(p_throat),
        arc_cmd(58.0, p_chest_in, large_arc=0, sweep=0),
        line_cmd(p_chest_prow),
        arc_cmd(68.0, p_belly_low, large_arc=0, sweep=1),
        line_cmd(p_tail_notch),
        line_cmd(p_hip_L),
        line_cmd(p_wing_pocket),
        line_cmd(p_shoulder_L),
        "Z",
        eye_cut,
        spiral_cut
    ]))

    rays.extend([
        (p_crown_top[0], p_crown_top[1], p_beak_tip[0], p_beak_tip[1]),
        (p_beak_tip[0], p_beak_tip[1], p_throat[0], p_throat[1]),
        (p_chest_in[0], p_chest_in[1], p_chest_prow[0], p_chest_prow[1]),
        (p_belly_low[0], p_belly_low[1], p_tail_notch[0], p_tail_notch[1]),
        (p_tail_notch[0], p_tail_notch[1], p_hip_L[0], p_hip_L[1]),
        (p_hip_L[0], p_hip_L[1], p_wing_pocket[0], p_wing_pocket[1]),
    ])
    vertices.extend([
        p_beak_tip, p_crown_top, p_crest_notch, p_throat,
        p_chest_in, p_chest_prow, p_belly_low, p_tail_notch, p_hip_L
    ])

    # ------------------------------------------------------------------
    # 3. GRAND LEFT WING (左翼 — 4 Stepped, Upward-Sweeping Crescent-Origami
    #    Feather Pinions like the Nihonbashi Kirin's Wing!)
    # Notice how each feather blade curves UPWARD along its own osculating circle
    # and steps inward so the wing has a dramatic, organic-geometric silhouette!
    # ------------------------------------------------------------------
    # Feather L1 (Grand Leading Wing Arch — sweeps from shoulder (-24, -14) all the way
    # up to the top-left ring notch (-54, -148) and curves down the left flank):
    circles.append((18.0, -12.0, 156.0, True))
    circles.append((34.0, -4.0, 134.0, False))
    l1_tip    = (-46.0, -148.0)                          # Pierces near top-left kamon ring notch!
    l1_flank  = pt_on_circle(18, -12, 156, -158)         # (-126.6, -70.4)
    l1_fold   = (-76.0, -46.0)                           # Crisp origami inner facet corner
    l1_root   = (-24.0, -16.0)                           # Shoulder root
    paths.append(" ".join([
        move_cmd(l1_tip),
        arc_cmd(156.0, l1_flank, large_arc=0, sweep=0),
        line_cmd(l1_fold),
        line_cmd(l1_root),
        arc_cmd(134.0, l1_tip, large_arc=0, sweep=1),
        "Z"
    ]))
    rays.append((l1_flank[0], l1_flank[1], l1_fold[0], l1_fold[1]))
    rays.append((l1_fold[0], l1_fold[1], l1_root[0], l1_root[1]))
    vertices.extend([l1_tip, l1_flank, l1_fold, l1_root])

    # Feather L2 (Second Curved Pinion — crescent blade curving from (-136, -18) to (-20, 4)):
    circles.append((14.0, -28.0, 152.0, True))
    circles.append((24.0, -16.0, 124.0, False))
    l2_tip    = (-128.0, -58.0)
    l2_outer  = (-136.0, -6.0)
    l2_fold   = (-78.0, -12.0)
    l2_root   = (-22.0, 2.0)
    l2_in_mid = (-76.0, -37.5)
    paths.append(" ".join([
        move_cmd(l2_tip),
        arc_cmd(152.0, l2_outer, large_arc=0, sweep=0),
        line_cmd(l2_fold),
        line_cmd(l2_root),
        line_cmd(l2_in_mid),
        line_cmd(l2_tip),
        "Z"
    ]))
    rays.append((l2_outer[0], l2_outer[1], l2_fold[0], l2_fold[1]))
    rays.append((l2_fold[0], l2_fold[1], l2_root[0], l2_root[1]))
    vertices.extend([l2_tip, l2_outer, l2_fold, l2_root])

    # Feather L3 (Third Curved Pinion — stepped inward, tip at (-134, 42)):
    circles.append((10.0, -38.0, 156.0, False))
    l3_tip    = (-134.0, 2.5)
    l3_outer  = (-124.0, 48.0)
    l3_fold   = (-72.0, 20.0)
    l3_root   = (-24.0, 14.0)
    l3_in_mid = (-78.0, -3.5)
    paths.append(" ".join([
        move_cmd(l3_tip),
        arc_cmd(156.0, l3_outer, large_arc=0, sweep=0),
        line_cmd(l3_fold),
        line_cmd(l3_root),
        line_cmd(l3_in_mid),
        line_cmd(l3_tip),
        "Z"
    ]))
    rays.append((l3_outer[0], l3_outer[1], l3_fold[0], l3_fold[1]))
    vertices.extend([l3_tip, l3_outer, l3_fold])

    # Feather L4 (Fourth Inner Origami Feather — stepped further inward, leaving generous
    # negative space above the tail):
    l4_tip    = (-118.0, 56.0)
    l4_outer  = (-96.0, 86.0)
    l4_root   = (-44.0, 34.0)
    l4_in_mid = (-70.0, 28.5)
    paths.append(" ".join([
        move_cmd(l4_tip),
        arc_cmd(140.0, l4_outer, large_arc=0, sweep=0),
        line_cmd(l4_root),
        line_cmd(l4_in_mid),
        line_cmd(l4_tip),
        "Z"
    ]))
    rays.append((l4_outer[0], l4_outer[1], l4_root[0], l4_root[1]))
    vertices.extend([l4_tip, l4_outer, l4_root])

    # ------------------------------------------------------------------
    # 4. RIGHT SWEPT ORIGAMI WING (右揚羽 — 3 Stepped Upward-Pointing Blades
    #    Rising Behind the Breast with Generous Sky Above & Below!)
    # ------------------------------------------------------------------
    circles.append((-24.0, -68.0, 172.0, True))
    circles.append((-12.0, -48.0, 152.0, False))
    circles.append((-8.0, -24.0, 134.0, False))

    # Right Blade R1 (High primary wing tip sweeping up toward (142, -38)):
    r1_root_top = (44.0, -36.0)
    r1_tip      = (142.0, -42.0)
    r1_low      = (138.0, -8.0)
    r1_root_bot = (66.0, -16.0)
    paths.append(" ".join([
        move_cmd(r1_root_top),
        line_cmd(r1_tip),
        arc_cmd(152.0, r1_low, large_arc=0, sweep=1),
        line_cmd(r1_root_bot),
        line_cmd(r1_root_top),
        "Z"
    ]))
    rays.append((r1_root_top[0], r1_root_top[1], r1_tip[0], r1_tip[1]))
    rays.append((r1_low[0], r1_low[1], r1_root_bot[0], r1_root_bot[1]))
    vertices.extend([r1_root_top, r1_tip, r1_low, r1_root_bot])

    # Right Blade R2 (Middle stepped blade, tip at (134, 0) to (122, 28)):
    r2_root_top = (68.0, -7.5)
    r2_tip      = (136.0, 0.0)
    r2_low      = (122.0, 30.0)
    r2_root_bot = (66.0, 18.0)
    paths.append(" ".join([
        move_cmd(r2_root_top),
        line_cmd(r2_tip),
        arc_cmd(134.0, r2_low, large_arc=0, sweep=1),
        line_cmd(r2_root_bot),
        arc_cmd(68.0, r2_root_top, large_arc=0, sweep=0),
        "Z"
    ]))
    rays.append((r2_low[0], r2_low[1], r2_root_bot[0], r2_root_bot[1]))
    vertices.extend([r2_tip, r2_low, r2_root_bot])

    # Right Blade R3 (Lower stepped origami pinion, tip at (116, 38) to (96, 62)):
    r3_root_top = (64.0, 26.5)
    r3_tip      = (118.0, 38.0)
    r3_low      = (96.0, 62.0)
    r3_root_bot = (50.0, 52.0)
    paths.append(" ".join([
        move_cmd(r3_root_top),
        line_cmd(r3_tip),
        arc_cmd(120.0, r3_low, large_arc=0, sweep=1),
        line_cmd(r3_root_bot),
        arc_cmd(68.0, r3_root_top, large_arc=0, sweep=0),
        "Z"
    ]))
    rays.append((r3_low[0], r3_low[1], r3_root_bot[0], r3_root_bot[1]))
    vertices.extend([r3_tip, r3_low, r3_root_bot])

    # ------------------------------------------------------------------
    # 5. ICONIC ORIGAMI TAIL SPIRE & TWO SLENDER TRAILING CRANE LEGS
    #    (折鶴の鋭い尾羽と二本の脚 — Leaving Clear Negative Space on Both Sides!)
    # ------------------------------------------------------------------
    # Origami Tail Spire (Left facet + Right facet forming a sharp pleated spire
    # pointing down-left toward the kamon ring notch at deg 126!):
    tl_base_L = (-46.0, 54.0)
    tl_base_M = (-22.0, 88.0)
    tl_spire  = (-82.0, 134.0)     # Reaches right into the lower-left ring notch!
    paths.append(" ".join([
        move_cmd(tl_base_L),
        line_cmd(tl_base_M),
        line_cmd(tl_spire),
        line_cmd(tl_base_L),
        "Z"
    ]))
    rays.append((tl_base_L[0], tl_base_L[1], tl_spire[0], tl_spire[1]))
    rays.append((tl_base_M[0], tl_base_M[1], tl_spire[0], tl_spire[1]))
    vertices.extend([tl_base_L, tl_base_M, tl_spire])

    # Second pleated tail fold alongside the spire:
    tl2_base_L = (-14.0, 92.0)
    tl2_base_R = (8.0, 88.0)
    tl2_tip    = (-46.0, 140.0)
    paths.append(" ".join([
        move_cmd(tl2_base_L),
        line_cmd(tl2_base_R),
        line_cmd(tl2_tip),
        line_cmd(tl2_base_L),
        "Z"
    ]))
    rays.append((tl2_base_R[0], tl2_base_R[1], tl2_tip[0], tl2_tip[1]))
    vertices.extend([tl2_base_L, tl2_base_R, tl2_tip])

    # Two Slender Trailing Crane Legs (二本の脚) extending diagonally down-right:
    # Leg 1 (Upper/Right trailing leg):
    leg1_a = (28.0, 82.0)
    leg1_b = (42.0, 72.0)
    leg1_c = (78.0, 126.0)
    leg1_d = (64.0, 134.0)
    paths.append(" ".join([
        move_cmd(leg1_a),
        line_cmd(leg1_b),
        line_cmd(leg1_c),
        line_cmd(leg1_d),
        line_cmd(leg1_a),
        "Z"
    ]))
    rays.append((leg1_b[0], leg1_b[1], leg1_c[0], leg1_c[1]))

    # Leg 2 (Lower/Left trailing leg, parallel with 7px gap):
    leg2_a = (14.0, 88.0)
    leg2_b = (23.0, 84.0)
    leg2_c = (56.0, 137.0)
    leg2_d = (42.0, 142.0)
    paths.append(" ".join([
        move_cmd(leg2_a),
        line_cmd(leg2_b),
        line_cmd(leg2_c),
        line_cmd(leg2_d),
        line_cmd(leg2_a),
        "Z"
    ]))
    rays.append((leg2_a[0], leg2_a[1], leg2_d[0], leg2_d[1]))
    vertices.extend([leg1_c, leg1_d, leg2_c, leg2_d])

    # Additional outer harmonic construction circles (like Rikyu's upper & side balance circles)
    circles.append((64.0, -96.0, 112.0, True))
    circles.append((-52.0, -76.0, 104.0, True))
    circles.append((-48.0, 74.0, 86.0, False))
    circles.append((54.0, 78.0, 78.0, True))

    return paths, circles, rays, vertices

def generate_svg():
    crest_paths, all_circles, exact_lines, key_vertices = build_crest_and_geometry()

    svg_lines = []
    svg_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg_lines.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 1000" width="100%" height="100%">')
    svg_lines.append('  <defs>')
    # 10px fine millimeter sub-grid
    svg_lines.append('    <pattern id="sub-grid" width="10" height="10" patternUnits="userSpaceOnUse">')
    svg_lines.append('      <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#E2DDD3" stroke-width="0.6"/>')
    svg_lines.append('    </pattern>')
    # 50px major millimeter grid
    svg_lines.append('    <pattern id="major-grid" width="50" height="50" patternUnits="userSpaceOnUse">')
    svg_lines.append('      <rect width="50" height="50" fill="url(#sub-grid)"/>')
    svg_lines.append('      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="#D2CCC0" stroke-width="0.9"/>')
    svg_lines.append('    </pattern>')
    # Smooth vertical fade mask so the grid dissolves into the paper above the CONCEPT footer
    svg_lines.append('    <linearGradient id="grid-fade" x1="0" y1="0" x2="0" y2="1">')
    svg_lines.append('      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>')
    svg_lines.append('      <stop offset="80%" stop-color="#FFFFFF" stop-opacity="1"/>')
    svg_lines.append('      <stop offset="97%" stop-color="#FFFFFF" stop-opacity="0"/>')
    svg_lines.append('      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>')
    svg_lines.append('    </linearGradient>')
    svg_lines.append('    <mask id="grid-mask">')
    svg_lines.append('      <rect x="40" y="40" width="720" height="720" fill="url(#grid-fade)"/>')
    svg_lines.append('    </mask>')
    # Blueprint clip path
    svg_lines.append('    <clipPath id="blueprint-clip">')
    svg_lines.append('      <rect x="40" y="40" width="720" height="720"/>')
    svg_lines.append('    </clipPath>')

    # Reusable #crest-shape template
    svg_lines.append('    <g id="crest-shape">')
    for d_str in crest_paths:
        svg_lines.append(f'      <path d="{d_str}" fill-rule="evenodd"/>')
    svg_lines.append('    </g>')
    svg_lines.append('  </defs>')

    # 1. Warm Washi Paper Background
    svg_lines.append('  <rect width="800" height="1000" fill="#F4F1EA"/>')

    # 2. Fading Millimeter Grid Layer
    svg_lines.append('  <rect x="40" y="40" width="720" height="720" fill="url(#major-grid)" mask="url(#grid-mask)"/>')

    # 3. Central Translucent Blueprint Motif (at 400, 385)
    svg_lines.append('  <g transform="translate(400, 385)">')
    svg_lines.append('    <use href="#crest-shape" fill="#8C877E" fill-opacity="0.38" stroke="#4A463F" stroke-width="1.25" stroke-linejoin="round"/>')
    svg_lines.append('  </g>')

    # 4. Synchronized Compass-and-Straightedge Construction Overlay
    svg_lines.append('  <g clip-path="url(#blueprint-clip)" mask="url(#grid-mask)">')
    svg_lines.append('    <g transform="translate(400, 385)">')

    # 4a. Extended Secant & Tangent Rays
    for (x1, y1, x2, y2) in exact_lines:
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length > 1e-5:
            ux, uy = dx / length, dy / length
            ex1, ey1 = x1 - 1200.0 * ux, y1 - 1200.0 * uy
            ex2, ey2 = x1 + 1200.0 * ux, y1 + 1200.0 * uy
            svg_lines.append(
                f'      <line x1="{fmt(ex1)}" y1="{fmt(ey1)}" x2="{fmt(ex2)}" y2="{fmt(ey2)}" '
                f'stroke="#5C574F" stroke-width="0.72" stroke-opacity="0.68"/>'
            )

    # 4b. Osculating Construction Circles + Center Crosshairs + Radius Callouts
    for (cx, cy, r, has_callout) in all_circles:
        svg_lines.append(
            f'      <circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r)}" '
            f'fill="none" stroke="#5C574F" stroke-width="0.82" stroke-opacity="0.76"/>'
        )
        svg_lines.append(
            f'      <path d="M {fmt(cx - 3.5)} {fmt(cy)} H {fmt(cx + 3.5)} M {fmt(cx)} {fmt(cy - 3.5)} V {fmt(cy + 3.5)}" '
            f'fill="none" stroke="#4A463F" stroke-width="0.85" stroke-opacity="0.85"/>'
        )
        if has_callout and r >= 20:
            svg_lines.append(
                f'      <line x1="{fmt(cx)}" y1="{fmt(cy)}" x2="{fmt(cx + r)}" y2="{fmt(cy)}" '
                f'stroke="#4A463F" stroke-width="0.75" stroke-opacity="0.75"/>'
            )
            svg_lines.append(
                f'      <line x1="{fmt(cx + r)}" y1="{fmt(cy - 3.0)}" x2="{fmt(cx + r)}" y2="{fmt(cy + 3.0)}" '
                f'stroke="#4A463F" stroke-width="0.75" stroke-opacity="0.75"/>'
            )

    # 4c. Anchor Vertex Dots at origami fold intersections
    for (vx, vy) in key_vertices:
        svg_lines.append(
            f'      <circle cx="{fmt(vx)}" cy="{fmt(vy)}" r="1.7" fill="#4A463F" fill-opacity="0.82"/>'
        )

    svg_lines.append('    </g>')
    svg_lines.append('  </g>')

    # 5. Editorial Outer Frame & Bottom-Right Preview Inset Box
    svg_lines.append('  <rect x="40" y="40" width="720" height="920" fill="none" stroke="#C6C0B4" stroke-width="1"/>')
    svg_lines.append('  <rect x="560" y="760" width="200" height="200" fill="#F4F1EA" stroke="#C6C0B4" stroke-width="1"/>')

    # 6. Top Brand Header: Rikyu Tea Master Silhouette + Serif Title
    svg_lines.append('  <g transform="translate(352, 60)">')
    svg_lines.append('    <path d="M 8 8 C 8 3, 18 3, 18 8 L 19 14 L 7 14 Z" fill="#3A3631"/>')
    svg_lines.append('    <circle cx="13" cy="18" r="5" fill="#E5C9A8"/>')
    svg_lines.append('    <path d="M 3 34 C 3 24, 9 22, 13 22 C 18 22, 23 25, 24 34 Z" fill="#3A3631"/>')
    svg_lines.append('    <path d="M 4 29 Q 8 29 9 33 L 3 33 Z" fill="#F4F1EA"/>')
    svg_lines.append('    <path d="M 5 27 H 11 C 11 30, 5 30, 5 27 Z" fill="#7A7267"/>')
    svg_lines.append(
        '    <text x="32" y="29" font-family="\'Noto Serif CJK JP\', \'Noto Serif\', \'Georgia\', \'Times New Roman\', serif" '
        'font-size="25" font-weight="600" fill="#3A3631" letter-spacing="0.5">Rikyū</text>'
    )
    svg_lines.append('  </g>')

    # 7. Bottom-Left CONCEPT Editorial Block
    svg_lines.append(
        '  <text x="76" y="810" font-family="\'Noto Sans CJK JP\', \'Noto Sans SC\', \'Helvetica Neue\', \'Arial\', sans-serif" '
        'font-size="13" font-weight="600" fill="#4A463F" letter-spacing="2.8">CONCEPT</text>'
    )
    concept_lines = [
        "折り鶴の鋭い直線的ファセットと、天へ舞い上がる鶴の優美な",
        "円弧を融合し、丸輪の家紋様式へと再構成した紋章です。大きく",
        "広げた左右非対称の翼と幾何学的な胴体・尾羽を等幅の余白で",
        "切り分け、尺規作図の秩序の中に凛とした飛翔の勢いを宿しました。"
    ]
    for idx, line in enumerate(concept_lines):
        y_pos = 846 + idx * 25
        svg_lines.append(
            f'  <text x="76" y="{y_pos}" font-family="\'Noto Sans CJK JP\', \'Noto Sans SC\', sans-serif" '
            f'font-size="14" font-weight="400" fill="#6E6A63" letter-spacing="0.4">{line}</text>'
        )

    # 8. Bottom-Right Finished Solid Kamon Emblem Preview (Centered at 660, 860, scaled to 0.32)
    svg_lines.append('  <g transform="translate(660, 860) scale(0.32)">')
    svg_lines.append('    <use href="#crest-shape" fill="#3A3631" stroke="none"/>')
    svg_lines.append('  </g>')

    svg_lines.append('</svg>')

    with open(SVG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Saved SVG to: {os.path.abspath(SVG_PATH)}")

if __name__ == "__main__":
    generate_svg()
