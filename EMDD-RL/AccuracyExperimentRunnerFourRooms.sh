STEP_LIMIT_EQUALLY_BALANCED=1
EQUALLY_BALANCED=3

LINEAR="LINEAR"
EXPONENTIAL="EXPONENTIAL"

H_ALL="H_ALL"
# H_NEIGHBOR="H_NEIGHBOR"
H_SET="H_SET"
H_CONCEPT_FILTER="H_CONCEPT_FILTER"

DATASET_ARRAY=($EQUALLY_BALANCED)
#("EMDD" "DD")
ALGORITHM_ARRAY=("EMDDCF")
SEARCH_ARRAY=($H_CONCEPT_FILTER) # ($H_SET $H_ALL)
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
                echo AccuracyExperimentFourRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
                python3 AccuracyExperimentFourRooms.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
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
          python3 AccuracyExperimentFourRooms.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
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
            echo AccuracyExperimentFourRoomsDDCF.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT kparameter=$K_PARAM
            python3 AccuracyExperimentFourRoomsDDCF.py data=$dataset algh=$algorithm search=0 method=0 skip=0 neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT kparameter=$K_PARAM
          done

        done
      done

    elif [ $algorithm = "EMDDCF" ]
    then
      echo "EMMDCF ALG"
      for SEARCH in ${SEARCH_ARRAY[*]}
      do
        for METHOD in ${METHOD_ARRAY[*]}
        do
          for K_PARAM in ${K_PARAMETER_SET[*]}
          do
            for NEGATIVEBAGCOUNT in ${NEGATIVE_BAG_COUNTS[*]}
            do
              for POSITIVEBAGCOUNT in ${POSITIVE_BAG_COUNTS[*]}
              do
                echo AccuracyExperimentFourRoomsEMDDCF.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD skip=$SKIPPING neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT
                python3 AccuracyExperimentFourRoomsEMDDCF.py data=$dataset algh=$algorithm search=$SEARCH method=$METHOD neg=$NEGATIVEBAGCOUNT pos=$POSITIVEBAGCOUNT kparameter=$K_PARAM
              done
            done
          done
        done

      done
    fi
  done
echo
done