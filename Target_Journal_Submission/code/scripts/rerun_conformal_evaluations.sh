#!/bin/bash
# Rerun all conformal evaluations with the extended comparator set (sequential stages, 4 workers each)
set -e
cd /home/user/p_c1_4/Target_Journal_Submission/code
L=../results/experiment_logs
echo "start $(date +%T)"
python3 -W ignore experiments/e04_within_cohort.py --stagers yasa lgbm_sc_s0 --workers 4 > $L/e04_main.log 2>&1; echo "E04 main done $(date +%T)"
python3 -W ignore experiments/e06_cross_cohort.py --stagers yasa lgbm_sc_s0 > $L/e06.log 2>&1; echo "E06 done $(date +%T)"
python3 -W ignore experiments/e07_utility_and_stats.py > $L/e07.log 2>&1; echo "E07 done $(date +%T)"
python3 -W ignore experiments/e08_error_analysis.py > $L/e08.log 2>&1; echo "E08 done $(date +%T)"
python3 -W ignore experiments/e09_robustness.py --skip-predict --workers 4 > $L/e09.log 2>&1; echo "E09 done $(date +%T)"
python3 -W ignore experiments/e04_within_cohort.py --stagers lgbm_sc_s1 lgbm_sc_s2 --no-loso --workers 4 > $L/e04_seeds.log 2>&1; echo "E04 seeds done $(date +%T)"
python3 -W ignore experiments/e10_efficiency.py > $L/e10.log 2>&1; echo "E10 done $(date +%T)"
echo CHAIN2_DONE
