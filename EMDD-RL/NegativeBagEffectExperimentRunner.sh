# python 2.7
export PATH=/usr/bin:$PATH
STEP_LIMIT_EQUALLY_BALANCED=1
EQUALLY_BALANCED=3

LINEAR="LINEAR"
EXPONENTIAL="EXPONENTIAL"

H_ALL="H_ALL"
# H_NEIGHBOR="H_NEIGHBOR"
H_SET="H_SET"

DATASET_ARRAY=($STEP_LIMIT_EQUALLY_BALANCED $EQUALLY_BALANCED)
ALGORITHM_ARRAY=("EMDD" "DD")
SEARCH_ARRAY=($H_ALL $H_SET)
METHOD_ARRAY=($LINEAR $EXPONENTIAL)
SKIP_ARRAY=(1 2 3 4)
NEGATIVE_BAG_COUNTS=(0 5 10 15 20)

for dataset in ${DATASET_ARRAY[*]}
do
  for algorithm in ${ALGORITHM_ARRAY[*]}
  do
    if [ $algorithm = "EMDD" ]
    then
      echo "EMMD ALG"
      for SEARCH in ${SEARCH_ARRAY[*]}
      do
        for METHOD in ${METHOD_ARRAY[*]}
        do
          for SKIPPING in ${SKIP_ARRAY[*]}
          do
            for NEGATIVEBAGCOUNT in ${NEGATIVE_BAG_COUNTS[*]}
            do
              echo NegativeBagEffectExperimentTwoRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT
              python NegativeBagEffectExperimentTwoRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT
            done
          done
        done

      done
    else
      for NEGATIVEBAGCOUNT in ${NEGATIVE_BAG_COUNTS[*]}
      do
        echo NegativeBagEffectExperimentTwoRooms.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT
        python NegativeBagEffectExperimentTwoRooms.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT
      done
    fi
  done

echo

done