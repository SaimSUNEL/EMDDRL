export PYTHONPATH=../

STEP_LIMIT_EQUALLY_BALANCED=1

EQUALLY_BALANCED=3

LINEAR="LINEAR"
EXPONENTIAL="EXPONENTIAL"

H_ALL="H_ALL"
# H_NEIGHBOR="H_NEIGHBOR"
H_SET="H_SET"
S1=$H_SET
S2=$H_ALL

DATASET_ARRAY=($EQUALLY_BALANCED)
#("EMDD" "DD")
algorithm="EMDD"
search=$S2
model=$EXPONENTIAL
k=4

python3 "EMDD-DDExperimentalTwoRooms5X(Online).py" algh=$algorithm search=$search method=$model skip=$k
