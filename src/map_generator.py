# Generate PNG map showing ship route over OSM-style background
import logging
from datetime import datetime as _dt
from PIL import Image, ImageDraw

logger = logging.getLogger(__name__)

MAP_W, MAP_H = 1600, 900


def _get_font(size=18):
    from PIL import ImageFont
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"
                                  "DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _scale_points(route, img_w=MAP_W, img_h=MAP_H):
    if not route:
        return [], (img_w // 2, img_h // 2)
    clat = sum(p[0] for p in route) / len(route)
    clon = sum(p[1] for p in route) / len(route)
    pts = []
    for lat, lon in route:
        x = int((clon - lon) * -8000 + img_w // 2)
        y = int((clat - lat) * 8000 + img_h // 2)
        pts.append((x, y))
    return pts, (img_w // 2, img_h // 2)


def generate_map(route_points=None, ship_pos=None, name="Unknown",
                 output_path="/home/harbor-watch/templates/map.png"):
    img = Image.new("RGB", (MAP_W, MAP_H), (40, 55, 80))
    draw = ImageDraw.Draw(img)

    # Title bar top
    draw.rectangle([0, 0, MAP_W - 1, 60], fill=(25, 35, 55))
    title_font = _get_font(26)
    draw.text((40, 18), "Harbor Watch - Port of A Coruna",
              fill=(255, 255, 255), font=title_font)

    # Route line
    pts, ref = _scale_points(route_points or [], MAP_W, MAP_H)
    if len(pts) >= 2:
        draw.line(pts, fill=(230, 210, 80), width=4)

    # Entry point (yellow dot at start of route)
    if pts:
        first = pts[0]
        draw.ellipse([first[0]-10, first[1]-10,
                       first[0]+10, first[1]+10],
                     fill=(230, 255, 80))

    # Ship current position (red dot)
    if ship_pos:
        sp = _scale_points([ship_pos], MAP_W, MAP_H)
        sx, sy = sp[0]
        draw.ellipse([sx-16, sy-16, sx+16, sy+16],
                     fill=(220, 55, 50), outline=(240, 170, 170), width=3)

    # Vessel name label
    if name:
        nfont = _get_font(18)
        draw.text((40, 68), "Vessel: " + name,
                  fill=(255, 240, 220), font=nfont)

    # Timestamp bottom-left
    tsf = _get_font(13)
    now_str = _dt.now().strftime("%Y-%m-%d %H:%M")
    draw.text((40, MAP_H - 28), now_str,
              fill=(160, 170, 195), font=tsf)

    # Watermark bottom-right
    draw.text((MAP_W - 140, MAP_H - 28), "harbor-watch",
              fill=(100, 120, 155), font=tsf)

    img.save(output_path)
    logger.info("Map saved: %s @%dx%d", output_path, MAP_W, MAP_H)
    return output_path


def generate_enhanced_map(route_points=None, ship_pos=None, name="Unknown",
                          imo=None, flag=None, gross_tons=None, length_m=None,
                          output_path="/home/harbor-watch/templates/map.png"):
    # Generate base map first then add info card overlay
    generate_map(route_points, ship_pos, name, output_path)

    img = Image.open(output_path)
    draw = ImageDraw.Draw(img)

    # Info panel box at upper right corner (semi-dark background)
    cx, cy = 1260, 90
    pw, ph = 300, 150
    draw.rectangle([cx - 4, cy - 4, cx + pw + 4, cy + ph + 4], fill=(18, 22, 38))
    draw.rectangle([cx, cy, cx + pw, cy + ph], outline=(50, 115, 200), width=2)

    font = _get_font(16)
    y_off = cy + 25
    info_lines = []
    if name:
        info_lines.append("Vessel: " + str(name))
    if imo:
        info_lines.append("IMO: " + str(imo))
    if flag:
        info_lines.append("Flag: " + str(flag))
    if gross_tons:
        info_lines.append("GRT: " + "{:,}".format(gross_tons))
    if length_m:
        info_lines.append("Length: {}m".format(length_m))

    y_off = cy + 25
    for line in info_lines:
        draw.text((cx + 14, y_off), line, fill=(230, 235, 240), font=font)
        y_off += 22

    img.save(output_path)
    logger.info("Enhanced map saved with %d info lines", len(info_lines))
    return output_path
