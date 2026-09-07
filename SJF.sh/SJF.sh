#!/bin/bash

read -p "Enter number of processes: " n

for ((i=0; i<n; i++))
do
    p[$i]=$((i+1))
    read -p "Enter Arrival Time and Burst Time for Process P${p[$i]}: " arrival[$i] burst[$i]
    completed[$i]=0
done

current_time=0
completed_count=0

while (( completed_count < n ))
do
    idx=-1
    min_bt=999999

    # Ready queue-তে থাকা সর্বনিম্ন Burst Time-এর প্রসেস খোঁজা
    for ((i=0; i<n; i++))
    do
        if (( arrival[i] <= current_time && completed[i] == 0 ))
        then
            if (( burst[i] < min_bt ))
            then
                min_bt=${burst[i]}
                idx=$i
            elif (( burst[i] == min_bt ))
            then
                if (( arrival[i] < arrival[idx] ))
                then
                    idx=$i
                fi
            fi
        fi
    done

    # যদি কোনো প্রসেস Ready না থাকে (CPU Idle)
    if (( idx == -1 ))
    then
        current_time=$((current_time + 1))
    else
        current_time=$((current_time + burst[idx]))
        completion[$idx]=$current_time
        turnaround[$idx]=$((completion[idx] - arrival[idx]))
        waiting[$idx]=$((turnaround[idx] - burst[idx]))
        completed[$idx]=1
        completed_count=$((completed_count + 1))
    fi
done

echo ""
echo "--- SJF Scheduling Result ---"
echo "PID  AT  BT  CT  TAT  WT"
for ((i=0; i<n; i++))
do
    echo "P${p[i]}   ${arrival[i]}   ${burst[i]}   ${completion[i]}   ${turnaround[i]}    ${waiting[i]}"
done