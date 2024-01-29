# python 2.7
export PATH=/usr/bin:$PATH
STEP_LIMIT_EQUALLY_BALANCED=1
STEP_LIMIT_ONLY_POSITIVE=2
EQUALLY_BALANCED=3
ONLY_POSITIVE=4

LINEAR="LINEAR"
EXPONENTIAL="EXPONENTIAL"

H_ALL="H_ALL"
H_NEIGHBOR="H_NEIGHBOR"
H_SET="H_SET"

DATASET_ARRAY=($STEP_LIMIT_EQUALLY_BALANCED $STEP_LIMIT_ONLY_POSITIVE $ONLY_POSITIVE)
ALGORITHM_ARRAY=("EMDD")
SEARCH_ARRAY=($H_SET)
METHOD_ARRAY=($LINEAR $EXPONENTIAL)
SKIP_ARRAY=(1 2 3 4)


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
              echo EMDD-DDExperimentalTwoRooms4X.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING
              python EMDD-DDExperimentalTwoRooms4X.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING
          done
        done

      done
    else
      echo EMDD-DDExperimentalTwoRooms4X.py data=$dataset algh=$algorithm search=0 method=0 skip=0
      python EMDD-DDExperimentalTwoRooms4X.py data=$dataset algh=$algorithm search=0 method=0 skip=0
    fi

    # echo $dataset $algorithm
    # python EMDD-DDExperimentalTwoRooms.py DATA=$dataset ALG=$algorithm
  done

echo

done