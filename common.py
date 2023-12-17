def test_assertions(tests, solve_function):
    for test_no, (test_data, solutions) in enumerate(tests.items()):
        for i in range(2):
            s = solutions[i]
            if s is not None:
                a = solve_function(test_data, i + 1)
                if not a == s:
                    raise ValueError(f"Failed Test #{test_no + 1}; Part #{i + 1}: Actual: {a}, Expected: {s}")
    print("All tests passed!")
