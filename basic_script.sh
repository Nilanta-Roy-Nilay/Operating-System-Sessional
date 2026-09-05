#!/bin/bash

name="NILAY"
echo "Hello,$name!" 

current_dir=$(pwd)
echo "You are in: $current_dir"

read -p "Enter your age: " age
echo "You are $age years old."

age=25
printf "name: %s\nage: %d\n""$name""$age"

fruits=("Apple" "Banana" "Orange")
colors=()
colors[0]="Red"
colors[1]="Green"
colors[2]="Blue"

echo ${fruits[0]}
echo ${fruits[1]}
echo ${fruits[@]}
echo ${#fruits[@]}

fruits=("Apple" "Banana")
fruits+=("Orange")
echo ${fruits[@]}

unset fruits[1]
echo ${fruits[@]}

for i in {1,5}
do
  echo "Number:$i"
done
