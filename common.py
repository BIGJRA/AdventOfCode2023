def test_assertions(tests, solve_function, debug=False):
    for test_data, solutions in tests.items():
        sol1, sol2 = solutions
        if sol1 is not None:
            act1 = solve_function(test_data, 1)
            if not debug:
                assert (act1 == sol1)
            if debug:
                print(f"For Part 1: Actual: {act1}, Expected: {sol1}")
        if sol2 is not None:
            act2 = solve_function(test_data, 2)
            if not debug:
                assert (act2 == sol2)
            if debug:
                print(f"For Part 2: Actual: {act2}, Expected: {sol2}")
    print("All assertions passed!")
