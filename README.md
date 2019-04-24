# Lottery

## Summary

This project is designed to pick numbers for EuroMillion.

It does so by,

1. Dump all the past draws from https://www.euro-millions.com and store them in a database.
1. Generate 5 numbers from a pool of 50 numbers, and another 2 numbers from a pool of 12 numbers.
1. Check if these number overlaps with any previous draws in the database. If not, they are good candidates to proceed
   (based on the fact that no duplicate draws in the past).
