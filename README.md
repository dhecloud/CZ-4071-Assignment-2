# CZ4071-Assignment-2

## Prerequisites

```
Python (3.6)
```

## Using your dataset

Our code works for any SNAP network from https://snap.stanford.edu/data/index.html
However, preprocessing is required to work with our code.
Save the SPAN txt in /

We have included reformat.py to change the format.

1. Change line 5 to the name of the SPAN dataset in reformat.py eg 
```
TXT_NAME = "ca-CondMat.txt"
```
2. run reformat.py
3. two txt files will be saved in graph/ - {TXT_NAME}_deg.txt and {TXT_NAME}_adj.txt

## Running BDOne and LinearTime

1. Change line 3 to the name of the span dataset in Graph.py eg
```
GRAPH_NAME = "ca-CondMat" (without the .txt)
```
2. Set verbose option (True/False) at line 4
3. python Graph.py

you can use any of the sample SPAN graphs we have provided - ca-CondMat, AstroPh, email, GrQc