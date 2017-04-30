for module in c499; do
    for model in 4d_table linear quadratic cubic; do
        python construct_power_model.py ../data/${module}_training/sequences ${model} ../models/${module}_power_model ${model}_power_model
        python power_model_prediction.py ../data/${module}_testing/sequences ../models/${module}_power_model/${model}_power_model ${model} ../models/${module}_power_model/${model}_error
    done
done
