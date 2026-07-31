#i/bin/bash
echo "Enter your age"
read h
if [ $h -ge 18 ]; then
   echo "voter"
else
   echo "non voter"
fi
