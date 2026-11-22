"""Map elapsed days to distance along a fourth-order Hilbert curve."""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def hilbert(index, side=16):
    x = y = 0
    scale = 1
    while scale < side:
        rx = (index // 2) & 1
        ry = (index ^ rx) & 1
        if ry == 0:
            if rx == 1:
                x, y = scale - 1 - x, scale - 1 - y
            x, y = y, x
        x += scale * rx
        y += scale * ry
        index //= 4
        scale *= 2
    return x, y


def render(today):
    start = date(today.year, 1, 1)
    next_year = date(today.year + 1, 1, 1)
    total = (next_year - start).days
    elapsed = (today - start).days
    fraction = elapsed / total
    path = [hilbert(i) for i in range(256)]
    edge, remainder = divmod(elapsed * 255, total)
    x, y = path[edge]
    nx, ny = path[edge + 1]
    head = x + (nx - x) * remainder / total, y + (ny - y) * remainder / total

    def coordinates(points):
        return " ".join(f"{x:.3f},{y:.3f}" for x, y in points)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="736" height="166" viewBox="0 0 736 166" role="img" aria-labelledby="title">
  <title id="title">{today.isoformat()} KST · 올해 {fraction:.2%} 경과 · 새해까지 {total-elapsed}일</title>
  <rect width="736" height="166" fill="#0b0e13"/>
  <g font-family="ui-monospace,monospace">
    <text x="28" y="36" fill="#8fa2b5" font-size="17">{today.year} / YEAR PROGRESS</text>
    <text x="26" y="103" fill="#e8f3ed" font-size="56" font-weight="bold">{fraction:.2%}</text>
    <text x="29" y="140" fill="#6aebc0" font-size="16">{today.isoformat()} KST  ·  D−{total-elapsed}</text>
  </g>
  <g transform="translate(529 19) scale(8.5)" fill="none" stroke-width=".28" stroke-linejoin="round" stroke-linecap="round">
    <polyline stroke="#324052" points="{coordinates(path)}"/>
    <polyline stroke="#6aebc0" points="{coordinates(path[:edge+1]+[head])}"/>
    <circle cx="{head[0]:.3f}" cy="{head[1]:.3f}" r=".5" fill="#ffc068"/>
  </g>
</svg>
"""


if __name__ == "__main__":
    today = datetime.now(timezone(timedelta(hours=9))).date()
    (Path(__file__).resolve().parents[1] / "assets/year.svg").write_text(render(today))
