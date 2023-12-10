for i in {1..25}; do
    script_name="2023_$(printf "%02d" $i).py"
    script_path="./$script_name"

    if [ -f "$script_path" ]; then
        echo "Running $script_name..."
        start_time=$(date +%s)
        python3 "$script_path"
        end_time=$(date +%s)
        echo "Script $script_name took $((end_time - start_time)) seconds to run."
        echo "---------------------"
    else
        echo "Script $script_name not found."
    fi
done