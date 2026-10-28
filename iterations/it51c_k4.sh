#!/bin/bash
# it51c: akenum3 on K4 for lags given, all 9 models. Output: solutions to out/it51_k4_L<L>_f<f>_k<k>.txt, summary to stdout
CT=$(cat data/ciphertext.txt); CAP=${2:-1000000000}
for L in $1; do for f in 0 1 2; do for k in 0 1 2; do
  iterations/c/akenum3 $CT $L $f $k 2000000 $CAP > iterations/out/it51_k4_L${L}_f${f}_k${k}.txt 2> >(cat)
done; done; done
