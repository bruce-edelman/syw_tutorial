rule random_numbers:
    output:
        "src/data/random_numbers.dat"
    cache:
        True
    script:
        "src/scripts/random_numbers.py"
