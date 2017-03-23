def get_nth_diff_at_point(point, coefficient, degree, n):
    if n == 0:
        return (point ** degree) * coefficient
    return get_nth_diff_at_point(point, coefficient * degree, degree - 1, n - 1)
