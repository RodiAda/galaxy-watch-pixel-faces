#!/bin/bash
export ANDROID_SERIAL=${ANDROID_SERIAL:?set ANDROID_SERIAL}
P=com.google.android.wearable.watchface.rwf
OUT=$1; mkdir -p "$OUT"
trap "adb shell svc power stayon false" EXIT
adb shell svc power stayon true
for s in $2; do
  short=${s##*.}; short=${short%WatchFaceService}
  adb shell input keyevent KEYCODE_WAKEUP; adb shell input keyevent KEYCODE_HOME; sleep 1
  adb shell am broadcast -a com.google.android.wearable.app.DEBUG_SURFACE --es operation set-watchface --es watchFaceId $P/$s >/dev/null
  for i in $(seq 1 25); do sleep 1; cur=$(adb shell dumpsys wallpaper | grep -m1 -oE '[A-Za-z0-9]+WatchFaceService'); [ "${cur%WatchFaceService}" = "$short" ] && break; done
  sleep 3
  result=no-picker
  for attempt in 1 2 3; do
    adb logcat -c
    adb shell input keyevent KEYCODE_WAKEUP; sleep 0.5; adb shell input tap 225 20; sleep 1
    adb shell input swipe 200 230 201 231 1600
    for i in $(seq 1 8); do sleep 1; adb logcat -d | grep -q 'showPicker: end' && break; done
    adb logcat -d | grep -q 'showPicker: end' || { adb shell input keyevent KEYCODE_HOME; continue; }
    sleep 2
    adb shell input tap 225 383
    for i in $(seq 1 12); do sleep 1; adb logcat -d | grep -qE 'Session started|Unable to create createOnWatchEditorSession' && break; done
    sleep 3
    log=$(adb logcat -d); echo "$log" > "$OUT/$short.log"
    adb exec-out screencap -p > "$OUT/$short-editor.png"
    top=$(adb shell dumpsys activity activities | grep -m1 topResumedActivity | grep -oE '[A-Za-z]+Activity' | tail -1)
    if echo "$log" | grep -q 'Unable to create createOnWatchEditorSession'; then result="editor-failed: $(echo "$log" | grep -A1 'Unable to create createOnWatchEditorSession' | tail -1 | cut -c33-140)"
    elif [ "$top" = WatchFaceEditorActivity ]; then result=editor-ok
    elif echo "$log" | grep -q 'Clicked Customize'; then result="clicked-but-top=$top"
    else result=no-click; adb shell input keyevent KEYCODE_BACK; sleep 1; continue
    fi
    break
  done
  echo "$short | attempt=$attempt | $result"
  adb shell input keyevent KEYCODE_BACK; sleep 1; adb shell input keyevent KEYCODE_BACK; sleep 1
done
