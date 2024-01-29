STEP_LIMIT_EQUALLY_BALANCED=1
EQUALLY_BALANCED=3

LINEAR="LINEAR"
EXPONENTIAL="EXPONENTIAL"

H_ALL="H_ALL"
# H_NEIGHBOR="H_NEIGHBOR"
H_SET="H_SET"

DATASET_ARRAY=($EQUALLY_BALANCED)
#("EMDD" "DD")
ALGORITHM_ARRAY=("DDCF")
SEARCH_ARRAY=($H_SET)
#($EXPONENTIAL)
METHOD_ARRAY=($EXPONENTIAL $LINEAR)
SKIP_ARRAY=(4)
# POSITIVE_BAG_COUNTS=(5 10 15 20)
# NEGATIVE_BAG_COUNTS=(0 5 10 15 20)
POSITIVE_BAG_COUNTS=(20)
NEGATIVE_BAG_COUNTS=(20)
K_PARAMETER_SET=(2 4 6 8 10 12)

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
              for POSITIVEBAGCOUNT in ${POSITIVE_BAG_COUNTS[*]}
              do


                echo AccuracyExperimentTwoRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
                python3 AccuracyExperimentTwoRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
              done
            done
          done
        done

      done
    elif [ $algorithm = "DD" ]
    then
      for NEGATIVEBAGCOUNT in ${NEGATIVE_BAG_COUNTS[*]}
      do
        for POSITIVEBAGCOUNT in ${POSITIVE_BAG_COUNTS[*]}
        do
          echo AccuracyExperimentTwoRooms.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
          /opt/python-3.7.10/bin/python3.7 AccuracyExperimentTwoRooms.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
        done
      done
    elif [ $algorithm = "DDCF" ]
    then
      echo "************DDCF************"
      for NEGATIVEBAGCOUNT in ${NEGATIVE_BAG_COUNTS[*]}
      do
        for POSITIVEBAGCOUNT in ${POSITIVE_BAG_COUNTS[*]}
        do
          for K_PARAM in ${K_PARAMETER_SET[*]}
          do
            echo AccuracyExperimentTwoRoomsDDCF.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT kparameter=$K_PARAM
            python3 AccuracyExperimentTwoRoomsDDCF.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT kparameter=$K_PARAM
          done

        done
      done
    fi
  done

echo

done