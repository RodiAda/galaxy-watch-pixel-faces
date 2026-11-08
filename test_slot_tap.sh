#!/bin/bash
export ANDROID_SERIAL=${ANDROID_SERIAL:?set ANDROID_SERIAL}
OUT=$1; X=$2; Y=$3; mkdir -p "$OUT"
old=$(adb shell settings get system screen_off_timeout)
trap "adb shell settings put system screen_off_timeout $old" EXIT
adb shell settings put system screen_off_timeout 120000
top(){ adb shell dumpsys activity activities | grep -m1 topResumedActivity; }
ined(){ top | grep -q WatchFaceEditor; }
for a in 1 2 3 4; do
  adb shell input keyevent KEYCODE_HOME; sleep 1; adb shell input keyevent KEYCODE_WAKEUP; sleep 1; adb logcat -c
  adb shell input swipe 200 230 201 231 1600
  for i in 1 2 3 4 5 6; do sleep 1; adb logcat -d | grep -q 'showPicker: end' && break; done
  sleep 1.5; adb shell input tap 225 383
  for i in $(seq 15); do sleep 1; ined && break; done
  ined && break
done
ined || { echo no-editor; exit 1; }
sleep 3
for p in 1 2 3 4 5 6 7 8 9 10 11 12; do
  ined || { echo editor-closed; exit 1; }
  adb shell uiautomator dump /sdcard/ui.xml >/dev/null 2>&1; adb shell cat /sdcard/ui.xml > "$OUT/ui$p.xml"
  grep -qE 'class="android.view.View"[^>]*content-desc="[^"]+"|content-desc="[^"]+"[^>]*class="android.view.View"' "$OUT/ui$p.xml" && break
  if [ $p -le 5 ]; then adb shell input swipe 400 225 50 225 300; else adb shell input swipe 130 225 420 225 300; fi; sleep 2
done
ined || { echo editor-closed; exit 1; }
adb exec-out screencap -p > "$OUT/page.png"
if [ -z "$2" ]; then read X Y < <(python3 -I -c "
import re,sys
s=open(sys.argv[1]).read()
for n in re.findall(r'<node [^>]*>',s):
  if 'class=\"android.view.View\"' in n and re.search(r'content-desc=\"[^\"]+\"',n):
    a,b,c,d=map(int,re.search(r'bounds=\"\[(\d+),(\d+)\]\[(\d+),(\d+)\]',n).groups()); print((a+c)//2,(b+d)//2); break
" "$OUT/ui$p.xml"); fi
echo "tap $X $Y"
adb logcat -c; adb shell input tap $X $Y; sleep 5
adb exec-out screencap -p > "$OUT/after.png"
top | grep -oE '[A-Za-z.]+/[A-Za-z.$]+'
adb logcat -d > "$OUT/log.txt"
grep -E 'TAP|FATAL|AndroidRuntime|VerifyError' "$OUT/log.txt" | cut -c1-220 | head -5
