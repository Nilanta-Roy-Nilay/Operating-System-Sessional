#!/bin/bash

echo "Welcome to random password generation"

echo "Please enter the length of the password:"

read PASS_LENGTH

if ! [[ $PASS_LENGTH =~ ^[0-9]+$ ]]; then
    echo "Error: Please enter a valid number."
    exit 1
fi
  password=()

for p in $(seq 1 3);
do  
   password+=("$(openssl rand -base64 48 | cut -c1-$PASS_LENGTH )")
done

echo "Here are the generated passwords:"
printf "%s\n" "${password[@]}"

echo "Do you want to save these passwords to a file? (y/n)"
read choice 
if [ "$choice" = "y" ]; then
    echo "Enter the passphrase for encryption:"
    read -s PASSPHRASE
   
    printf "%s\n" "${passwords[@]}" > passwords.txt

    ccrypt -d -K "$PASSPHRASE" passwords.txt

    echo "Passwords saved securely to passwords.txt.cpt"

elif ["$choice" = "n"]; then
    echo "Passwords not saved."
fi
