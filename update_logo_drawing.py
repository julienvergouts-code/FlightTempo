with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find("@Composable\nfun PrecisionRosterDialLogoIcon(")
if start_idx != -1:
    brace_count = 0
    end_idx = start_idx
    for i in range(start_idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx = i + 1
                break
    new_logo_code = '''@Composable
fun PrecisionRosterDialLogoIcon(modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val w = size.width
        val h = size.height
        val cx = w / 2f
        val cy = h / 2f
        val dialR = w * 0.44f
        val sunR = w * 0.32f

        // Deep Midnight Navy Container
        drawCircle(color = Color(0xFF030C1C), radius = w / 2f, center = Offset(cx, cy))

        // 360° Instrument Precision Dial Circle
        drawCircle(color = Color(0xFF1E3A8A).copy(alpha = 0.5f), radius = dialR, center = Offset(cx, cy), style = Stroke(width = w * 0.015f))

        // 360° Instrument Dial Ticks (24 ticks spaced every 15°)
        for (i in 0..23) {
            val angleDeg = i * 15f
            val rad = Math.toRadians(angleDeg.toDouble())
            val isMajor = i % 3 == 0
            val len = if (isMajor) w * 0.07f else w * 0.04f
            val r1 = dialR
            val r2 = dialR - len
            val x1 = cx + (r1 * Math.cos(rad)).toFloat()
            val y1 = cy + (r1 * Math.sin(rad)).toFloat()
            val x2 = cx + (r2 * Math.cos(rad)).toFloat()
            val y2 = cy + (r2 * Math.sin(rad)).toFloat()
            val tickColor = if (isMajor && angleDeg in 180f..360f) Color(0xFFFBBF24) else Color(0xFF94A3B8).copy(alpha = 0.7f)
            drawLine(
                color = tickColor,
                start = Offset(x1, y1),
                end = Offset(x2, y2),
                strokeWidth = if (isMajor) w * 0.025f else w * 0.015f,
                cap = StrokeCap.Round
            )
        }

        // Radiant Golden Sun Arc Ring
        val sunPath = Path().apply {
            addArc(
                oval = androidx.compose.ui.geometry.Rect(cx - sunR, cy - sunR, cx + sunR, cy + sunR),
                startAngleDegrees = 180f,
                sweepAngleDegrees = 180f
            )
        }
        drawPath(
            path = sunPath,
            color = Color(0xFFFBBF24),
            style = Stroke(width = w * 0.05f, cap = StrokeCap.Round)
        )

        // Inner Golden Halo Glow
        val haloPath = Path().apply {
            addArc(
                oval = androidx.compose.ui.geometry.Rect(cx - (sunR * 0.82f), cy - (sunR * 0.82f), cx + (sunR * 0.82f), cy + (sunR * 0.82f)),
                startAngleDegrees = 180f,
                sweepAngleDegrees = 180f
            )
        }
        drawPath(
            path = haloPath,
            color = Color(0xFFF59E0B).copy(alpha = 0.8f),
            style = Stroke(width = w * 0.025f, cap = StrokeCap.Round)
        )

        // Cyan Horizon Line
        drawLine(
            color = Color(0xFF22D3EE),
            start = Offset(cx - (sunR * 1.35f), cy),
            end = Offset(cx + (sunR * 1.35f), cy),
            strokeWidth = w * 0.035f,
            cap = StrokeCap.Round
        )

        // White Jetliner Silhouette
        val planePath = Path().apply {
            moveTo(cx, cy - (sunR * 0.55f))
            lineTo(cx + (sunR * 0.06f), cy)
            lineTo(cx + (sunR * 0.12f), cy + (sunR * 0.18f))
            lineTo(cx - (sunR * 0.12f), cy + (sunR * 0.18f))
            lineTo(cx - (sunR * 0.06f), cy)
            close()
        }
        drawPath(planePath, Color.White)

        val wingPath = Path().apply {
            moveTo(cx - (sunR * 0.88f), cy + (sunR * 0.04f))
            lineTo(cx, cy - (sunR * 0.08f))
            lineTo(cx + (sunR * 0.88f), cy + (sunR * 0.04f))
            lineTo(cx + (sunR * 0.88f), cy + (sunR * 0.12f))
            lineTo(cx, cy + (sunR * 0.06f))
            lineTo(cx - (sunR * 0.88f), cy + (sunR * 0.12f))
            close()
        }
        drawPath(wingPath, Color.White)

        // Lower Alertness Sine Wave Lines
        val wave1 = Path().apply {
            moveTo(cx - (sunR * 1.1f), cy + (sunR * 0.35f))
            cubicTo(
                cx - (sunR * 0.5f), cy + (sunR * 0.75f),
                cx + (sunR * 0.5f), cy + (sunR * 0.25f),
                cx + (sunR * 1.1f), cy + (sunR * 0.35f)
            )
        }
        drawPath(
            path = wave1,
            color = Color(0xFF0284C7).copy(alpha = 0.85f),
            style = Stroke(width = w * 0.025f, cap = StrokeCap.Round)
        )

        val wave2 = Path().apply {
            moveTo(cx - (sunR * 1.1f), cy + (sunR * 0.52f))
            cubicTo(
                cx - (sunR * 0.5f), cy + (sunR * 0.92f),
                cx + (sunR * 0.5f), cy + (sunR * 0.42f),
                cx + (sunR * 1.1f), cy + (sunR * 0.52f)
            )
        }
        drawPath(
            path = wave2,
            color = Color(0xFF38BDF8).copy(alpha = 0.75f),
            style = Stroke(width = w * 0.02f, cap = StrokeCap.Round)
        )

        // Crescent Moon in Wave Trough
        val moonCx = cx
        val moonCy = cy + (sunR * 0.50f)
        val moonR = sunR * 0.22f
        drawCircle(Color(0xFF38BDF8), radius = moonR, center = Offset(moonCx, moonCy))
        drawCircle(Color(0xFF030C1C), radius = moonR * 0.85f, center = Offset(moonCx + (moonR * 0.35f), moonCy - (moonR * 0.2f)))
    }
}'''
    new_content = content[:start_idx] + new_logo_code + content[end_idx:]
    with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("START NOT FOUND")
