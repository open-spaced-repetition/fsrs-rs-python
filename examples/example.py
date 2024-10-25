import fsrs_rs_python

# Pick to your liking (see above)
optimal_retention = 0.75
# Use default parameters/Weights for scheduler

fsrs = fsrs_rs_python.FSRS(parameters=fsrs_rs_python.DEFAULT_PARAMETERS)

# Create a completely new card
day1_states = fsrs.next_states(None, optimal_retention, 0)

# Rate as `hard` on first day
day1 = day1_states.hard
print(day1)  # scheduled as `in 4 days`

# Now we review the card 2 days later
day3_states = fsrs.next_states(day1.memory, optimal_retention, 2)

# Rate as `good` this time
day3 = day3_states.good
print(day3)
