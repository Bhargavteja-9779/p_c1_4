#!/usr/bin/env bash
# Download the public datasets used in this study (PhysioNet open-access mirrors on AWS S3).
#   Sleep-EDF Expanded v1.0.0 (Kemp et al. 2000; doi:10.13026/C2X676)        ~8.2 GB
#   HMC Sleep Staging Database v1.1 (Alvarez-Estevez & Rijsman 2021; doi:10.13026/t79q-fr32) ~16 GB
# Usage: bash scripts/download_data.sh [DATA_ROOT]   (default: code/data/raw)
# Both datasets are open access (Sleep-EDF: ODC-By 1.0; HMC: CC BY 4.0). Cite them as in the manuscript.
set -euo pipefail
ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)/data/raw}"
S3=https://physionet-open.s3.amazonaws.com
mkdir -p "$ROOT/sleep-edfx/sleep-cassette" "$ROOT/sleep-edfx/sleep-telemetry" "$ROOT/hmc/recordings"

cd "$ROOT/sleep-edfx"
for f in RECORDS SHA256SUMS.txt SC-subjects.xls ST-subjects.xls; do curl -sSL --retry 3 "$S3/sleep-edfx/1.0.0/$f" -o "$f"; done
awk '{print $2}' SHA256SUMS.txt | grep -E "\.edf$" | xargs -P 8 -I{} sh -c \
  'test -s "{}" || curl -sSL --retry 3 "'$S3'/sleep-edfx/1.0.0/{}" -o "{}"'
grep -E "\.edf$" SHA256SUMS.txt | sha256sum -c --quiet && echo "Sleep-EDF checksums OK"

cd "$ROOT/hmc"
for f in RECORDS SHA256SUMS.txt Subjects_info_aggregated.txt LICENSE.txt; do curl -sSL --retry 3 "$S3/hmc-sleep-staging/1.1/$f" -o "$f"; done
awk '{print $2}' SHA256SUMS.txt | grep recordings/ | grep -E "\.(edf|txt)$" | grep -v sleepscoring.edf | \
  xargs -P 8 -I{} sh -c 'test -s "{}" || curl -sSL --retry 3 "'$S3'/hmc-sleep-staging/1.1/{}" -o "{}"'
grep recordings/ SHA256SUMS.txt | grep -E "\.(edf|txt)$" | grep -v sleepscoring.edf | sha256sum -c --quiet && echo "HMC checksums OK"
echo "Data in $ROOT"
