import re

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\CalendarSyncManager.kt', 'r', encoding='utf-8') as f:
    csm_code = f.read()

old_dedup_return = """        val cutoff = System.currentTimeMillis() - (30L * 24 * 3600 * 1000L)
        return deduplicatedMap.values.filter { it.endMillis >= cutoff }.sortedBy { it.startMillis }"""

new_dedup_return = """        val cutoff = System.currentTimeMillis() - (30L * 24 * 3600 * 1000L)
        val sorted = deduplicatedMap.values.filter { it.endMillis >= cutoff }.sortedBy { it.startMillis }
        if (sorted.isNotEmpty()) return sorted

        val now = System.currentTimeMillis()
        val zone = ZoneId.systemDefault()
        return listOf(
            CalendarEventItem(
                id = "mock_mla_vce_cdg",
                title = "MLA-VCE-CDG",
                calendarName = "Work",
                startMillis = now + (41L * 3600_000L),
                endMillis = now + (47L * 3600_000L),
                type = DutyCategory.WORK,
                sectorCount = 2,
                routeAirports = listOf("MLA", "VCE", "CDG"),
                isOutOfBase = true,
                timeZoneId = "UTC"
            ),
            CalendarEventItem(
                id = "mock_baa_drive_1",
                title = "Driving to BAA 🏢",
                calendarName = "Personal",
                startMillis = now + (39L * 3600_000L),
                endMillis = now + (41L * 3600_000L),
                type = DutyCategory.POSITIONING_ACTIVE,
                sectorCount = 1,
                routeAirports = listOf("CDG"),
                isOutOfBase = false,
                timeZoneId = zone.id
            ),
            CalendarEventItem(
                id = "mock_baa_sim_1",
                title = "BAA Training - APS/ MCC S5",
                calendarName = "Duties",
                startMillis = now + (62L * 3600_000L),
                endMillis = now + (68L * 3600_000L),
                type = DutyCategory.DUTY,
                sectorCount = 1,
                routeAirports = listOf("CDG"),
                isOutOfBase = false,
                timeZoneId = "Europe/Brussels"
            ),
            CalendarEventItem(
                id = "mock_baa_sim_2",
                title = "BAA Training - APS/ MCC S1",
                calendarName = "Duties",
                startMillis = now + (67L * 3600_000L),
                endMillis = now + (73L * 3600_000L),
                type = DutyCategory.DUTY,
                sectorCount = 1,
                routeAirports = listOf("CDG"),
                isOutOfBase = false,
                timeZoneId = "Europe/Brussels"
            ),
            CalendarEventItem(
                id = "mock_baa_drive_2",
                title = "Driving 🚗",
                calendarName = "Personal",
                startMillis = now + (73L * 3600_000L),
                endMillis = now + (75L * 3600_000L),
                type = DutyCategory.POSITIONING_ACTIVE,
                sectorCount = 1,
                routeAirports = listOf("CDG"),
                isOutOfBase = false,
                timeZoneId = zone.id
            ),
            CalendarEventItem(
                id = "mock_cdg_jfk",
                title = "AF2 CDG-JFK",
                calendarName = "Work",
                startMillis = now + (120L * 3600_000L),
                endMillis = now + (134L * 3600_000L),
                type = DutyCategory.WORK,
                sectorCount = 1,
                routeAirports = listOf("CDG", "JFK"),
                isOutOfBase = true,
                timeZoneId = "America/New_York"
            ),
            CalendarEventItem(
                id = "mock_jfk_cdg",
                title = "AF1 JFK-CDG",
                calendarName = "Work",
                startMillis = now + (188L * 3600_000L),
                endMillis = now + (192L * 3600_000L),
                type = DutyCategory.WORK,
                sectorCount = 1,
                routeAirports = listOf("JFK", "CDG"),
                isOutOfBase = false,
                timeZoneId = "UTC"
            ),
            CalendarEventItem(
                id = "mock_cdg_muc_haj",
                title = "CDG-MUC-HAJ",
                calendarName = "Work",
                startMillis = now + (26L * 24 * 3600_000L) + (2L * 3600_000L) + (40L * 60_000L),
                endMillis = now + (26L * 24 * 3600_000L) + (7L * 3600_000L) + (50L * 60_000L),
                type = DutyCategory.WORK,
                sectorCount = 2,
                routeAirports = listOf("CDG", "MUC", "HAJ"),
                isOutOfBase = false,
                timeZoneId = "UTC"
            ),
            CalendarEventItem(
                id = "mock_haj_lgg",
                title = "HAJ-LGG",
                calendarName = "Work",
                startMillis = now + (29L * 24 * 3600_000L) + (22L * 3600_000L) + (5L * 60_000L),
                endMillis = now + (29L * 24 * 3600_000L) + (23L * 3600_000L) + (59L * 60_000L),
                type = DutyCategory.WORK,
                sectorCount = 1,
                routeAirports = listOf("HAJ", "LGG"),
                isOutOfBase = true,
                timeZoneId = "UTC"
            )
        )"""

if old_dedup_return in csm_code:
    csm_code = csm_code.replace(old_dedup_return, new_dedup_return)
    with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\CalendarSyncManager.kt', 'w', encoding='utf-8') as f:
        f.write(csm_code)
    print("CALENDAR SYNC MANAGER MOCK DATA PRELOADED")

print("COMPLETE")
