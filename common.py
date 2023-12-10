def test_assertions(tests, solve_function):
    for test_data, solutions in tests.items():
        sol1, sol2 = solutions
        if sol1 is not None:
            assert(solve_function(test_data, 1) == sol1)
        if sol2 is not None:
            assert(solve_function(test_data, 2) == sol2)
    print("All assertions passed!")
