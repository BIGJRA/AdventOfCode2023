#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

for i in {1..25}; do
    script_name="2023_$(printf "%02d" $i).py"
    script_path="./$script_name"

    if [ -f "$script_path" ]; then
        echo "Running $script_name..."
        start_time=$(date +%s)

        error_file=$(mktemp)
        python3 "$script_path" 2> "$error_file"

        end_time=$(date +%s)

        if [ -s "$error_file" ]; then
          echo -e "${RED}Error Output:"
          cat "$error_file"
          echo "${NC}"
        else
          if [ "$((end_time - start_time))" -gt 10 ]; then
            echo "${RED}Script $script_name took $((end_time - start_time)) seconds to run.${NC}"
          else
            echo "${GREEN}Script $script_name took $((end_time - start_time)) seconds to run.${NC}"
          fi
        fi

        echo "---------------------"
        rm "$error_file"
    else
        echo "${RED}Script $script_name not found.${NC}"
    fi
done