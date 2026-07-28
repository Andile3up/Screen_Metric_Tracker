#!/bin/bash

#================================================================
for file in ~/3up_workspace/data/Impressions/raw/*; do
  # Commands to run on "$file"
  if [[ -f $file ]]; then
      echo "Processing raw: $file"
      to_date=$(date -d "2 hours ago" +%s)
      file_date=$(date -r $file +%s)
      echo $file_date
      echo $to_date
      if [ $to_date -ge $file_date ];
        then
            python collector.py $file
            if [ $? -eq 0 ]; then
              rm $file
            fi
      fi
  fi
done

for file in ~/3up_workspace/data/Impressions/processed/*; do
  # Commands to run on "$file"
  if [[ -f $file ]]; then
      echo "Processing: $file"
      python collector2.py $file
      if [ $? -eq 0 ]; then
        rm $file
      fi
  fi
done

for file in ~/3up_workspace/data/Impressions/upload/*; do
  # Commands to run on "$file"
  if [[ -f $file ]]; then
      echo "Processing: $file"
      python uploader.py $file Impressions
      if [ $? -eq 0 ]; then
        rm $file
      fi
  fi
done
#==============================================


for file in ~/3up_workspace/data/GPS/raw/*; do
  # Commands to run on "$file"
  if [[ -f $file ]]; then
      echo "Processing raw: $file"
      to_date=$(date -d "2 hours ago" +%s)
      file_date=$(date -r $file +%s)
      echo $file_date
      echo $to_date
      if [ $to_date -ge $file_date ];
        then
            python collect2_GPS.py $file
            if [ $? -eq 0 ]; then
              rm $file
            fi
      fi
  fi
done

for file in ~/3up_workspace/data/GPS/upload/*; do
  # Commands to run on "$file"
  if [[ -f $file ]]; then
      echo "Processing: $file"
      python uploader.py $file GPS $device_id
      if [ $? -eq 0 ]; then
        rm $file
      fi
  fi
done
