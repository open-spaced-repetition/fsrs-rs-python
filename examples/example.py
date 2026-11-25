import fsrs_rs_python

# Pick to your liking (see above)
optimal_retention = 0.75
# Use default parameters/Weights for scheduler (34 values select FSRS-7)

fsrs = fsrs_rs_python.FSRS(parameters=fsrs_rs_python.DEFAULT_PARAMETERS)
print(fsrs.model_version)  # ModelVersion.FSRS7

# Create a completely new card
day1_states = fsrs.next_states(None, optimal_retention, 0)

# Rate as `hard` on first day
day1 = day1_states.hard
print(day1)  # `interval` is in days and may be fractional

# Now we review the card 2.5 days later (elapsed days may be fractional)
day3_states = fsrs.next_states(day1.memory, optimal_retention, 2.5)

# Rate as `good` this time
day3 = day3_states.good
print(day3)
