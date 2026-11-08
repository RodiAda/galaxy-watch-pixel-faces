# Pixel Watch faces on Galaxy Watch5

Google Pixel Watch Faces 5.0.231.924930285 (`com.google.android.wearable.watchface.rwf`, Android 16+, from APKMirror,
SHA-256 `ddbe8fc4663123afacca057f412c3baa01691535dd12a91311a255158078b9db`, signed by Google) patched to run on a
Galaxy Watch5 SM-R910 (Wear OS 6, API 36, firmware R910XXS2DZG3, Wear Services v16).

## Build

```
./build.sh                    # -> dist/rwf-patched.apk
adb install -r dist/rwf-patched.apk
adb shell pm grant com.google.android.wearable.watchface.rwf android.permission.health.READ_HEART_RATE
adb shell pm grant com.google.android.wearable.watchface.rwf android.permission.health.READ_HEALTH_DATA_IN_BACKGROUND
adb shell pm grant com.google.android.wearable.watchface.rwf android.permission.ACTIVITY_RECOGNITION
```

The first install over the Google-signed package needs `adb uninstall com.google.android.wearable.watchface.rwf`.
Signing key: `keys/watch.jks`, alias `watch`, password from `KS_PASS` (stored in Bitwarden). Losing it means
uninstalling and losing watch face favorites/settings on the next update.

Tools: apktool 3.0.3, uber-apk-signer 1.3.0 (in `tools/`).

## Patches

| file | problem on Samsung | fix |
|---|---|---|
| `10_colorpicker.py` | Wear Services v16 parser rejects `ColorUserStyleSetting` | converted to `ListUserStyleSetting` with generated swatch drawables |
| `20_device_check_and_manifest.py` | app refuses to start without `PIXEL_WATCH_EXPERIENCE`; Samsung picker ignores `PIXEL_WATCH_FACE` category | check forced; `WATCH_FACE` category added, services exported (still guarded by `BIND_WALLPAPER`); Tubes offload check skipped at startup |
| `30_offload_and_pele.py` | `com.google.wear.displayoffload.DisplayOffloadManager` missing; Koru faces gated on `pele-runtime.google.version` | `gwl` tolerates missing manager; `fbk.az` returns true (Samsung ships `pele-runtime` with feature `pele-runtime.samsung.version-1`) |
| `40_headless_init.py` | editor headless instances skip Hilt `onCreate` → `lateinit watchFaceConfiguration` | `gwy.I()` lazily fills static-provided fields `l,m,n,p,q` |
| `50_strip_flavors.py` | Wear Services rebuilds flavors nonstop, resolving Fitbit / Google Weather providers | `UserStyleFlavors` removed, `FLAVORS_SUPPORTED=false` |
| `60_koru_events.py` | Samsung pele runtime does not know `toInteractive` / `toAmbient` (Orbita rings missing, GLUI cache not written, editor lag) | renamed to `hipower` / `lopower` |
| `65_linear_expressions.py` | Samsung pele `ComplicationLinear` has no `title`/`text` attributes, dynamic-expression text in linear complications was dropped | expressions bound to `text-buffer` of the text elements, like the round complication |
| `70_safe_settings.py` | reading hidden settings (`rsb_wake_enabled`) throws `SecurityException` and kills the process | `Settings.*.get*` routed through `rwfcompat.SafeSettings` returning defaults |
| `80_safe_pele.py` | Samsung pele runtime throws `IllegalArgumentException` on unknown attributes/events (Tubes `DistanceColorAndScale.color-start`) | `setAttribute` / `sendCustomEventToAll` routed through `rwfcompat.SafePele` |
| `90_editor_timeout.py` | editor session creation exceeds the 4 s `withTimeout` on this watch | 4000 ms timeouts raised to 15000 ms in `iug.k` / `iug.l` |
| `95_headless_oncreate.py` | headless instances still miss Hilt fields (`modularColorBandMatchingConfiguration`, `artworkFetcher`) | `dkz.ez` calls `onCreate()` after `attachBaseContext`; `iht.eu` falls back to `getApplicationContext()` |
| `97_editor_tap.py` | Koru tap filter asks the pele runtime which element was hit; in the headless editor instance nothing processes the tap, so complication slots cannot be selected | if the runtime did not process the tap, fall back to the slot bounds |

Obfuscated class names (`gwl`, `gwy`, `fbk`, `hak`, ...) are specific to this APK version.

## Applying a face without the picker

```
adb shell am broadcast -a com.google.android.wearable.app.DEBUG_SURFACE \
  --es operation set-watchface \
  --es watchFaceId com.google.android.wearable.watchface.rwf/com.google.android.wearable.watchface.pilot.PilotWatchFaceService
```

Every call adds a favorite. The first attempt after install often fails during warm-up.

`test_faces.sh OUTDIR "<services>"` applies each face, opens Customize from the picker and stores screenshots and logs.
`test_editor_retry.sh OUTDIR "<services>"` does the same with up to 3 attempts per face and prints one result line per face.
Both set `svc power stayon true` and reset it on exit.
`test_slot_tap.sh OUTDIR [X Y]` opens the editor, finds the complications page and taps a slot.

## Status

See `NOTES.md`.
