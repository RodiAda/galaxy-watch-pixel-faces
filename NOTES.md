# Status (2026-11-08)

## Verified on the watch (build with patches 10-95)

- All 31 faces apply and render, including Koru faces, Orbita rings.
- Current face after the last session: Modular (temporarily set for testing); the user's face was Orbita.
- Customize opens for every face that has settings: Abstract, Accessible, Active, Adventure, AnalogArc, AnalogBold,
  AnalogClassic, Artist, ArtsAndCulture, BBB, BoldDigital, BoldUtility20, Chronograph, Expedition, Modular, Orbita,
  Pacific, Pilot, PilotBold, Reveal, Rotation, RushHour, SCAnalog, Shapes, TidalPool, TimeInTime, Track2, Tubes,
  WordClock.
- BedtimeMode and Pride have nothing to customize (one colour, one layout); Samsung picker hides the button
  (`animateCustomizeButton: false`), same as on Pixel.
- Tapping a complication in the editor opens the provider chooser (patch 97), selection is applied (checked on Tubes,
  Active).
- Automated long-press is flaky (watch dozes); `test_editor_retry.sh` retries up to 3 times.
- Health permissions granted manually.

## Open

1. Editor fields `gwy.i` / `gwy.o` come from the Hilt component; patch 95 now runs `onCreate`, so likely filled.
   Watch for crashes in `gwy.H()` / `gwy.T()`.
2. Koru faces: `ComplicationLinear.title/text` fixed by patch 65. `offload-status` error is harmless (debug canvas
   with `display: discard`).
3. Tubes: tilt effect cannot work, Samsung libpele lacks the native `DistanceColorAndScale` and `IMUDataHandler`
   widget types (only `ApplicationWidget`, `DefaultWidget`, ...). Tubes render static, colors work.
4. Screen auto-rotate was on (`accelerometer_rotation=1`) and rotated the whole UI; set to 0 on 2026-11-08.
5. Clean up favorites (41 entries, many duplicates): Wear Services has no remove operation in `DEBUG_SURFACE`
   (only `set-watchface`, `unset-watchface`); has to be done through the picker UI. Ask which to keep.
6. Google Weather for Wear OS 1.10.330 (`com.google.android.wearable.weather`, Google-signed, cert SHA-256
   5c869c18...) installed from `original/weather/`, coarse + background location granted. Its `WeatherProviderService`
   offers `RANGED_VALUE`, which Orbita and other faces expect (Samsung weather temperature is `SHORT_TEXT` only, drawn
   small). Samsung weather `AUTOREFRESH` is a non-wakeup RTC alarm (fired 14 times in 17 days).
7. Samsung Health complications for heart rate, water, sleep and food hide data when the face is not in their
   `SAFE_WATCH_FACES` list (empty), Wear Services passes `safe=2` for every third-party face. Cannot be changed without
   re-signing Samsung Health or Wear Services. Heart rate replaced by `~/Проекты/hr-complication` (Health Services
   passive data, `RANGED_VALUE`). Other Samsung providers do not hold `GET_IS_FOR_SAFE_WATCH_FACE` and work.

## Watch connection

Wireless debugging port changes; find it with `avahi-browse -tpr _adb-tls-connect._tcp` (`adb mdns` misses it,
stale entries linger). The PC is paired. In zsh use `ANDROID_SERIAL`, not `-s $S`.

## Debloat

`debloat/disabled-by-claude.txt` lists packages disabled with `pm disable-user` (24); `debloat/*-before.txt` is the
state before. Not to touch: unused Samsung watch faces, Outlook, Spotify, Google Fit/Gmail/Calendar/Home,
Google Camera. Google Calendar is the preferred `APP_CALENDAR` handler.
