#!/bin/bash
# Revision-1 rerun (after cycle-1 review): no-mask convention, new comparators, honest protocol, sensitivity.
set -e
cd "$(dirname "$0")/.."
L=../results/experiment_logs
s() { echo "$1 $(date +%T)"; }
python3 -W ignore experiments/e03_night_summaries.py --workers 4 > $L/e03_night_summaries.log 2>&1; s "E03 done"
python3 -W ignore experiments/e04_within_cohort.py --stagers yasa lgbm_sc_s0 --workers 4 > $L/e04_main.log 2>&1; s "E04 done"
python3 -W ignore experiments/e06_cross_cohort.py --stagers yasa lgbm_sc_s0 > $L/e06.log 2>&1; s "E06 done"
python3 -W ignore experiments/e07_utility_and_stats.py > $L/e07.log 2>&1; s "E07 done"
python3 -W ignore experiments/e08_error_analysis.py > $L/e08.log 2>&1; s "E08 done"
python3 -W ignore experiments/e09_robustness.py --skip-predict --workers 4 > $L/e09.log 2>&1; s "E09 done"
python3 -W ignore experiments/e11_conditional_coverage.py > $L/e11.log 2>&1; s "E11 done"
python3 -W ignore experiments/e12_honest_protocol.py --R 50 > $L/e12.log 2>&1; s "E12 done"
python3 -W ignore experiments/e13_preregistered_sensitivity.py > $L/e13.log 2>&1; s "E13 done"
python3 -W ignore experiments/e14_montage_sensitivity.py > $L/e14.log 2>&1; s "E14 done"
python3 -W ignore experiments/e04_within_cohort.py --stagers lgbm_sc_s1 lgbm_sc_s2 --no-loso --workers 4 > $L/e04_seeds.log 2>&1; s "E04 seeds done"
python3 -W ignore experiments/e10_efficiency.py > $L/e10.log 2>&1; s "E10 done"
echo REVISION1_DONE
