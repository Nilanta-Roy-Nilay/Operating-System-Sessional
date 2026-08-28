#!/bin/bash

fruits=("Apple" "Banana" "Mango")
fruits=("${fruits[@]:0:2}" "Grapes" "${fruits[@]:2}")
colors=()
colors[0]="Red"
colors[1]="Green"
colors[2]="Blue"

echo ${fruits[0]} #apple
echo ${fruits[1]} #apple
echo ${fruits[@]} #apple
echo ${#fruits[0]} #apple

fruits2=("Lemon""Orange")
fruits2+=("blackberry")
echo ${#fruits2[@]}

do 
  echo "I like $fruitttt"
done


