import re

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the historyPath / forecastPath drawing blocks in Canvas with a single continuous rosterPath
old_curves = """                    // 5. Recent History Curve
                    val historyPath = Path()
                    var histPenDown = false
                    var lastHistOffset: Offset? = null
                    visiblePoints.filter { it.isHistory }.forEach { pt ->
                        val score = pt.rosterAlertness
                        val x = leftAxisW + (((pt.hourOffsetFromNow - minOffset) / totalSpanHours) * chartW)
                        val y = chartH - (((score - 1f) / 9f) * chartH)
                        if (!histPenDown) {
                            historyPath.moveTo(x, y)
                            histPenDown = true
                        } else {
                            historyPath.lineTo(x, y)
                        }
                        lastHistOffset = Offset(x, y)
                    }
                    drawPath(
                        path = historyPath,
                        color = Color(0xFF64748B),
                        style = Stroke(width = 2.6.dp.toPx(), cap = StrokeCap.Round)
                    )

                    // 6. Next 72-Hour Roster Forecast Curve (Solid Teal)
                    val forecastPath = Path()
                    var forePenDown = false
                    visiblePoints.filter { !it.isHistory }.forEach { pt ->
                        val score = pt.rosterAlertness
                        val x = leftAxisW + (((pt.hourOffsetFromNow - minOffset) / totalSpanHours) * chartW)
                        val y = chartH - (((score - 1f) / 9f) * chartH)
                        if (!forePenDown) {
                            forecastPath.moveTo(x, y)
                            forePenDown = true
                        } else {
                            forecastPath.lineTo(x, y)
                        }
                    }
                    drawPath(
                        path = forecastPath,
                        color = Color(0xFF0F766E),
                        style = Stroke(width = 3.dp.toPx(), cap = StrokeCap.Round)
                    )

                    if (dayShiftOffset == 0) {
                        lastHistOffset?.let {
                            drawCircle(Color(0xFF0F766E), radius = 4.5.dp.toPx(), center = it)
                        }
                    }"""

new_curves = """                    // 5. Continuous Roster Alertness Curve (Zero gaps!)
                    val continuousRosterPath = Path()
                    var lastNowOffset: Offset? = null
                    val realNowMillis = System.currentTimeMillis()

                    visiblePoints.forEachIndexed { idx, pt ->
                        val x = leftAxisW + (((pt.hourOffsetFromNow - minOffset) / totalSpanHours) * chartW)
                        val y = chartH - (((pt.rosterAlertness - 1f) / 9f) * chartH)
                        if (idx == 0) {
                            continuousRosterPath.moveTo(x, y)
                        } else {
                            continuousRosterPath.lineTo(x, y)
                        }
                        if (dayShiftOffset == 0 && pt.timestampMillis <= realNowMillis) {
                            lastNowOffset = Offset(x, y)
                        }
                    }

                    val curveColor = if (dayShiftOffset < 0) Color(0xFF64748B) else Color(0xFF0F766E)
                    drawPath(
                        path = continuousRosterPath,
                        color = curveColor,
                        style = Stroke(width = 3.dp.toPx(), cap = StrokeCap.Round)
                    )

                    // Only draw NOW dot when viewing Today (dayShiftOffset == 0)
                    if (dayShiftOffset == 0) {
                        lastNowOffset?.let {
                            drawCircle(Color(0xFF0F766E), radius = 5.dp.toPx(), center = it)
                            drawCircle(Color.White, radius = 2.5.dp.toPx(), center = it)
                        }
                    }"""

if old_curves in content:
    content = content.replace(old_curves, new_curves)
    print("MAIN ACTIVITY CONTINUOUS CURVE UPDATED")
else:
    print("OLD CURVES PATTERN NOT FOUND")

# Also add 12h / 24h / 48h / 72h Zoom Level options in controls row
old_zoom_control = """                Surface(
                    onClick = { onHistoryHoursChange(if (historyHours == 24) 48 else 24) },
                    color = Color.White,
                    shape = RoundedCornerShape(10.dp),
                    border = BorderStroke(1.dp, palette.cardBorder)
                ) {
                    Text(
                        "Past $historyHours hours ⌄",
                        color = palette.textPrimary,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 8.dp)
                    )
                }"""

new_zoom_control = """                Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    listOf(12, 24, 48, 72).forEach { hrs ->
                        val isSel = historyHours == hrs
                        Surface(
                            onClick = { onHistoryHoursChange(hrs) },
                            color = if (isSel) palette.accentTeal else Color.White,
                            shape = RoundedCornerShape(8.dp),
                            border = BorderStroke(1.dp, if (isSel) palette.accentTeal else palette.cardBorder)
                        ) {
                            Text(
                                "${hrs}h",
                                color = if (isSel) Color.White else palette.textPrimary,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 6.dp)
                            )
                        }
                    }
                }"""

if old_zoom_control in content:
    content = content.replace(old_zoom_control, new_zoom_control)
    print("ZOOM CONTROLS UPDATED")

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(content)
