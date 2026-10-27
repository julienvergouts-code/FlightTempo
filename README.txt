Restwise roster, recovery, and travel-model overlay v16

Apply this ZIP to the Android Studio project root and replace matching files. Then sync Gradle and launch the app.

Fixes in v16:
- Destination METAR now follows the nearest upcoming event that has an actual route, rather than stopping at the next non-route calendar event (such as instruction or simulator duty).
- Changing selected calendars or an event's travel/duty override refreshes the destination weather.
- Destination METAR is displayed independently of the local METAR, so a missing local report no longer hides a valid destination report.
- Adds ICAO mappings for ATL, IAH, MUC, ORY, and IST.
- Second-job calendar events can be interpreted as Simulator, Aircraft, or Training when a saved second-job keyword matches.
- Actual route events and explicit flying titles remain classified as flying even when they match second-job keywords; explicit simulator and training duties remain non-flying duty.

Retains v15 and earlier changes:
- Restores the missing `events: List<CalendarEventItem>` parameter on InteractiveScheduleTabView.
- Calendar source selection is only in My Roster.
- Work profile selection, second-job role / keywords, and IATA / ICAO home-base input.
- Now-screen sleep schedule at the bottom with 14-day and 28-day update actions.
- Extended Health Connect HRV and resting-heart-rate query/cache window.
- Gradual itinerary-based circadian adjustment after time-zone travel.
- Career sleep-debt and preceding graph / daylight / travel updates.

Validation:
- Reviewed the changed source and retained the v15 function-signature correction.
- A full Gradle build has not been run for this package; the previous attempt was blocked because Gradle 9.6.0 was not cached and services.gradle.org was unreachable.
- The original Android Studio project is not overwritten by this overlay.

Included files:
- app/src/main/java/com/restwise/app/CalendarSyncManager.kt
- app/src/main/java/com/restwise/app/FatigueEngine.kt
- app/src/main/java/com/restwise/app/HealthConnectManager.kt
- app/src/main/java/com/restwise/app/MainActivity.kt
- app/src/main/AndroidManifest.xml
- app/src/main/res/values/health_permissions.xml
- app/src/test/java/com/restwise/app/FatigueRepairTest.kt
