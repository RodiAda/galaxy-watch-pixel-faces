#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
W=build/work; rm -rf build; mkdir -p build dist
java -jar tools/apktool_3.0.3.jar d -s -f -o build/orig original/rwf-5.0.231.924930285.apk >/dev/null
java -jar tools/apktool_3.0.3.jar d -f -o $W original/rwf-5.0.231.924930285.apk >/dev/null
python3 -I patches/10_colorpicker.py build/orig $W
for p in patches/20_*.py patches/30_*.py patches/40_*.py patches/50_*.py patches/60_*.py patches/65_*.py patches/70_*.py patches/80_*.py patches/90_*.py patches/95_*.py patches/97_*.py; do python3 -I "$p" $W; done
java -jar tools/apktool_3.0.3.jar b -o build/unsigned.apk $W >/dev/null
java -jar tools/uber-apk-signer-1.3.0.jar -a build/unsigned.apk --ks keys/watch.jks --ksAlias watch --ksPass "${KS_PASS:?set KS_PASS}" --ksKeyPass "${KS_PASS:?set KS_PASS}" -o build/signed >/dev/null
cp build/signed/unsigned-aligned-signed.apk dist/rwf-patched.apk
echo dist/rwf-patched.apk
