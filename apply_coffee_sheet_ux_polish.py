import re

with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'@Composable\s+fun CoffeeLoggingBottomSheet[\s\S]*?^\}\s*^\}', re.MULTILINE)

new_sheet_code = """@Composable
fun CoffeeLoggingBottomSheet(
    palette: AppPalette,
    onDismiss: () -> Unit,
    onLogUpdated: () -> Unit
) {
    val context = LocalContext.current
    var selectedHoursAgo by remember { mutableStateOf(0.0) }
    var selectedMg by remember { mutableIntStateOf(150) }
    var selectedLabel by remember { mutableStateOf("☕☕ Double Espresso (~150mg)") }

    var currentIngestions by remember { mutableStateOf(CaffeineSimulator.loadIngestions(context)) }
    val now = System.currentTimeMillis()
    val activePlasmaMg = remember(currentIngestions, now) {
        CaffeineSimulator.calculateActiveCaffeine(currentIngestions, now)
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Log & Manage Caffeine", fontWeight = FontWeight.Bold, fontSize = 16.sp, color = palette.textPrimary)
                Surface(
                    color = Color(0xFFE6F4F1),
                    shape = RoundedCornerShape(8.dp),
                    border = BorderStroke(1.dp, palette.accentTeal)
                ) {
                    Text(
                        "${activePlasmaMg.toInt()}mg Active",
                        color = palette.accentTeal,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }
            }
        },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState())) {
                Text("Pharmacokinetic t½ = 5.5h · 18.3h Espresso Backtrack Model", fontSize = 11.sp, color = palette.textSecondary)

                // 1. Time Offset Selector (Single line horizontal chips, no vertical wrapping)
                Text("When did you drink it?", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = palette.textPrimary)
                Row(horizontalArrangement = Arrangement.spacedBy(4.dp), modifier = Modifier.fillMaxWidth()) {
                    listOf(
                        0.0 to "Now",
                        1.0 to "1h ago",
                        2.0 to "2h ago",
                        4.0 to "4h ago"
                    ).forEach { (hrs, label) ->
                        Surface(
                            onClick = { selectedHoursAgo = hrs },
                            color = if (selectedHoursAgo == hrs) Color(0xFFE6F4F1) else palette.subCardBg,
                            shape = RoundedCornerShape(8.dp),
                            border = BorderStroke(1.dp, if (selectedHoursAgo == hrs) palette.accentTeal else palette.cardBorder),
                            modifier = Modifier.weight(1f)
                        ) {
                            Box(contentAlignment = Alignment.Center, modifier = Modifier.padding(vertical = 6.dp)) {
                                Text(
                                    text = label,
                                    fontSize = 11.sp,
                                    fontWeight = if (selectedHoursAgo == hrs) FontWeight.Bold else FontWeight.Medium,
                                    color = if (selectedHoursAgo == hrs) palette.accentTeal else palette.textPrimary,
                                    maxLines = 1
                                )
                            }
                        }
                    }
                }

                // 2. Streamlined 2-Column Grid for Dose Presets
                Text("Caffeine product & dose", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = palette.textPrimary)
                val presetRows = listOf(
                    listOf(150 to "☕☕ Double Espresso (~150mg)", 160 to "⚡⚡ Large Energy (~160mg)"),
                    listOf(100 to "💊 Caffeine Tablet (~100mg)", 65 to "☕ Single Espresso (~65mg)"),
                    listOf(180 to "☕ Cold Brew (~180mg)", 80 to "⚡ Standard Energy (~80mg)")
                )

                Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    presetRows.forEach { rowPairs ->
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.fillMaxWidth()) {
                            rowPairs.forEach { (mg, label) ->
                                val selected = selectedMg == mg
                                Surface(
                                    onClick = {
                                        selectedMg = mg
                                        selectedLabel = label
                                    },
                                    color = if (selected) Color(0xFFE6F4F1) else palette.subCardBg,
                                    shape = RoundedCornerShape(8.dp),
                                    border = BorderStroke(1.dp, if (selected) palette.accentTeal else palette.cardBorder),
                                    modifier = Modifier.weight(1f)
                                ) {
                                    Text(
                                        text = label,
                                        color = if (selected) palette.accentTeal else palette.textPrimary,
                                        fontSize = 11.sp,
                                        fontWeight = if (selected) FontWeight.Bold else FontWeight.Normal,
                                        maxLines = 1,
                                        overflow = TextOverflow.Ellipsis,
                                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 8.dp)
                                    )
                                }
                            }
                        }
                    }
                }

                // 3. Add to Engine Button with Instant Toast Confirmation
                Button(
                    onClick = {
                        CaffeineSimulator.saveIngestion(context, selectedMg, selectedHoursAgo, selectedLabel)
                        currentIngestions = CaffeineSimulator.loadIngestions(context)
                        onLogUpdated()
                        android.widget.Toast.makeText(context, "Logged ${selectedLabel}! Active caffeine updated.", android.widget.Toast.LENGTH_SHORT).show()
                    },
                    colors = ButtonDefaults.buttonColors(containerColor = palette.accentButtonBg),
                    shape = RoundedCornerShape(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("+ Add to Engine", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }

                Divider(color = palette.cardBorder, thickness = 1.dp)

                // 4. Visible Active Log List & Delete Buttons
                Text("Active Log (${currentIngestions.size} items)", fontSize = 12.sp, fontWeight = FontWeight.Bold, color = palette.textPrimary)

                if (currentIngestions.isEmpty()) {
                    Text("No active caffeine logged.", fontSize = 11.sp, color = palette.textSecondary)
                } else {
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        currentIngestions.forEach { item ->
                            val timeStr = DateTimeFormatter.ofPattern("HH:mm", Locale.ENGLISH)
                                .withZone(ZoneId.systemDefault())
                                .format(Instant.ofEpochMilli(item.timestampMillis))

                            Surface(
                                color = palette.subCardBg,
                                shape = RoundedCornerShape(8.dp),
                                border = BorderStroke(1.dp, palette.cardBorder),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(item.label, fontSize = 11.sp, fontWeight = FontWeight.Bold, color = palette.textPrimary)
                                        Text("Logged at $timeStr · ${item.milligrams}mg", fontSize = 9.5.sp, color = palette.textSecondary)
                                    }
                                    IconButton(
                                        onClick = {
                                            CaffeineSimulator.removeIngestion(context, item.id)
                                            currentIngestions = CaffeineSimulator.loadIngestions(context)
                                            onLogUpdated()
                                        },
                                        modifier = Modifier.size(24.dp)
                                    ) {
                                        Text("✕", color = Color.Red, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = onDismiss,
                colors = ButtonDefaults.buttonColors(containerColor = palette.accentButtonBg),
                shape = RoundedCornerShape(10.dp)
            ) {
                Text("Done", color = Color.White, fontWeight = FontWeight.Bold)
            }
        }
    )
}"""

match = pattern.search(content)
if match:
    content = content[:match.start()] + new_sheet_code + content[match.end():]
    with open(r'C:\Users\user\AndroidStudioProjects\Restwise\app\src\main\java\com\restwise\app\MainActivity.kt', 'w', encoding='utf-8') as f:
        f.write(content)
    print("APPLIED COFFEE SHEET UX POLISH SUCCESSFULLY")
else:
    print("PATTERN NOT FOUND")
