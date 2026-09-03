p=(1 2 3 )
arrival=(0 4 6)
burst=(5 3 2)
n=3
completion=()
waiting=()
turnaround=()

current_time=0
for ((i=0;i<n;i++))
do
for ((j=i+1; j<n; j++))
    do
        if (( arrival[i] > arrival[j] ))
        then
            temp=${arrival[i]}
            arrival[i]=${arrival[j]}
            arrival[j]=$temp

            temp=${burst[i]}
            burst[i]=${burst[j]}
            burst[j]=$temp

            temp=${i}
            i_temp=$i
        fi
   if (( current_time<arrival[i] ))
then
    current_time=${arrival[i]}
fi
  current_time=$((current_time+burst[i]))
  completion[$i]=$current_time

 turnaround[$i]=$((completion[i]-arrival[i]))
 waiting[$i]=$((turnaround[i]-burst[i]))
done
  done
echo " PID AT BT CT TAT WT"

for ((i=0;i<n;i++))
do
   echo " ${p[i]}  ${arrival[i]}   ${burst[i]}  ${completion[i]}  ${turnaround[i]}  ${waiting[i]}"
done
