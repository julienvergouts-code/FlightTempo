with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update RestwiseAppRoot to hold timeDisplayMode
old_root_vars = """    var usualWakeTime by remember { mutableStateOf(prefs.getString("usual_wake", "07:00") ?: "07:00") }
    var inferFromWatch by remember { mutableStateOf(prefs.getBoolean("infer_watch", true)) }
    var hotelQualityFactor by remember { mutableFloatStateOf(prefs.getFloat("hotel_quality_factor", 0.85f)) }"""

new_root_vars = """    var usualWakeTime by remember { mutableStateOf(prefs.getString("usual_wake", "07:00") ?: "07:00") }
    var inferFromWatch by remember { mutableStateOf(prefs.getBoolean("infer_watch", true)) }
    var hotelQualityFactor by remember { mutableFloatStateOf(prefs.getFloat("hotel_quality_factor", 0.85f)) }
    var timeDisplayMode by remember { mutableStateOf(prefs.getString("time_display_mode", "LOCAL") ?: "LOCAL") }"""
text = text.replace(old_root_vars, new_root_vars)

# 2. Add to MainContentColumn parameters
old_mcc_sig = """    inferFromWatch: Boolean,
    userBirthday: String,"""

new_mcc_sig = """    inferFromWatch: Boolean,
    userBirthday: String,
    timeDisplayMode: String,
    onTimeDisplayModeChange: (String) -> Unit,"""
text = text.replace(old_mcc_sig, new_mcc_sig)

# 3. Add to MainContentColumn calls in RestwiseAppRoot (wide and compact)
old_mcc_call_wide = """                            inferFromWatch = inferFromWatch,
                            userBirthday = userBirthday,"""

new_mcc_call_wide = """                            inferFromWatch = inferFromWatch,
                            userBirthday = userBirthday,
                            timeDisplayMode = timeDisplayMode,
                            onTimeDisplayModeChange = { mode ->
                                timeDisplayMode = mode
                                prefs.edit { putString("time_display_mode", mode) }
                            },"""
text = text.replace(old_mcc_call_wide, new_mcc_call_wide)

# 4. Pass into CrewSettingsDialog call in RestwiseAppRoot
old_dialog_call = """                        usualWakeTime = usualWakeTime,
                        inferFromWatch = inferFromWatch,
                        events = calendarEvents,"""

new_dialog_call = """                        usualWakeTime = usualWakeTime,
                        inferFromWatch = inferFromWatch,
                        timeDisplayMode = timeDisplayMode,
                        onTimeDisplayModeChange = { mode ->
                            timeDisplayMode = mode
                            prefs.edit { putString("time_display_mode", mode) }
                        },
                        events = calendarEvents,"""
text = text.replace(old_dialog_call, new_dialog_call)

# 5. Add to CrewSettingsDialog parameters
old_dialog_sig = """    usualWakeTime: String,
    inferFromWatch: Boolean,
    events: List<CalendarEventItem> = emptyList(),"""

new_dialog_sig = """    usualWakeTime: String,
    inferFromWatch: Boolean,
    timeDisplayMode: String,
    onTimeDisplayModeChange: (String) -> Unit,
    events: List<CalendarEventItem> = emptyList(),"""
text = text.replace(old_dialog_sig, new_dialog_sig)

# 6. CrewSettingsDialog state and auto-save updates
old_dialog_state = """    var commuteModeDraft by remember(commuteMode) { mutableStateOf(commuteMode) }
    var watchEnabledDraft by remember(inferFromWatch) { mutableStateOf(inferFromWatch) }"""

new_dialog_state = """    var commuteModeDraft by remember(commuteMode) { mutableStateOf(commuteMode) }
    var watchEnabledDraft by remember(inferFromWatch) { mutableStateOf(inferFromWatch) }
    var timeDisplayModeDraft by remember(timeDisplayMode) { mutableStateOf(timeDisplayMode) }"""
text = text.replace(old_dialog_state, new_dialog_state)

old_dialog_persist = """            putBoolean("has_second_employment", hasSecondEmployment)
        }
        saveFreelanceRulesToPrefs(userPrefs, freelanceRules)"""

new_dialog_persist = """            putBoolean("has_second_employment", hasSecondEmployment)
        }
        saveFreelanceRulesToPrefs(userPrefs, freelanceRules)
        onTimeDisplayModeChange(timeDisplayModeDraft)"""
text = text.replace(old_dialog_persist, new_dialog_persist)

old_dialog_launched = """        customKeywords, customAirfields, inferFromWatchDraft, hasSecondEmployment, freelanceRules, removedCodesCSV
    ) {"""

new_dialog_launched = """        customKeywords, customAirfields, inferFromWatchDraft, hasSecondEmployment, freelanceRules, removedCodesCSV,
        timeDisplayModeDraft
    ) {"""
text = text.replace(old_dialog_launched, new_dialog_launched)

# 7. Add to SettingsSectionBody parameters and call
old_body_call = """                                    inferFromWatch = inferFromWatchDraft,
                                    onInferFromWatchChange = { inferFromWatchDraft = it },"""

new_body_call = """                                    inferFromWatch = inferFromWatchDraft,
                                    onInferFromWatchChange = { inferFromWatchDraft = it },
                                    timeDisplayMode = timeDisplayModeDraft,
                                    onTimeDisplayModeChange = { timeDisplayModeDraft = it },"""
text = text.replace(old_body_call, new_body_call)

old_body_sig = """    inferFromWatch: Boolean,
    onInferFromWatchChange: (Boolean) -> Unit,"""

new_body_sig = """    inferFromWatch: Boolean,
    onInferFromWatchChange: (Boolean) -> Unit,
    timeDisplayMode: String,
    onTimeDisplayModeChange: (String) -> Unit,"""
text = text.replace(old_body_sig, new_body_sig)

# 8. Add UI for Time Display Mode in SettingsSectionBody (under AIRLINE)
old_airline_ui = """        SettingsMenuSection.AIRLINE -> {
            Card(
                colors = CardDefaults.cardColors(containerColor = palette.cardBg),
                shape = RoundedCornerShape(18.dp),
                border = BorderStroke(1.dp, palette.cardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("✈ Airline & Roster", color = palette.textPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)"""

new_airline_ui = """        SettingsMenuSection.AIRLINE -> {
            Card(
                colors = CardDefaults.cardColors(containerColor = palette.cardBg),
                shape = RoundedCornerShape(18.dp),
                border = BorderStroke(1.dp, palette.cardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("✈ Airline & Roster", color = palette.textPrimary, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                    Text("Timeline Graph Time Reference", color = palette.textSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxWidth()) {
                        listOf("LOCAL" to "Local Time", "HOME" to "Home Base", "UTC" to "UTC / Zulu").forEach { (mode, label) ->
                            FilterChip(
                                selected = timeDisplayMode == mode,
                                onClick = { onTimeDisplayModeChange(mode) },
                                label = { Text(label, fontSize = 11.sp, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
            }

            Card(
                colors = CardDefaults.cardColors(containerColor = palette.cardBg),
                shape = RoundedCornerShape(18.dp),
                border = BorderStroke(1.dp, palette.cardBorder),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                    Text("Operator Preset Dropdown", color = palette.textSecondary, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)"""
text = text.replace(old_airline_ui, new_airline_ui)

# 9. Update RestwiseGraphTabView definition in MainContentColumn
old_graph_call = """                onShowRoutineChange = onShowRoutineChange,
                dayShiftOffset = dayShiftOffset,
                onDayShiftChange = onDayShiftChange,
                homeBaseIata = homeBaseIata,
                locationInfo = locationInfo,"""

new_graph_call = """                onShowRoutineChange = onShowRoutineChange,
                dayShiftOffset = dayShiftOffset,
                onDayShiftChange = onDayShiftChange,
                homeBaseIata = homeBaseIata,
                locationInfo = locationInfo,
                timeDisplayMode = timeDisplayMode,"""
text = text.replace(old_graph_call, new_graph_call)

# 10. Update RestwiseGraphTabView signature & timezone logic
old_graph_sig = """    dayShiftOffset: Int,
    onDayShiftChange: (Int) -> Unit,
    homeBaseIata: String = "",
    locationInfo: LocationInfo,
    palette: AppPalette,"""

new_graph_sig = """    dayShiftOffset: Int,
    onDayShiftChange: (Int) -> Unit,
    homeBaseIata: String = "",
    locationInfo: LocationInfo,
    timeDisplayMode: String = "LOCAL",
    palette: AppPalette,"""
text = text.replace(old_graph_sig, new_graph_sig)

old_graph_zone = """    val chartPalette = getTimelinePalette(palette)
    val zoneIdStr = locationInfo.timeZoneId.takeIf { it.isNotBlank() && runCatching { ZoneId.of(it) }.isSuccess }
        ?: CalendarSyncManager.airportTimeZoneId(homeBaseIata)
        ?: ZoneId.systemDefault().id
    val zone = runCatching { ZoneId.of(zoneIdStr) }.getOrElse { ZoneId.systemDefault() }
    val realNowMillis = System.currentTimeMillis()"""

new_graph_zone = """    val chartPalette = getTimelinePalette(palette)
    val zoneIdStr = when (timeDisplayMode) {
        "HOME" -> CalendarSyncManager.airportTimeZoneId(homeBaseIata) ?: ZoneId.systemDefault().id
        "UTC" -> "UTC"
        else -> locationInfo.timeZoneId.takeIf { it.isNotBlank() && runCatching { ZoneId.of(it) }.isSuccess }
            ?: CalendarSyncManager.airportTimeZoneId(homeBaseIata)
            ?: ZoneId.systemDefault().id
    }
    val zone = runCatching { ZoneId.of(zoneIdStr) }.getOrElse { ZoneId.systemDefault() }
    val zoneLabel = when (timeDisplayMode) {
        "HOME" -> "HOME: ${zone.id.split("/").lastOrNull() ?: zone.id}"
        "UTC" -> "UTC / ZULU"
        else -> "LOC: ${zone.id.split("/").lastOrNull() ?: zone.id}"
    }
    val realNowMillis = System.currentTimeMillis()"""
text = text.replace(old_graph_zone, new_graph_zone)

old_graph_button = """                        Text("↺", color = palette.accentTeal, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        Text(
                            zoneIdStr,
                            color = palette.accentTeal,"""

new_graph_button = """                        Text("↺", color = palette.accentTeal, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                        Text(
                            zoneLabel,
                            color = palette.accentTeal,"""
text = text.replace(old_graph_button, new_graph_button)

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'w', encoding='utf-8') as f:
    f.write(text)

print("TIME REFERENCE DISPLAY MODE COMPLETED")
