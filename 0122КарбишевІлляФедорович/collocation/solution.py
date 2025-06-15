import numpy as np

def fr2_mcol(lamb, X, K_func, f_func):
    """
    Метод колокації для розв'язання інтегрального рівняння.
    lamb - скаляр, значення множника
    X - вузлові точки колокаційної сітки
    K_func - функція ядра K(x, t)
    f_func - функція правої частини f(x)
    """
    n_points = len(X)
    collocation_points = n_points - 1
    midpoints = 0.5 * (X[:-1] + X[1:])
    step = X[1] - X[0]

    A_matrix = np.zeros((collocation_points, collocation_points))
    b_vector = np.zeros(collocation_points)

    vectorized_f = np.vectorize(f_func)

    for i, x_i in enumerate(midpoints):
        b_vector[i] = vectorized_f(x_i)
        for j, x_j in enumerate(midpoints):
            kernel_value = K_func(x_i, x_j)
            A_matrix[i, j] = lamb * step * kernel_value
            if i == j:
                A_matrix[i, j] += 1


    solution_vector = np.linalg.solve(A_matrix, b_vector)

    return midpoints, solution_vector