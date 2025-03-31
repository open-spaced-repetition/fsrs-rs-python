from fsrs_rs_python import DEFAULT_PARAMETERS, default_simulator_config, simulate

if __name__ == "__main__":
    config = default_simulator_config()
    config.learn_span = 50
    config.learn_limit = 10

    simulation_result = simulate(DEFAULT_PARAMETERS, 0.9, config)

    print("Day,\tMemoriszed,\tReview Count,\tLearn Count,\tCost Per Day,\tCorrect Per Day")
    print(
        *(
            ",\t".join(f"{a:.2f}" for a in [i, *t])
            for i, t in enumerate(
                zip(
                    simulation_result.memorized_cnt_per_day,
                    simulation_result.review_cnt_per_day,
                    simulation_result.learn_cnt_per_day,
                    simulation_result.cost_per_day,
                    simulation_result.correct_cnt_per_day,
                )
            )
        ),
        sep="\n",
    )
