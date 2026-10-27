import re

# 1. Update FatigueEngine.kt
with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\FatigueEngine.kt', 'r', encoding='utf-8') as f:
    fe_content = f.read()

# Update buildDualCurveTimeline signature
old_bdct = """    fun buildDualCurveTimeline(
        nowMillis: Long,
        sleepSummary: SleepSummary,
        duties: List<CalendarEventItem>,
        homeBase: String,
        biologicalSex: String = "Not set",
        hotelTransferMinutes: Long = 30L,
        usualBedtimeHour: Float = 22.5f,
        usualWakeHour: Float = 7.0f,
        baseHotelFactor: Float = 0.85f,
        caffeineIngestions: List<CaffeineIngestionItem> = emptyList()
    ): Pair<List<AlertnessPoint>, List<SleepWindowBlock>> {"""

new_bdct = """    fun buildDualCurveTimeline(
        nowMillis: Long,
        sleepSummary: SleepSummary,
        duties: List<CalendarEventItem>,
        homeBase: String,
        biologicalSex: String = "Not set",
        hotelTransferMinutes: Long = 30L,
        homeCommuteMinutes: Long = 30L,
        usualBedtimeHour: Float = 22.5f,
        usualWakeHour: Float = 7.0f,
        baseHotelFactor: Float = 0.85f,
        caffeineIngestions: List<CaffeineIngestionItem> = emptyList()
    ): Pair<List<AlertnessPoint>, List<SleepWindowBlock>> {"""

if old_bdct in fe_content:
    fe_content = fe_content.replace(old_bdct, new_bdct)

# Update buildSleepTimelineBlocks call inside buildDualCurveTimeline
old_bstb_call = """        val sleepBlocks = buildSleepTimelineBlocks(
            nowMillis = nowMillis,
            startMillis = startMillis,
            endMillis = endMillis,
            recordedSessions = sleepSummary.sessions,
            duties = duties,
            homeBase = homeBase,
            baseZone = zone,
            biologicalPhaseShiftHours = biologicalPhaseShiftHours,
            targetMinutes = sleepSummary.target24hMinutes,
            usualBedtimeHour = usualBedtimeHour,
            usualWakeHour = usualWakeHour,
            hotelTransferMinutes = hotelTransferMinutes
        )"""

new_bstb_call = """        val sleepBlocks = buildSleepTimelineBlocks(
            nowMillis = nowMillis,
            startMillis = startMillis,
            endMillis = endMillis,
            recordedSessions = sleepSummary.sessions,
            duties = duties,
            homeBase = homeBase,
            baseZone = zone,
            biologicalPhaseShiftHours = biologicalPhaseShiftHours,
            targetMinutes = sleepSummary.target24hMinutes,
            usualBedtimeHour = usualBedtimeHour,
            usualWakeHour = usualWakeHour,
            hotelTransferMinutes = hotelTransferMinutes,
            homeCommuteMinutes = homeCommuteMinutes
        )"""

if old_bstb_call in fe_content:
    fe_content = fe_content.replace(old_bstb_call, new_bstb_call)

# Update buildSleepTimelineBlocks definition and transfer functions
old_bstb_def = """    private fun buildSleepTimelineBlocks(
        nowMillis: Long,
        startMillis: Long,
        endMillis: Long,
        recordedSessions: List<SleepSessionItem>,
        duties: List<CalendarEventItem>,
        homeBase: String,
        baseZone: ZoneId,
        biologicalPhaseShiftHours: Float,
        targetMinutes: Long,
        usualBedtimeHour: Float,
        usualWakeHour: Float,
        hotelTransferMinutes: Long
    ): List<SleepWindowBlock> {
        val blocks = mutableListOf<SleepWindowBlock>()

        // 1. Add actual recorded sleep sessions (Watch / Health Connect / Manual Override)
        recordedSessions.filter { it.endMillis >= startMillis && it.startMillis <= endMillis }.forEach { s ->
            blocks.add(
                SleepWindowBlock(
                    startMillis = s.startMillis,
                    endMillis = s.endMillis,
                    isRecorded = true,
                    label = "Recorded sleep"
                )
            )
        }

        // 2. Hybrid Watch / No-Watch Fallback
        val timelineStartMidnight = Instant.ofEpochMilli(startMillis).atZone(baseZone).toLocalDate()
            .atStartOfDay(baseZone).toInstant().toEpochMilli()
        val bedtimeMinuteOfDay = (((usualBedtimeHour % 24f) + 24f) % 24f * 60f).toInt().coerceIn(0, 1439)
        val wakeMinuteOfDay = (((usualWakeHour % 24f) + 24f) % 24f * 60f).toInt().coerceIn(0, 1439)

        val transferMillis = hotelTransferMinutes.coerceAtLeast(30L) * 60_000L
        fun transferBeforeDuty(duty: CalendarEventItem): Long = transferMillis
        fun transferAfterDuty(duty: CalendarEventItem): Long = transferMillis"""

new_bstb_def = """    private fun buildSleepTimelineBlocks(
        nowMillis: Long,
        startMillis: Long,
        endMillis: Long,
        recordedSessions: List<SleepSessionItem>,
        duties: List<CalendarEventItem>,
        homeBase: String,
        baseZone: ZoneId,
        biologicalPhaseShiftHours: Float,
        targetMinutes: Long,
        usualBedtimeHour: Float,
        usualWakeHour: Float,
        hotelTransferMinutes: Long,
        homeCommuteMinutes: Long = 30L
    ): List<SleepWindowBlock> {
        val blocks = mutableListOf<SleepWindowBlock>()

        // 1. Add actual recorded sleep sessions (Watch / Health Connect / Manual Override)
        recordedSessions.filter { it.endMillis >= startMillis && it.startMillis <= endMillis }.forEach { s ->
            blocks.add(
                SleepWindowBlock(
                    startMillis = s.startMillis,
                    endMillis = s.endMillis,
                    isRecorded = true,
                    label = "Recorded sleep"
                )
            )
        }

        // 2. Hybrid Watch / No-Watch Fallback
        val timelineStartMidnight = Instant.ofEpochMilli(startMillis).atZone(baseZone).toLocalDate()
            .atStartOfDay(baseZone).toInstant().toEpochMilli()
        val bedtimeMinuteOfDay = (((usualBedtimeHour % 24f) + 24f) % 24f * 60f).toInt().coerceIn(0, 1439)
        val wakeMinuteOfDay = (((usualWakeHour % 24f) + 24f) % 24f * 60f).toInt().coerceIn(0, 1439)

        val hotelTransferMillis = hotelTransferMinutes.coerceAtLeast(30L) * 60_000L
        val homeCommuteMillis = homeCommuteMinutes.coerceAtLeast(15L) * 60_000L

        fun transferBeforeDuty(duty: CalendarEventItem): Long {
            return if (duty.isOutOfBase) hotelTransferMillis else homeCommuteMillis
        }

        fun transferAfterDuty(duty: CalendarEventItem): Long {
            return if (duty.isOutOfBase) hotelTransferMillis else homeCommuteMillis
        }"""

if old_bstb_def in fe_content:
    fe_content = fe_content.replace(old_bstb_def, new_bstb_def)

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\FatigueEngine.kt', 'w', encoding='utf-8') as f:
    f.write(fe_content)

print("FATIGUE ENGINE UPDATED")


# 2. Update CalendarSyncManager.kt
with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\CalendarSyncManager.kt', 'r', encoding='utf-8') as f:
    csm_content = f.read()

old_parse_route = """    fun parseRouteAirports(title: String): List<String> {
        val normalized = LOWER_TO_BETWEEN_CODES.replace(title, "-")
        for (match in ROUTE_CHAIN.findAll(normalized)) {
            val codes = match.value.split(ROUTE_SEPARATOR).filter { it.length == 3 }
            if (codes.size < 2) continue
            if (codes.any { it in NON_ROUTE_CODES }) continue
            if (codes.any { AirportDatabase.timeZoneForCode(it) == null }) continue
            return codes
        }
        return emptyList()
    }"""

new_parse_route = """    fun parseRouteAirports(title: String, customAirfields: List<String> = emptyList()): List<String> {
        val normalized = LOWER_TO_BETWEEN_CODES.replace(title, "-")
        for (match in ROUTE_CHAIN.findAll(normalized)) {
            val codes = match.value.split(ROUTE_SEPARATOR).filter { it.length >= 3 }
            if (codes.size < 2) continue
            if (codes.any { it in NON_ROUTE_CODES }) continue
            if (codes.any { AirportDatabase.timeZoneForCode(it) == null && !customAirfields.contains(it) }) continue
            return codes
        }
        return emptyList()
    }"""

if old_parse_route in csm_content:
    csm_content = csm_content.replace(old_parse_route, new_parse_route)

# Pass customAirfieldsList into parseRouteAirports in fetchCrewCalendars
old_fetch_parse = """val airports = parseRouteAirports("$title $location")"""
new_fetch_parse = """val customAirfieldsStr = userPrefs.getString("custom_airfields_list", "") ?: ""
        val customAirfieldsList = customAirfieldsStr.split(',', ';').map { it.trim().uppercase(Locale.ROOT) }
        val airports = parseRouteAirports("$title $location", customAirfieldsList)"""

if old_fetch_parse in csm_content:
    csm_content = csm_content.replace(old_fetch_parse, new_fetch_parse)

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\CalendarSyncManager.kt', 'w', encoding='utf-8') as f:
    f.write(csm_content)

print("CALENDAR SYNC MANAGER UPDATED")
