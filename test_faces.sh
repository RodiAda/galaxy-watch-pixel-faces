#!/bin/bash
export ANDROID_SERIAL=${ANDROID_SERIAL:?set ANDROID_SERIAL}
P=com.google.android.wearable.watchface.rwf
OUT=$1; mkdir -p "$OUT"
trap "adb shell svc power stayon false" EXIT
adb shell svc power stayon true
faces="$2"
for s in $faces; do
  short=${s##*.}; short=${short%WatchFaceService}
  adb shell input keyevent KEYCODE_WAKEUP; adb shell input keyevent KEYCODE_HOME; sleep 1
  r=$(adb shell am broadcast -a com.google.android.wearable.app.DEBUG_SURFACE --es operation set-watchface --es watchFaceId $P/$s | tail -1)
  for i in $(seq 1 25); do
    sleep 1
    cur=$(adb shell dumpsys wallpaper | grep -m1 -oE '[A-Za-z0-9]+WatchFaceService'); cur=${cur%WatchFaceService}
    [ "$cur" = "$short" ] && break
  done
  sleep 2
  adb shell input keyevent KEYCODE_WAKEUP; sleep 0.5
  adb exec-out screencap -p > "$OUT/$short-face.png"
  adb logcat -c
  adb shell input tap 225 20; sleep 0.8
  adb shell input swipe 200 230 201 231 1500; sleep 4
  adb shell input tap 225 383; sleep 6
  adb exec-out screencap -p > "$OUT/$short-editor.png"
  log=$(adb logcat -d); echo "$log" > "$OUT/$short.log"
  started=$(echo "$log" | grep -c 'START u0 {act=androidx.wear.watchface.editor')
  fail=$(echo "$log" | grep -cE 'Unable to create createOnWatchEditorSession|WatchFace crashed|FATAL EXCEPTION')
  err=$(echo "$log" | grep -m1 -oE '(Caused by|imd|IllegalStateException|NullPointerException)[^\r]{0,110}')
  top=$(adb shell dumpsys activity activities | grep -m1 topResumedActivity | grep -oE '[A-Za-z]+Activity')
  applied=$([ "$cur" = "$short" ] && echo yes || echo "no($cur)")
  echo "$short | applied=$applied | editorStarted=$started | fail=$fail | top=$top | $err"
  adb shell input keyevent KEYCODE_BACK; sleep 1; adb shell input keyevent KEYCODE_BACK; sleep 1
done
