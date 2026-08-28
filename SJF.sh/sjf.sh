#!/bin/bash

echo "Enter number of processes:"
read n

bt=()
for ((i=0; i<n; i++))
do
  echo "Enter burst time for P$((i+1)):"
  read bt[$i]
done

# Sort burst times (SJF)
 for ((i=0; i<n-1; i++))
 do
   for ((j=0; j<n-i-1; j++))
   do
     if [${bt[j]} -gt ${bt[$((j+1))]}]; then
        temp=${bt[j]}
        bt[$j] = ${bt[$((j+1))]}
        bt[$((j+1))] = $temp
     fi
   done
 done

wt[0]=0
tat[0]=${bt[0]}

for ((i=1; i<n; i++))
do
  wt[$i]=$((wt[i-1] + bt[i-1]))
  tat[$i]=$((wt[i] +bt[i]))
done

echo -e "\nProcess\tBurst\tWaiting\tTurnaround"
for ((i=0; i<n; i++))
do
  echo "P$((i+1)) ${bt[i]} ${wt[i]} ${tat[i]}"
done
