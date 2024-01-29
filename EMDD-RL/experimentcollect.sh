export PATH=/usr/bin:$PATH
for i in {1..99}
do
  echo $i
  which python
  python3.9 DataCollector.py
done