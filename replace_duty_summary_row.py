import re

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TopTwoDutySummaryRow call in MainContentColumn
old_call = """            else -> {
                TopTwoDutySummaryRow(events = calendarEvents, homeBase = homeBaseIata, palette = palette)"""

new_call = """            else -> {
                TopTwoDutySummaryRow(
                    events = calendarEvents,
                    homeBase = homeBaseIata,
                    palette = palette,
                    nextDutyEval = nextDutyEval,
                    activeCaffeineMg = CaffeineSimulator.calculateActiveCaffeine(caffeineIngestions, nowMillis),
                    onCompareClick = { onNavigateTab("Graph") }
                )"""

if old_call in content:
    content = content.replace(old_call, new_call)

# 2. Replace TopTwoDutySummaryRow implementation
pattern = re.compile(r'@Composable\s+fun TopTwoDutySummaryRow[\s\S]*?^\}\s*^\}', re.MULTILINE)

new_row_code = """@Composable
fun TopTwoDutySummaryRow(
    events: List<CalendarEventItem>,
    homeBase: String,
    palette: AppPalette,
    nextDutyEval: NextDutyAlertnessEvaluation? = null,
    activeCaffeineMg: Double = 0.0,
    onCompareClick: () -> Unit = {}
) {
    var liveNow by remember { mutableLongStateOf(System.currentTimeMillis()) }
    LaunchedEffect(Unit) {
        while (true) {
            delay(10000)
            liveNow = System.currentTimeMillis()
        }
    }

    val activeDuty = events.filter { liveNow >= it.startMillis && liveNow < it.endMillis }
        .maxByOrNull { it.type.baseDrainMultiplier }
    val nextEv = activeDuty ?: events.filter { it.startMillis > liveNow }.minByOrNull { it.startMillis }
    val zone = nextEv?.let { runCatching { ZoneId.of(it.timeZoneId) }.getOrNull() } ?: ZoneId.systemDefault()
    val timeFmt = DateTimeFormatter.ofPattern("HH:mm", Locale.ENGLISH).withZone(zone)

    // Alertness Score & Caffeine Status
    val scoreVal = nextDutyEval?.currentAwakeIndex ?: 8.8f
    val readinessPct = ((scoreVal - 1.0f) / 9.0f).coerceIn(0.05f, 1.0f)
    val readinessStatus = if (scoreVal >= 7.0f) "GO" else if (scoreVal >= 5.0f) "CAUTION" else "FATIGUE"

    // Time until report / start
    val untilStr = when {
        activeDuty != null -> "In progress"
        nextEv != null -> {
            val diffMins = ((nextEv.startMillis - liveNow) / 60_000L).coerceAtLeast(0L)
            "In ${diffMins / 60}h %02dm".format(diffMins % 60)
        }
        else -> "—"
    }

    val dutyCategoryLabel = when (nextEv?.type) {
        DutyCategory.WORK -> "LINE FLIGHT"
        DutyCategory.CHECK -> "EXAMINER / CHECK"
        DutyCategory.POSITIONING_ACTIVE -> "ACTIVE COMMUTE"
        DutyCategory.POSITIONING_PASSIVE -> "DEADHEAD"
        DutyCategory.STANDBY -> "STANDBY / RESERVE"
        else -> "DUTY"
    }

    // Target lights out (computed from duty start - hotel commute - 8h sleep buffer)
    val lightsOutStr = remember(nextEv) {
        if (nextEv != null) {
            val targetSleepStart = nextEv.startMillis - (9L * 3600_000L)
            timeFmt.format(Instant.ofEpochMilli(targetSleepStart))
        } else "21:30"
    }

    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        // 1. LIVE COGNITIVE READINESS CARD
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFF132330)),
            shape = RoundedCornerShape(16.dp),
            border = BorderStroke(1.dp, Color(0xFF1F3547)),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "LIVE COGNITIVE READINESS",
                        color = Color(0xFF94A3B8),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 0.5.sp
                    )
                    Surface(
                        color = Color(0xFF0F3B36),
                        shape = RoundedCornerShape(6.dp),
                        border = BorderStroke(1.dp, Color(0xFF14534A))
                    ) {
                        Text(
                            "%.1f / 10 · %s".format(Locale.ENGLISH, scoreVal, readinessStatus),
                            color = Color(0xFF34D399),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp)
                        )
                    }
                }

                // Progress Bar
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(8.dp)
                        .clip(RoundedCornerShape(4.dp))
                        .background(Color(0xFF1E3547))
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(readinessPct)
                            .fillMaxHeight()
                            .clip(RoundedCornerShape(4.dp))
                            .background(
                                Brush.horizontalGradient(
                                    listOf(Color(0xFF10B981), Color(0xFF34D399), Color(0xFF6EE7B7))
                                )
                            )
                    )
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        if (activeCaffeineMg > 0) "Boosted +0.4 pts now · Minimal sleep friction"
                        else "Natural circadian baseline · No active caffeine",
                        color = Color(0xFF94A3B8),
                        fontSize = 11.sp
                    )
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(4.dp)
                    ) {
                        Text("☕", fontSize = 12.sp)
                        Text(
                            "${activeCaffeineMg.toInt()} mg active",
                            color = Color(0xFF34D399),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }

        // 2. NEXT DUTY & TARGET REST CARD
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFF132330)),
            shape = RoundedCornerShape(16.dp),
            border = BorderStroke(1.dp, Color(0xFF1F3547)),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(
                modifier = Modifier.padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Surface(
                        color = Color(0xFF0F3B36),
                        shape = RoundedCornerShape(6.dp)
                    ) {
                        Text(
                            "NEXT DUTY · $dutyCategoryLabel",
                            color = Color(0xFF34D399),
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.padding(horizontal = 7.dp, vertical = 3.dp)
                        )
                    }
                    Text(
                        untilStr,
                        color = Color(0xFF38BDF8),
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold
                    )
                }

                Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(
                        nextEv?.title ?: "No duty scheduled",
                        color = Color.White,
                        fontSize = 17.sp,
                        fontWeight = FontWeight.Bold
                    )
                    Text(
                        if (nextEv != null) "Report ${timeFmt.format(Instant.ofEpochMilli(nextEv.startMillis))} LOC · ${nextEv.sectorCount} Sector(s)"
                        else "No active pairing imported",
                        color = Color(0xFF94A3B8),
                        fontSize = 12.sp
                    )
                }

                // Sub-Box: Target Lights-Out & Compare Mode
                Surface(
                    color = Color(0xFF0D1B26),
                    shape = RoundedCornerShape(12.dp),
                    border = BorderStroke(1.dp, Color(0xFF1E3547)),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                Text("🎯", fontSize = 12.sp)
                                Text(
                                    "Target Lights-Out: $lightsOutStr LOC",
                                    color = Color.White,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                            Text(
                                "Protects optimal recovery window before duty wake",
                                color = Color(0xFF64748B),
                                fontSize = 10.5.sp
                            )
                        }
                        Text(
                            "Compare Mode",
                            color = Color(0xFF38BDF8),
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.clickable { onCompareClick() }
                        )
                    }
                }
            }
        }
    }
}"""

match = pattern.search(content)
if match:
    content = content[:match.start()] + new_row_code + content[match.end():]
    with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("REPLACED DUTY SUMMARY ROW SUCCESSFULLY")
else:
    print("PATTERN NOT FOUND")
