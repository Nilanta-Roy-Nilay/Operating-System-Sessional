#!/bin/bash
echo " Enter num1: "
read num1
echo" Enter num2: "
read num2
if [ $num1 -ls $num2 ]; then

echo "$num1 is lower than $num2"
else
echo "$num2 is lower than $num1"
fi
