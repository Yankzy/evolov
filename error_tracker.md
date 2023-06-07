1. "An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block."
   - Occured in: SubCategoryMutation mutation class
   - THEORIES:
     - It's caused by "ATOMIC_MUTATIONS": True, in settings.
   - SOLUTION:
     - It's caused by "ATOMIC_MUTATIONS": True, in settings.
