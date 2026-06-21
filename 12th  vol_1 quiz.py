import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import random
import time
import json
import os
import math
from PIL import Image, ImageTk

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
DATA_FILE = "student_data_vol1.json"

THEMES = {
    "Light": {
        "bg": "#f8f9fa", "surface": "#ffffff", "primary": "#1b4f72", 
        "primary_light": "#e8f0fe", "accent": "#2e86c1", "text": "#2c3e50", 
        "text_muted": "#7f8c8d", "success": "#27ae60", "danger": "#e74c3c"
    },
    "Dark": {
        "bg": "#121212", "surface": "#1e1e1e", "primary": "#0f2d42", 
        "primary_light": "#1b365d", "accent": "#3498db", "text": "#e0e0e0", 
        "text_muted": "#a0a0a0", "success": "#2ecc71", "danger": "#e74c3c"
    }
}

ALL_QUESTIONS = [
    # === EXERCISE 1.8: MATRICES AND DETERMINANTS ===
    {
        "exercise": "Exercise 1.8", "book_num": 1,
        "question": "If |adj(adj A)| = |A|^9, then the order of the square matrix A is",
        "options": ["3", "4", "2", "5"], "correct": "4"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 2,
        "question": "If A is a 3x3 non-singular matrix such that AA^T = A^TA and B = A^-1 A^T, then BB^T =",
        "options": ["A", "B", "I_3", "B^T"], "correct": "I_3"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 3,
        "question": "If A = [[3, 5], [1, 2]] and B = adj A and C = 3A, then |adj B| / |C| =",
        "options": ["1/3", "1/9", "1/4", "1"], "correct": "1/9"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 4,
        "question": "If A [[1, -2], [1, 4]] = [[6, 0], [0, 6]], then A =",
        "options": ["[[1, -2], [1, 4]]", "[[1, 2], [-1, 4]]", "[[4, 2], [-1, 1]]", "[[4, -1], [2, 1]]"], "correct": "[[4, 2], [-1, 1]]"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 5,
        "question": "If A = [[7, 3], [4, 2]], then 9I_2 - A =",
        "options": ["A^-1", "A^-1 / 2", "3A^-1", "2A^-1"], "correct": "2A^-1"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 6,
        "question": "If A = [[2, 0], [1, 5]] and B = [[1, 4], [2, 0]] then |adj(AB)| =",
        "options": ["-40", "-80", "-60", "-20"], "correct": "-40"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 7,
        "question": "If P = [[1, x, 0], [1, 3, 0], [2, 4, -2]] is the adjoint of 3x3 matrix A and |A| = 4 then x is",
        "options": ["15", "12", "14", "11"], "correct": "11"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 8,
        "question": "If A = [[3, 1, -1], [2, -2, 0], [1, 2, -1]] and A^-1 = [[a_11, a_12, a_13], [a_21, a_22, a_23], [a_31, a_32, a_33]] then the value of a_23 is",
        "options": ["0", "-2", "-3", "-1"], "correct": "-1"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 9,
        "question": "If A, B and C are invertible matrices of some order, then which one of the following is not true?",
        "options": ["adj A = |A|A^-1", "adj(AB) = (adj A)(adj B)", "det A^-1 = (det A)^-1", "(ABC)^-1 = C^-1 B^-1 A^-1"], "correct": "adj(AB) = (adj A)(adj B)"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 10,
        "question": "If (AB)^-1 = [[12, -17], [-19, 27]] and A^-1 = [[1, -1], [-2, 3]] then B^-1 =",
        "options": ["[[2, -5], [-3, 8]]", "[[8, 5], [3, 2]]", "[[3, 1], [2, 1]]", "[[8, -5], [-3, 2]]"], "correct": "[[2, -5], [-3, 8]]"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 11,
        "question": "If A^T A^-1 is symmetric, then A^2 =",
        "options": ["A^-1", "(A^T)^2", "A^T", "(A^-1)^2"], "correct": "(A^T)^2"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 12,
        "question": "If A is a non-singular matrix such that A^-1 = [[5, 3], [-2, -1]], then (A^T)^-1 =",
        "options": ["[[-5, 3], [2, 1]]", "[[-1, -3], [2, 5]]", "[[5, -2], [3, -1]]", "[[5, 3], [-2, -1]]"], "correct": "[[5, -2], [3, -1]]"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 13,
        "question": "If A = [[3/5, 4/5], [x, 3/5]] and A^T = A^-1 then the value of x is",
        "options": ["-4/5", "-3/5", "3/5", "4/5"], "correct": "-4/5"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 14,
        "question": "If A = [[1, tan(theta/2)], [-tan(theta/2), 1]] and AB = I_2, then B =",
        "options": ["(cos^2(theta/2))A", "(cos^2(theta/2))A^T", "(cos^2 theta)I", "(sin^2(theta/2))A"], "correct": "(cos^2(theta/2))A^T"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 15,
        "question": "If A = [[cos theta, sin theta], [-sin theta, cos theta]] and A(adj A) = [[k, 0], [0, k]], then k =",
        "options": ["0", "sin theta", "cos theta", "1"], "correct": "1"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 16,
        "question": "If A = [[2, 3], [5, -2]] be such that lambda A^-1 = A then lambda is",
        "options": ["17", "14", "19", "21"], "correct": "19"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 17,
        "question": "If adj A = [[2, 3], [4, -1]] and adj B = [[1, -2], [-3, 1]] then adj(AB) is",
        "options": ["[[-7, -1], [7, -9]]", "[[-6, 5], [-2, -10]]", "[[-7, 7], [-1, -9]]", "[[-6, -2], [5, -10]]"], "correct": "[[-6, 5], [-2, -10]]"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 18,
        "question": "The rank of the matrix [[1, 2, 3, 4], [2, 4, 6, 8], [-1, -2, -3, -4]] is",
        "options": ["1", "2", "4", "3"], "correct": "1"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 19,
        "question": "If ax + by = e^m, cx + dy = e^n, delta_1 = |[m, b], [n, d]|, delta_2 = |[a, m], [c, n]|, delta_3 = |[a, b], [c, d]|, then the values of x and y are respectively,",
        "options": ["e^(delta_2/delta_1), e^(delta_3/delta_1)", "log(delta_1/delta_3), log(delta_2/delta_3)", "log(delta_2/delta_1), log(delta_3/delta_1)", "e^(delta_1/delta_3), e^(delta_2/delta_3)"], "correct": "log(delta_1/delta_3), log(delta_2/delta_3)"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 20,
        "question": "Which of the following is/are correct?\n(i) Adjoint of a symmetric matrix is also symmetric.\n(ii) Adjoint of a diagonal matrix is also diagonal.\n(iii) If A is square matrix of order n and lambda is a scalar, adj(lambda A) = lambda^n adj(A).\n(iv) A(adj A) = (adj A)A = |A|I",
        "options": ["Only (i)", "(ii) and (iii)", "(iii) and (iv)", "(i), (ii) and (iv)"], "correct": "(i), (ii) and (iv)"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 21,
        "question": "If rho(A) = rho([A|B]), then the system AX = B of linear equations is",
        "options": ["consistent and has a unique solution", "consistent and has infinitely many solutions", "consistent", "inconsistent"], "correct": "consistent"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 22,
        "question": "If 0 <= theta <= pi and the system of equations x + (sin theta)y - (cos theta)z = 0, (cos theta)x - y + z = 0, (sin theta)x + y - z = 0 has a non-trivial solution then theta is",
        "options": ["2pi/3", "3pi/4", "5pi/6", "pi/4"], "correct": "pi/4"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 23,
        "question": "The augmented matrix of a system of linear equations is [[1, 2, 7, 3], [0, 1, 4, 6], [0, 0, lambda-7, mu+5]]. The system has infinitely many solutions if",
        "options": ["lambda = 7, mu != -5", "lambda = -7, mu = 5", "lambda != 7, mu != -5", "lambda = 7, mu = -5"], "correct": "lambda = 7, mu = -5"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 24,
        "question": "Let A = [[2, -1, 1], [-1, 2, -1], [1, -1, 2]] and 4B = [[3, 1, -1], [1, 3, x], [-1, 1, 3]]. If B is the inverse of A, then the value of x is",
        "options": ["2", "4", "3", "1"], "correct": "1"
    },
    {
        "exercise": "Exercise 1.8", "book_num": 25,
        "question": "If A = [[3, -3, 4], [2, -3, 4], [0, -1, 1]], then adj(adj A) is",
        "options": ["[[3, -3, 4], [2, -3, 4], [0, -1, 1]]", "[[6, -6, 8], [4, -6, 8], [0, -2, 2]]", "[[-3, 3, -4], [-2, 3, -4], [0, 1, -1]]", "[[3, -3, 4], [0, -1, 1], [2, -3, 4]]"], "correct": "[[3, -3, 4], [2, -3, 4], [0, -1, 1]]"
    },

    # === EXERCISE 2.9: COMPLEX NUMBERS ===
    {"exercise": "Exercise 2.9", "book_num": 1, "question": "i^n + i^(n+1) + i^(n+2) + i^(n+3) is", "options": ["0", "1", "-1", "i"], "correct": "0"},
    {"exercise": "Exercise 2.9", "book_num": 2, "question": "The value of sum_{n=1}^{13} (i^n + i^(n-1)) is", "options": ["1 + i", "i", "1", "0"], "correct": "1 + i"},
    {"exercise": "Exercise 2.9", "book_num": 3, "question": "The area of the triangle formed by the complex numbers z, iz, and z + iz in the Argand's diagram is", "options": ["1/2 |z|^2", "|z|^2", "3/2 |z|^2", "2|z|^2"], "correct": "1/2 |z|^2"},
    {"exercise": "Exercise 2.9", "book_num": 4, "question": "The conjugate of a complex number is 1/(i+2). Then, the complex number is", "options": ["1 / (i+2)", "-1 / (i+2)", "1 / (i-2)", "-1 / (i-2)"], "correct": "-1 / (i-2)"},
    {"exercise": "Exercise 2.9", "book_num": 5, "question": "If z = ((sqrt(3) + i)^3 * (3i + 4)^2) / (8 + 6i)^2, then |z| is equal to", "options": ["0", "1", "2", "3"], "correct": "2"},
    {"exercise": "Exercise 2.9", "book_num": 6, "question": "If z is a non-zero complex number such that 2i z^2 = bar(z), then |z| is", "options": ["1/2", "1", "2", "3"], "correct": "1/2"},
    {"exercise": "Exercise 2.9", "book_num": 7, "question": "If |z - 2 + i| <= 2, then the greatest value of |z| is", "options": ["sqrt(3) - 2", "sqrt(3) + 2", "sqrt(5) - 2", "sqrt(5) + 2"], "correct": "sqrt(5) + 2"},
    {"exercise": "Exercise 2.9", "book_num": 8, "question": "If |z - 3/z| = 2, then the least value of |z| is", "options": ["1", "2", "3", "5"], "correct": "1"},
    {"exercise": "Exercise 2.9", "book_num": 9, "question": "If |z| = 1 then the value of (1 + z) / (1 + bar(z)) is", "options": ["z", "bar(z)", "1/z", "1"], "correct": "z"},
    {"exercise": "Exercise 2.9", "book_num": 10, "question": "The solution of the equation |z| - z = 1 + 2i is", "options": ["3/2 - 2i", "-3/2 + 2i", "2 - 3/2 i", "2 + 3/2 i"], "correct": "3/2 - 2i"},
    {"exercise": "Exercise 2.9", "book_num": 11, "question": "If |z_1| = 1, |z_2| = 2, |z_3| = 3 and |9z_1 z_2 + 4z_1 z_3 + z_2 z_3| = 12 then the value of |z_1 + z_2 + z_3| is", "options": ["1", "2", "3", "4"], "correct": "2"},
    {"exercise": "Exercise 2.9", "book_num": 12, "question": "If z is a complex number such that z in C \\ R and z + 1/z in R, then |z| is", "options": ["0", "1", "2", "3"], "correct": "1"},
    {"exercise": "Exercise 2.9", "book_num": 13, "question": "z_1, z_2, and z_3 are complex numbers such that z_1 + z_2 + z_3 = 0 and |z_1| = |z_2| = |z_3| = 1 then z_1^2 + z_2^2 + z_3^2 is", "options": ["3", "2", "1", "0"], "correct": "0"},
    {"exercise": "Exercise 2.9", "book_num": 14, "question": "If (z - 1) / (z + 1) is purely imaginary, then |z| is", "options": ["1/2", "1", "2", "3"], "correct": "1"},
    {"exercise": "Exercise 2.9", "book_num": 15, "question": "If z = x + iy is a complex number such that |z + 2| = |z - 2|, then the locus of z is", "options": ["real axis", "imaginary axis", "ellipse", "circle"], "correct": "imaginary axis"},
    {"exercise": "Exercise 2.9", "book_num": 16, "question": "The principal argument of 3 / (-1 + i) is", "options": ["-5pi/6", "-2pi/3", "-3pi/4", "-pi/2"], "correct": "-3pi/4"},
    {"exercise": "Exercise 2.9", "book_num": 17, "question": "The principal argument of (sin 40° + i cos 40°)^5 is", "options": ["-110°", "-70°", "70°", "110°"], "correct": "-70°"},
    {"exercise": "Exercise 2.9", "book_num": 18, "question": "If (1 + i)(1 + 2i)(1 + 3i)...(1 + ni) = x + iy, then 2 * 5 * 10 * ... * (1 + n^2) is", "options": ["1", "i", "x^2 + y^2", "1 + n^2"], "correct": "x^2 + y^2"},
    {"exercise": "Exercise 2.9", "book_num": 19, "question": "If w != 1 is a cubic root of unity and (1 + w)^7 = A + Bw then (A, B) equals", "options": ["(1, 0)", "(-1, 1)", "(0, 1)", "(1, 1)"], "correct": "(1, 1)"},
    {"exercise": "Exercise 2.9", "book_num": 20, "question": "The principal argument of the complex number ((1 + i sqrt(3))^2) / (4i (1 - i sqrt(3))) is", "options": ["2pi/3", "pi/6", "5pi/6", "pi/2"], "correct": "pi/2"},
    {"exercise": "Exercise 2.9", "book_num": 21, "question": "If alpha and beta are the roots of x^2 + x + 1 = 0, then alpha^2020 + beta^2020 is", "options": ["-2", "-1", "1", "2"], "correct": "-1"},
    {"exercise": "Exercise 2.9", "book_num": 22, "question": "The product of all four values of (cos(pi/3) + i sin(pi/3))^(3/4) is", "options": ["-2", "-1", "1", "2"], "correct": "1"},
    {"exercise": "Exercise 2.9", "book_num": 23, "question": "If w != 1 is a cubic root of unity and |[1, 1, 1], [1, -w^2 - 1, w^2], [1, w^2, w^7]| = 3k, then k is equal to", "options": ["1", "-1", "sqrt(3)i", "-sqrt(3)i"], "correct": "-sqrt(3)i"},
    {"exercise": "Exercise 2.9", "book_num": 24, "question": "The value of ((1 + sqrt(3)i) / (1 - sqrt(3)i))^10 is", "options": ["cis(2pi/3)", "cis(4pi/3)", "-cis(2pi/3)", "-cis(4pi/3)"], "correct": "-cis(2pi/3)"},
    {"exercise": "Exercise 2.9", "book_num": 25, "question": "If w = cis(2pi/3), then the number of distinct roots of |[z+1, w, w^2], [w, z+w^2, 1], [w^2, 1, z+w]| = 0 is", "options": ["1", "2", "3", "4"], "correct": "1"},

    # === EXERCISE 3.7: THEORY OF EQUATIONS ===
    {"exercise": "Exercise 3.7", "book_num": 1, "question": "A zero of x^3 + 64 is", "options": ["0", "4", "4i", "-4"], "correct": "-4"},
    {"exercise": "Exercise 3.7", "book_num": 2, "question": "If f and g are polynomials of degrees m and n respectively, and if h(x) = (f o g)(x), then the degree of h is", "options": ["mn", "m + n", "m^n", "n"], "correct": "mn"},
    {"exercise": "Exercise 3.7", "book_num": 3, "question": "A polynomial equation in x of degree n always has", "options": ["n distinct roots", "n real roots", "n complex roots", "at most one root"], "correct": "n complex roots"},
    {"exercise": "Exercise 3.7", "book_num": 4, "question": "If alpha, beta, and gamma are the zeros of x^3 + px^2 + qx + r, then sum (1 / alpha) is", "options": ["-q/r", "-p/r", "q/r", "-q/p"], "correct": "-q/r"},
    {"exercise": "Exercise 3.7", "book_num": 5, "question": "According to the rational root theorem, which number is not a possible rational zero of 4x^7 + 2x^4 - 10x^3 - 5?", "options": ["-1", "5/4", "4/5", "5"], "correct": "4/5"},
    {"exercise": "Exercise 3.7", "book_num": 6, "question": "The polynomial x^3 - kx^2 + 9x has three real zeros if and only if k satisfies", "options": ["|k| <= 6", "k = 0", "|k| > 6", "|k| >= 6"], "correct": "|k| >= 6"},
    {"exercise": "Exercise 3.7", "book_num": 7, "question": "The number of real numbers in [0, 2pi] satisfying sin^4(x) - 2 sin^2(x) + 1 = 0 is", "options": ["2", "4", "1", "0"], "correct": "2"},
    {"exercise": "Exercise 3.7", "book_num": 8, "question": "The equation x^3 + 12x^2 + 10ax + 1999 = 0 definitely has a positive zero, if and only if", "options": ["a >= 0", "a > 0", "a < 0", "a <= 0"], "correct": "a < 0"},
    {"exercise": "Exercise 3.7", "book_num": 9, "question": "The polynomial x^3 + 2x + 3 has", "options": ["one negative and two imaginary zeros", "one positive and two imaginary zeros", "three real zeros", "no zeros"], "correct": "one negative and two imaginary zeros"},
    {"exercise": "Exercise 3.7", "book_num": 10, "question": "The number of positive zeros of the polynomial sum_{r=0}^{n} n_C_r (-1)^r x^r is", "options": ["0", "n", "< n", "r"], "correct": "n"},

    # === EXERCISE 4.6: INVERSE TRIGONOMETRIC FUNCTIONS ===
    {"exercise": "Exercise 4.6", "book_num": 1, "question": "The value of sin^-1(cos x), 0 <= x <= pi is", "options": ["pi - x", "x - pi/2", "pi/2 - x", "x - pi"], "correct": "pi/2 - x"},
    {"exercise": "Exercise 4.6", "book_num": 2, "question": "If sin^-1(x) + sin^-1(y) = 2pi/3; then cos^-1(x) + cos^-1(y) is equal to", "options": ["2pi/3", "pi/3", "pi/6", "pi"], "correct": "pi/3"},
    {"exercise": "Exercise 4.6", "book_num": 3, "question": "sin^-1(3/5) - cos^-1(12/13) + sec^-1(5/3) - cosec^-1(13/12) is equal to", "options": ["2pi", "pi", "0", "tan^-1(12/65)"], "correct": "0"},
    {"exercise": "Exercise 4.6", "book_num": 4, "question": "If sin^-1(x) = 2 sin^-1(alpha) has a solution, then", "options": ["|alpha| <= 1/sqrt(2)", "|alpha| >= 1/sqrt(2)", "|alpha| < 1/sqrt(2)", "|alpha| > 1/sqrt(2)"], "correct": "|alpha| <= 1/sqrt(2)"},
    {"exercise": "Exercise 4.6", "book_num": 5, "question": "sin^-1(cos x) = pi/2 - x is valid for", "options": ["-pi <= x <= 0", "0 <= x <= pi", "-pi/2 <= x <= pi/2", "-pi/4 <= x <= 3pi/4"], "correct": "0 <= x <= pi"},
    {"exercise": "Exercise 4.6", "book_num": 6, "question": "If sin^-1(x) + sin^-1(y) + sin^-1(z) = 3pi/2, the value of x^2017 + y^2018 + z^2019 - 9 / (x^101 + y^101 + z^101) is", "options": ["0", "1", "2", "3"], "correct": "0"},
    {"exercise": "Exercise 4.6", "book_num": 7, "question": "If cot^-1(x) = 2pi/5 for some x in R, the value of tan^-1(x) is", "options": ["-pi/10", "pi/5", "pi/10", "-pi/5"], "correct": "pi/10"},
    {"exercise": "Exercise 4.6", "book_num": 8, "question": "The domain of the function defined by f(x) = sin^-1(sqrt(x - 1)) is", "options": ["[1, 2]", "[-1, 1]", "[0, 1]", "[-1, 0]"], "correct": "[1, 2]"},
    {"exercise": "Exercise 4.6", "book_num": 9, "question": "If x = 1/5, the value of cos(cos^-1(x) + 2 sin^-1(x)) is", "options": ["-sqrt(24/25)", "sqrt(24/25)", "1/5", "-1/5"], "correct": "-1/5"},
    {"exercise": "Exercise 4.6", "book_num": 10, "question": "tan^-1(1/4) + tan^-1(2/9) is equal to", "options": ["1/2 cos^-1(3/5)", "1/2 sin^-1(3/5)", "1/2 tan^-1(3/5)", "tan^-1(1/2)"], "correct": "tan^-1(1/2)"},
    {"exercise": "Exercise 4.6", "book_num": 11, "question": "If the function f(x) = sin^-1(x^2 - 3), then x belongs to", "options": ["[-1, 1]", "[sqrt(2), 2]", "[-2, -sqrt(2)] U [sqrt(2), 2]", "[-2, -sqrt(2)]"], "correct": "[-2, -sqrt(2)] U [sqrt(2), 2]"},
    {"exercise": "Exercise 4.6", "book_num": 12, "question": "If cot^-1(2) and cot^-1(3) are two angles of a triangle, then the third angle is", "options": ["pi/4", "3pi/4", "pi/6", "pi/3"], "correct": "3pi/4"},
    {"exercise": "Exercise 4.6", "book_num": 13, "question": "sin^-1(tan(pi/4)) - sin^-1(sqrt(3/x)) = pi/6. Then x is a root of the equation", "options": ["x^2 - x - 6 = 0", "x^2 - x - 12 = 0", "x^2 + x - 12 = 0", "x^2 + x - 6 = 0"], "correct": "x^2 - x - 12 = 0"},
    {"exercise": "Exercise 4.6", "book_num": 14, "question": "sin^-1(2 cos^2(x) - 1) + cos^-1(1 - 2 sin^2(x)) =", "options": ["pi/2", "pi/3", "pi/4", "pi/6"], "correct": "pi/2"},
    {"exercise": "Exercise 4.6", "book_num": 15, "question": "If cot^-1(sqrt(sin alpha)) + tan^-1(sqrt(sin alpha)) = u, then cos 2u is equal to", "options": ["tan^2(alpha)", "0", "-1", "tan 2alpha"], "correct": "-1"},
    {"exercise": "Exercise 4.6", "book_num": 16, "question": "If |x| <= 1, then 2 tan^-1(x) - sin^-1(2x / (1 + x^2)) is equal to", "options": ["tan^-1(x)", "sin^-1(x)", "0", "pi"], "correct": "0"},
    {"exercise": "Exercise 4.6", "book_num": 17, "question": "The equation tan^-1(x) - cot^-1(x) = tan^-1(1/sqrt(3)) has", "options": ["no solution", "unique solution", "two solutions", "infinite number of solutions"], "correct": "unique solution"},
    {"exercise": "Exercise 4.6", "book_num": 18, "question": "If sin^-1(x) + cot^-1(1/2) = pi/2, then x is equal to", "options": ["1/2", "1/sqrt(5)", "2/sqrt(5)", "sqrt(3)/2"], "correct": "1/sqrt(5)"},
    {"exercise": "Exercise 4.6", "book_num": 19, "question": "If sin^-1(x/5) + cosec^-1(5/4) = pi/2, then the value of x is", "options": ["4", "5", "2", "3"], "correct": "3"},
    {"exercise": "Exercise 4.6", "book_num": 20, "question": "sin(tan^-1(x)), |x| < 1 is equal to", "options": ["x / sqrt(1 - x^2)", "1 / sqrt(1 - x^2)", "1 / sqrt(1 + x^2)", "x / sqrt(1 + x^2)"], "correct": "x / sqrt(1 + x^2)"},

    # === EXERCISE 5.6: TWO DIMENSIONAL ANALYTICAL GEOMETRY II ===
    {"exercise": "Exercise 5.6", "book_num": 1, "question": "The equation of the circle passing through (1,5) and (4,1) and touching y-axis is x^2 + y^2 - 5x - 6y + 9 + lambda(4x + 3y - 19) = 0 where lambda is equal to", "options": ["0, -40/9", "0", "40/9", "-40/9"], "correct": "0, -40/9"},
    {"exercise": "Exercise 5.6", "book_num": 2, "question": "The eccentricity of the hyperbola whose latus rectum is 8 and conjugate axis is equal to half the distance between the foci is", "options": ["4/3", "4/sqrt(3)", "2/sqrt(3)", "3/2"], "correct": "2/sqrt(3)"},
    {"exercise": "Exercise 5.6", "book_num": 3, "question": "The circle x^2 + y^2 = 4x + 8y + 5 intersects the line 3x - 4y = m at two distinct points if", "options": ["15 < m < 65", "35 < m < 85", "-85 < m < -35", "-35 < m < 15"], "correct": "-35 < m < 15"},
    {"exercise": "Exercise 5.6", "book_num": 4, "question": "The length of the diameter of the circle which touches the x-axis at the point (1,0) and passes through the point (2,3) is", "options": ["6/5", "5/3", "10/3", "3/5"], "correct": "10/3"},
    {"exercise": "Exercise 5.6", "book_num": 5, "question": "The radius of the circle 3x^2 + by^2 + 4bx - 6by + b^2 = 0 is", "options": ["1", "3", "sqrt(10)", "sqrt(11)"], "correct": "sqrt(11)"},
    {"exercise": "Exercise 5.6", "book_num": 6, "question": "The centre of the circle inscribed in a square formed by the lines x^2 - 8x - 12 = 0 and y^2 - 14y + 45 = 0 is", "options": ["(4,7)", "(7,4)", "(9,4)", "(4,9)"], "correct": "(4,7)"},
    {"exercise": "Exercise 5.6", "book_num": 7, "question": "The equation of the normal to the circle x^2 + y^2 - 2x - 2y + 1 = 0 which is parallel to the line 2x + 4y = 3 is", "options": ["x + 2y = 3", "x + 2y + 3 = 0", "2x + 4y + 3 = 0", "x - 2y + 3 = 0"], "correct": "x + 2y = 3"},
    {"exercise": "Exercise 5.6", "book_num": 8, "question": "If P(x,y) be any point on 16x^2 + 25y^2 = 400 with foci F_1(3,0) and F_2(-3,0) then PF_1 + PF_2 is", "options": ["8", "6", "10", "12"], "correct": "10"},
    {"exercise": "Exercise 5.6", "book_num": 9, "question": "The radius of the circle passing through the point (6, 2) two of whose diameters are x + y = 6 and x + 2y = 4 is", "options": ["10", "2 sqrt(5)", "6", "4"], "correct": "2 sqrt(5)"},
    {"exercise": "Exercise 5.6", "book_num": 10, "question": "The area of quadrilateral formed with foci of the hyperbolas x^2/a^2 - y^2/b^2 = 1 and x^2/a^2 - y^2/b^2 = -1 is", "options": ["4(a^2 + b^2)", "2(a^2 + b^2)", "a^2 + b^2", "1/2(a^2 + b^2)"], "correct": "2(a^2 + b^2)"},
    {"exercise": "Exercise 5.6", "book_num": 11, "question": "If the normals of the parabola y^2 = 4x drawn at the end points of its latus rectum are tangents to the circle (x - 3)^2 + (y + 2)^2 = r^2, then the value of r^2 is", "options": ["2", "3", "1", "4"], "correct": "2"},
    {"exercise": "Exercise 5.6", "book_num": 12, "question": "If x + y = k is a normal to the parabola y^2 = 12x, then the value of k is", "options": ["3", "-1", "1", "9"], "correct": "9"},
    {"exercise": "Exercise 5.6", "book_num": 13, "question": "The ellipse E_1: x^2/9 + y^2/4 = 1 is inscribed in a rectangle R whose sides are parallel to the coordinate axes. Another ellipse E_2 passing through the point (0,4) circumscribes the rectangle R. The eccentricity of the ellipse is", "options": ["sqrt(2)/2", "sqrt(3)/2", "1/2", "3/4"], "correct": "1/2"},
    {"exercise": "Exercise 5.6", "book_num": 14, "question": "Tangents are drawn to the hyperbola x^2/9 - y^2/4 = 1 parallel to the straight line 2x - y = 1. One of the points of contact of tangents on the hyperbola is", "options": ["(9/(2 sqrt(2)), -1/sqrt(2))", "(-9/(2 sqrt(2)), 1/sqrt(2))", "(9/(2 sqrt(2)), 1/sqrt(2))", "(3 sqrt(3), -2 sqrt(2))"], "correct": "(9/(2 sqrt(2)), 1/sqrt(2))"},
    {"exercise": "Exercise 5.6", "book_num": 15, "question": "The equation of the circle passing through the foci of the ellipse x^2/16 + y^2/9 = 1 having centre at (0,3) is", "options": ["x^2 + y^2 - 6y - 7 = 0", "x^2 + y^2 - 6y + 7 = 0", "x^2 + y^2 - 6y - 5 = 0", "x^2 + y^2 - 6y + 5 = 0"], "correct": "x^2 + y^2 - 6y - 7 = 0"},
    {"exercise": "Exercise 5.6", "book_num": 16, "question": "Let C be the circle with centre at (1,1) and radius = 1. If T is the circle centered at (0, y) passing through the origin and touching the circle C externally, then the radius of T is equal to", "options": ["sqrt(3)/sqrt(2)", "sqrt(3)/2", "1/2", "1/4"], "correct": "1/4"},
    {"exercise": "Exercise 5.6", "book_num": 17, "question": "Consider an ellipse whose centre is at the origin and its major axis is along x-axis. If its eccentricity is 3/5 and the distance between its foci is 6, then the area of the quadrilateral inscribed in the ellipse with diagonals as major and minor axis of the ellipse is", "options": ["8", "32", "80", "40"], "correct": "40"},
    {"exercise": "Exercise 5.6", "book_num": 18, "question": "Area of the greatest rectangle inscribed in the ellipse x^2/a^2 + y^2/b^2 = 1 is", "options": ["2ab", "ab", "sqrt(ab)", "a/b"], "correct": "2ab"},
    {"exercise": "Exercise 5.6", "book_num": 19, "question": "An ellipse has OB as semi minor axis, F and F' its foci and the angle FBF' is a right angle. Then the eccentricity of the ellipse is", "options": ["1/sqrt(2)", "1/2", "1/4", "1/sqrt(3)"], "correct": "1/sqrt(2)"},
    {"exercise": "Exercise 5.6", "book_num": 20, "question": "The eccentricity of the ellipse (x-3)^2 + (y-4)^2 = y^2/9 is", "options": ["sqrt(3)/2", "1/3", "1/(3 sqrt(2))", "1/sqrt(3)"], "correct": "1/3"},
    {"exercise": "Exercise 5.6", "book_num": 21, "question": "If the two tangents drawn from a point P to the parabola y^2 = 4x are at right angles then the locus of P is", "options": ["2x + 1 = 0", "x = -1", "2x - 1 = 0", "x = 1"], "correct": "x = -1"},
    {"exercise": "Exercise 5.6", "book_num": 22, "question": "The circle passing through (1,-2) and touching the axis of x at (3,0) passes through the point", "options": ["(-5,2)", "(2,-5)", "(5,-2)", "(-2,5)"], "correct": "(5,-2)"},
    {"exercise": "Exercise 5.6", "book_num": 23, "question": "The locus of a point whose distance from (-2,0) is 2/3 times its distance from the line x = -9/2 is", "options": ["a parabola", "a hyperbola", "an ellipse", "a circle"], "correct": "an ellipse"},
    {"exercise": "Exercise 5.6", "book_num": 24, "question": "The values of m for which the line y = mx + 2 sqrt(5) touches the hyperbola 16x^2 - 9y^2 = 144 are the roots of x^2 - (a+b)x - 4 = 0, then the value of (a+b) is", "options": ["2", "4", "0", "-2"], "correct": "0"},
    {"exercise": "Exercise 5.6", "book_num": 25, "question": "If the coordinates at one end of a diameter of the circle x^2 + y^2 - 8x - 4y + c = 0 are (11,2), the coordinates of the other end are", "options": ["(-5,2)", "(2,-5)", "(5,-2)", "(-2,5)"], "correct": "-5,2"},

    # === EXERCISE 6.10: VECTOR ALGEBRA ===
    {"exercise": "Exercise 6.10", "book_num": 1, "question": "If a_vec and b_vec are parallel vectors, then [a_vec, c_vec, b_vec] is equal to", "options": ["2", "-1", "1", "0"], "correct": "0"},
    {"exercise": "Exercise 6.10", "book_num": 2, "question": "If a vector alpha_vec lies in the plane of beta_vec and gamma_vec, then", "options": ["[alpha_vec, beta_vec, gamma_vec] = 1", "[alpha_vec, beta_vec, gamma_vec] = -1", "[alpha_vec, beta_vec, gamma_vec] = 0", "[alpha_vec, beta_vec, gamma_vec] = 2"], "correct": "[alpha_vec, beta_vec, gamma_vec] = 0"},
    {"exercise": "Exercise 6.10", "book_num": 3, "question": "If a_vec . b_vec = b_vec . c_vec = b_vec . a_vec = 0, then the value of [a_vec, b_vec, c_vec] is", "options": ["|a_vec||b_vec||c_vec|", "1/3 |a_vec||b_vec||c_vec|", "1", "-1"], "correct": "|a_vec||b_vec||c_vec|"},
    {"exercise": "Exercise 6.10", "book_num": 4, "question": "If a_vec, b_vec, c_vec are three unit vectors such that a_vec is perpendicular to b_vec, and is parallel to c_vec, then a_vec x (b_vec x c_vec) is equal to", "options": ["a_vec", "b_vec", "c_vec", "0_vec"], "correct": "b_vec"},
    {"exercise": "Exercise 6.10", "book_num": 5, "question": "If [a_vec, b_vec, c_vec] = 1, then the value of (a_vec.(b_vec x c_vec))/((c_vec x a_vec).b_vec) + (b_vec.(c_vec x a_vec))/((a_vec x b_vec).c_vec) + (c_vec.(a_vec x b_vec))/((c_vec x b_vec).a_vec) is", "options": ["1", "-1", "2", "3"], "correct": "1"},
    {"exercise": "Exercise 6.10", "book_num": 6, "question": "The volume of the parallelepiped with its edges represented by the vectors i_hat+j_hat, i_hat+2j_hat, i_hat+j_hat+pi*k_hat is", "options": ["pi/2", "pi/3", "pi", "pi/4"], "correct": "pi"},
    {"exercise": "Exercise 6.10", "book_num": 7, "question": "If a_vec and b_vec are unit vectors such that [a_vec, b_vec, a_vec x b_vec] = 1/4, then the angle between a_vec and b_vec is", "options": ["pi/3", "pi/4", "pi/2", "pi/6"], "correct": "pi/6"},
    {"exercise": "Exercise 6.10", "book_num": 8, "question": "If a_vec = i_hat+j_hat+k_hat, b_vec = i_hat+j_hat, c_vec = i_hat and (a_vec x b_vec) x c_vec = lambda*a_vec + mu*b_vec, then the value of lambda + mu is", "options": ["0", "1", "6", "3"], "correct": "0"},
    {"exercise": "Exercise 6.10", "book_num": 9, "question": "If a_vec, b_vec, c_vec are non-coplanar, non-zero vectors such that [a_vec, b_vec, c_vec] = 3, then {[a_vec x b_vec, b_vec x c_vec, c_vec x a_vec]}^2 is equal to", "options": ["81", "9", "27", "18"], "correct": "81"},
    {"exercise": "Exercise 6.10", "book_num": 10, "question": "If a_vec, b_vec, c_vec are three non-coplanar unit vectors such that a_vec x (b_vec x c_vec) = (b_vec + c_vec)/sqrt(2), then the angle between a_vec and b_vec is", "options": ["pi/2", "3pi/4", "pi/4", "pi"], "correct": "3pi/4"},
    {"exercise": "Exercise 6.10", "book_num": 11, "question": "If the volume of the parallelepiped with a_vec x b_vec, b_vec x c_vec, c_vec x a_vec as coterminous edges is 8 cubic units, then the volume of the parallelepiped with (a_vec x b_vec) x (b_vec x c_vec), (b_vec x c_vec) x (c_vec x a_vec) and (c_vec x a_vec) x (a_vec x b_vec) as coterminous edges is,", "options": ["8 cubic units", "512 cubic units", "64 cubic units", "24 cubic units"], "correct": "64 cubic units"},
    {"exercise": "Exercise 6.10", "book_num": 12, "question": "Consider the vectors a_vec, b_vec, c_vec, d_vec such that (a_vec x b_vec) x (c_vec x d_vec) = 0_vec. Let P_1 and P_2 be the planes determined by the pairs of vectors a_vec, b_vec and c_vec, d_vec respectively. Then the angle between P_1 and P_2 is", "options": ["0°", "45°", "60°", "90°"], "correct": "0°"},
    {"exercise": "Exercise 6.10", "book_num": 13, "question": "If a_vec x (b_vec x c_vec) = (a_vec x b_vec) x c_vec, where a_vec, b_vec, c_vec are any three vectors such that b_vec . c_vec != 0 and a_vec . b_vec != 0, then a_vec and c_vec are", "options": ["perpendicular", "parallel", "inclined at an angle pi/3", "inclined at an angle pi/6"], "correct": "parallel"},
    {"exercise": "Exercise 6.10", "book_num": 14, "question": "If a_vec = 2i_hat+3j_hat-k_hat, b_vec = i_hat+2j_hat-5k_hat, c_vec = 3i_hat+5j_hat-k_hat, then a vector perpendicular to a_vec and lies in the plane containing b_vec and c_vec is", "options": ["-17i_hat+21j_hat-97k_hat", "17i_hat+21j_hat-123k_hat", "-17i_hat-21j_hat+97k_hat", "-17i_hat-21j_hat-97k_hat"], "correct": "-17i_hat+21j_hat-97k_hat"},
    {"exercise": "Exercise 6.10", "book_num": 15, "question": "The angle between the lines (x-2)/3 = (y+1)/-2, z = 2 and (x-1)/1 = (2y+3)/3 = (z+5)/2 is", "options": ["pi/6", "pi/4", "pi/3", "pi/2"], "correct": "pi/2"},
    {"exercise": "Exercise 6.10", "book_num": 16, "question": "If the line (x-2)/3 = (y-1)/-5 = (z+2)/2 lies in the plane x + 3y - alpha*z + beta = 0, then (alpha, beta) is", "options": ["(-5,5)", "(-6,7)", "(5,-5)", "(6,-7)"], "correct": "(6,-7)"},
    {"exercise": "Exercise 6.10", "book_num": 17, "question": "The angle between the line r_vec = (i_hat+2j_hat-3k_hat) + t(2i_hat+j_hat-2k_hat) and the plane r_vec . (i_hat+j_hat) + 4 = 0 is", "options": ["0°", "30°", "45°", "90°"], "correct": "45°"},
    {"exercise": "Exercise 6.10", "book_num": 18, "question": "The coordinates of the point where the line r_vec = (6i_hat-j_hat-3k_hat) + t(-i_hat+4k_hat) meets the plane r_vec . (i_hat+j_hat-k_hat) = 3 are", "options": ["(2,1,0)", "(7,-1,-7)", "(1,2,-6)", "(5,-1,1)"], "correct": "(5,-1,1)"},
    {"exercise": "Exercise 6.10", "book_num": 19, "question": "Distance from the origin to the plane 3x - 6y + 2z + 7 = 0 is", "options": ["0", "1", "2", "3"], "correct": "1"},
    {"exercise": "Exercise 6.10", "book_num": 20, "question": "The distance between the planes x + 2y + 3z + 7 = 0 and 2x + 4y + 6z + 7 = 0 is", "options": ["sqrt(7)/(2 sqrt(2))", "7/2", "sqrt(7)/2", "7/(2 sqrt(2))"], "correct": "7/(2 sqrt(2))"},
    {"exercise": "Exercise 6.10", "book_num": 21, "question": "If the direction cosines of a line are 1/c, 1/c, 1/c then", "options": ["c = +-3", "c = +-sqrt(3)", "c > 0", "0 < c < 1"], "correct": "c = +-sqrt(3)"},
    {"exercise": "Exercise 6.10", "book_num": 22, "question": "The vector equation r_vec = (i_hat-2j_hat-k_hat) + t(6j_hat-k_hat) represents a straight line passing through the points", "options": ["(0,6,-1) and (1,-2,-1)", "(0,6,-1) and (-1,-4,-2)", "(1,-2,-1) and (1,4,-2)", "(1,-2,-1) and (0,-6,1)"], "correct": "(1,-2,-1) and (1,4,-2)"},
    {"exercise": "Exercise 6.10", "book_num": 23, "question": "If the distance of the point (1,1,1) from the origin is half of its distance from the plane x + y + z + k = 0, then the values of k are", "options": ["+-3", "+-6", "-3,9", "3,-9"], "correct": "3,-9"},
    {"exercise": "Exercise 6.10", "book_num": 24, "question": "If the planes r_vec . (2i_hat - lambda*j_hat + k_hat) = 3 and r_vec . (4i_hat + j_hat - mu*k_hat) = 5 are parallel, then the values of lambda and mu are", "options": ["1/2, -2", "-1/2, 2", "-1/2, -2", "1/2, 2"], "correct": "-1/2, -2"},
    {"exercise": "Exercise 6.10", "book_num": 25, "question": "If the length of the perpendicular from the origin to the plane 2x + 3y + lambda*z = 1, lambda > 0 is 1/5, then the value of lambda is", "options": ["2 sqrt(3)", "3 sqrt(2)", "0", "1"], "correct": "2 sqrt(3)"}
]

# ==========================================
# DATABASE & DATA MANAGEMENT LAYER
# ==========================================
class DatabaseManager:
    @staticmethod
    def load_data():
        if not os.path.exists(DATA_FILE):
            default_data = {
                "users": {"admin": "infinity123"},
                "history": {},
                "bookmarks": {}
            }
            DatabaseManager.save_data(default_data)
            return default_data
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {"users": {"admin": "infinity123"}, "history": {}, "bookmarks": {}}

    @staticmethod
    def save_data(data):
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error writing persistence model: {e}")

# ==========================================
# CUSTOM DRAWING COMPONENT
# ==========================================
class ModernChart(tk.Canvas):
    def __init__(self, parent, width=320, height=180, bg_color="#ffffff", **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg_color, highlightthickness=0, **kwargs)
        self.width = width
        self.height = height

    def draw_pie(self, correct, wrong, skipped, colors):
        self.delete("all")
        total = correct + wrong + skipped
        if total == 0:
            self.create_text(self.width/2, self.height/2, text="No Logs Available", font=("Arial", 10))
            return
            
        angles = [
            (correct / total) * 360,
            (wrong / total) * 360,
            (skipped / total) * 360
        ]
        
        cur_angle = 0
        palette = [colors["success"], colors["danger"], colors["text_muted"]]
        labels = ["Correct", "Wrong", "Skipped"]
        vals = [correct, wrong, skipped]
        
        cx, cy, r = self.width * 0.3, self.height / 2, min(self.width, self.height) * 0.4
        
        for angle, color in zip(angles, palette):
            if angle > 0:
                self.create_arc(cx-r, cy-r, cx+r, cy+r, start=cur_angle, extent=angle, fill=color, outline="")
                cur_angle += angle

        lx, ly = self.width * 0.65, self.height * 0.25
        for i, (label, val, col) in enumerate(zip(labels, vals, palette)):
            if val >= 0:
                self.create_rectangle(lx, ly, lx+12, ly+12, fill=col, outline="")
                self.create_text(lx+20, ly+6, text=f"{label}: {val}", anchor="w", font=("Arial", 9, "bold"), fill=colors["text"])
                ly += 25

# ==========================================
# MAIN APPLICATION ENGINE
# ==========================================
class QuizApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Tuitions - Adaptive Evaluation Engine (Vol 1)")
        self.root.geometry("1024x740")
        self.root.minsize(960, 680)
        
        # Core State Configuration
        self.db = DatabaseManager.load_data()
        self.current_user = None
        self.current_theme = "Light"
        self.active_session = None 
        
        # Runtime Test Registers
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.user_answers = {} 
        self.bookmarks = []
        self.is_exam_mode = False
        
        # Timer Management variables
        self.time_remaining = 0
        self.timer_running = False
        self.start_time_stamp = 0
        
        self.cached_logo = None
        self.preload_logo_image()
        
        # Initialize Base CSS Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.apply_theme_rules()
        self.show_login_screen()

    def preload_logo_image(self):
        try:
            if os.path.exists("infinity_logo.png"):
                raw_img = Image.open("infinity_logo.png")
                w_percent = (180 / float(raw_img.size[0]))
                h_size = int((float(raw_img.size[1]) * float(w_percent)))
                resized_img = raw_img.resize((180, h_size), Image.Resampling.LANCZOS)
                self.cached_logo = ImageTk.PhotoImage(resized_img)
        except Exception as e:
            print(f"Branding image failed to initialize: {e}")

    def apply_theme_rules(self):
        colors = THEMES[self.current_theme]
        self.root.configure(bg=colors["bg"])
        
        self.style.configure("TProgressbar", thickness=12, troughcolor=colors["bg"], background=colors["accent"])
        self.style.configure("Treeview", background=colors["surface"], foreground=colors["text"], fieldbackground=colors["surface"])
        self.style.map("Treeview", background=[('selected', colors["accent"])])

    def switch_theme(self):
        self.current_theme = "Dark" if self.current_theme == "Light" else "Light"
        self.apply_theme_rules()
        if self.current_user:
            if hasattr(self, "lbl_question"):
                self.setup_quiz_interface()
                self.load_question()
            else:
                self.show_home_dashboard()
        else:
            self.show_login_screen()

    def create_branded_header(self, parent_window, title_text, show_nav=True):
        colors = THEMES[self.current_theme]
        header_frame = tk.Frame(parent_window, bg=colors["primary"], pady=10, padx=20)
        header_frame.pack(fill=tk.X)
        
        left_container = tk.Frame(header_frame, bg=colors["primary"])
        left_container.pack(side=tk.LEFT)
        
        if self.cached_logo:
            lbl_logo = tk.Label(left_container, image=self.cached_logo, bg=colors["primary"])
            lbl_logo.pack(side=tk.LEFT, padx=(0, 15))
            
        lbl_title = tk.Label(left_container, text=title_text, font=("Arial", 16, "bold"), fg="white", bg=colors["primary"])
        lbl_title.pack(side=tk.LEFT)
        
        right_container = tk.Frame(header_frame, bg=colors["primary"])
        right_container.pack(side=tk.RIGHT)
        
        theme_btn = tk.Button(right_container, text=f"Theme: {self.current_theme}", font=("Arial", 9, "bold"), 
                              bg=colors["accent"], fg="white", bd=0, padx=10, pady=5, cursor="hand2", command=self.switch_theme)
        theme_btn.pack(side=tk.RIGHT, padx=5)
        
        if show_nav and self.current_user:
            home_btn = tk.Button(right_container, text="Dashboard Home", font=("Arial", 9, "bold"), 
                                 bg=colors["success"], fg="white", bd=0, padx=10, pady=5, cursor="hand2", command=self.confirm_exit_to_dashboard)
            home_btn.pack(side=tk.RIGHT, padx=5)

    def confirm_exit_to_dashboard(self):
        if hasattr(self, "timer_running") and self.timer_running:
            if not messagebox.askyesno("Exit Verification", "An active session running. Abandon context and go home?"):
                return
        self.timer_running = False
        self.show_home_dashboard()

    # ==========================================
    # SCREEN 1: LOGIN SYSTEM
    # ==========================================
    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        colors = THEMES[self.current_theme]
        self.create_branded_header(self.root, "Secure Entry Portal", show_nav=False)
        
        center_frame = tk.Frame(self.root, bg=colors["surface"], bd=1, relief=tk.GROOVE)
        center_frame.place(relx=0.5, rely=0.55, anchor=tk.CENTER, width=420, height=360)
        
        tk.Label(center_frame, text="Infinity Evaluation Gateway", font=("Arial", 14, "bold"), fg=colors["text"], bg=colors["surface"]).pack(pady=20)
        
        f_frame = tk.Frame(center_frame, bg=colors["surface"])
        f_frame.pack(fill=tk.X, padx=40)
        
        tk.Label(f_frame, text="Student Registration Key / Identifier ID:", font=("Arial", 10, "bold"), fg=colors["text_muted"], bg=colors["surface"]).pack(anchor="w", pady=(10, 2))
        entry_user = tk.Entry(f_frame, font=("Arial", 11), bg=colors["bg"], fg=colors["text"], insertbackground=colors["text"], relief=tk.SOLID, bd=1)
        entry_user.pack(fill=tk.X, ipady=4, pady=(0, 10))
        entry_user.insert(0, "admin")
        
        tk.Label(f_frame, text="Access Password Verification:", font=("Arial", 10, "bold"), fg=colors["text_muted"], bg=colors["surface"]).pack(anchor="w", pady=(5, 2))
        entry_pass = tk.Entry(f_frame, font=("Arial", 11), show="*", bg=colors["bg"], fg=colors["text"], insertbackground=colors["text"], relief=tk.SOLID, bd=1)
        entry_pass.pack(fill=tk.X, ipady=4, pady=(0, 20))
        entry_pass.insert(0, "infinity123")
        
        def run_auth_sequence():
            u = entry_user.get().strip()
            p = entry_pass.get().strip()
            
            if not u or not p:
                messagebox.showerror("Auth Failure", "Fields must be completely populated.")
                return
                
            if u in self.db["users"] and self.db["users"][u] == p:
                self.current_user = u
                self.show_home_dashboard()
            else:
                if messagebox.askyesno("Account Missing", "Profile identification tag unrecognized. Register brand new candidate?"):
                    self.db["users"][u] = p
                    self.db["bookmarks"][u] = []
                    self.db["history"][u] = []
                    DatabaseManager.save_data(self.db)
                    self.current_user = u
                    self.show_home_dashboard()

        btn_login = tk.Button(center_frame, text="Verify Credentials & Mount Base", font=("Arial", 11, "bold"), 
                              bg=colors["accent"], fg="white", bd=0, cursor="hand2", command=run_auth_sequence)
        btn_login.pack(fill=tk.X, padx=40, ipady=6, pady=10)

    # ==========================================
    # SCREEN 2: HOME DASHBOARD
    # ==========================================
    def show_home_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        colors = THEMES[self.current_theme]
        self.create_branded_header(self.root, f"Workspace Hub: {self.current_user}", show_nav=False)
        
        auto_recovery_file = f"recovery_vol1_{self.current_user}.json"
        if os.path.exists(auto_recovery_file):
            if messagebox.askyesno("Recovery Notice", "Unfinished session layout metadata found. Reconstitute core state?"):
                self.hydrate_recovered_session(auto_recovery_file)
                return
            else:
                os.remove(auto_recovery_file)

        main_paned = tk.Frame(self.root, bg=colors["bg"])
        main_paned.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        left_deck = tk.Frame(main_paned, bg=colors["bg"])
        left_deck.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        profile_card = tk.Frame(left_deck, bg=colors["surface"], bd=1, relief=tk.GROOVE)
        profile_card.pack(fill=tk.X, pady=(0, 15), padx=15, ipady=15)
        
        user_history = self.db["history"].get(self.current_user, [])
        total_runs = len(user_history)
        avg_score = int(sum(h['percentage'] for h in user_history)/total_runs) if total_runs > 0 else 0
        
        badge = "Novice Apprentice"
        if avg_score >= 90 and total_runs >= 5: badge = "Master Educator Elite"
        elif avg_score >= 75 and total_runs >= 3: badge = "Pro Senior Coach"
        elif total_runs >= 1: badge = "Consistent Explorer"
        
        tk.Label(profile_card, text=f"Welcome back, Specialist {self.current_user}!", font=("Arial", 13, "bold"), fg=colors["accent"], bg=colors["surface"]).pack(anchor="w", padx=10, pady=5)
        tk.Label(profile_card, text=f"Rank Tier Status: 🏅 {badge}", font=("Arial", 10, "italic"), fg=colors["success"], bg=colors["surface"]).pack(anchor="w", padx=10, pady=2)
        tk.Label(profile_card, text=f"Recorded Performance Logs: {total_runs} Completed   |   Mean Accuracy: {avg_score}%", font=("Arial", 9), fg=colors["text_muted"], bg=colors["surface"]).pack(anchor="w", padx=10, pady=5)
        
        mod_card = tk.Frame(left_deck, bg=colors["surface"], bd=1, relief=tk.GROOVE)
        mod_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(mod_card, text="Select Chapter Focus Module:", font=("Arial", 11, "bold"), fg=colors["text"], bg=colors["surface"]).pack(anchor="w", padx=15, pady=10)
        
        options_map = [
            ("Chapter 1: Exercise 1.8 (Matrices & Determinants)", "Exercise 1.8"),
            ("Chapter 2: Exercise 2.9 (Complex Numbers)", "Exercise 2.9"),
            ("Chapter 3: Exercise 3.7 (Theory of Equations)", "Exercise 3.7"),
            ("Chapter 4: Exercise 4.6 (Inverse Trigonometric)", "Exercise 4.6"),
            ("Chapter 5: Exercise 5.6 (Analytical Geometry II)", "Exercise 5.6"),
            ("Chapter 6: Exercise 6.10 (Vector Algebra)", "Exercise 6.10"),
            ("[Master Deck Matrix]: Combined Universal Evaluation Pool", "ALL")
        ]
        
        selected_mod = tk.StringVar(value="ALL")
        for txt, val in options_map:
            rb = tk.Radiobutton(mod_card, text=txt, variable=selected_mod, value=val, font=("Arial", 10), 
                                bg=colors["surface"], fg=colors["text"], activebackground=colors["surface"], selectcolor=colors["surface"], anchor="w")
            rb.pack(fill=tk.X, padx=20, pady=4)
            
        strat_frame = tk.Frame(mod_card, bg=colors["bg"], pady=10)
        strat_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=15)
        
        engine_mode = tk.StringVar(value="PRACTICE")
        
        rb_prac = tk.Radiobutton(strat_frame, text="Practice Mode (Untimed, Immediate Keys)", variable=engine_mode, value="PRACTICE", font=("Arial", 9, "bold"), bg=colors["bg"], fg=colors["text"])
        rb_prac.pack(side=tk.LEFT, padx=10)
        rb_exam = tk.Radiobutton(strat_frame, text="Exam Mode (Strict Clock, Sealed Matrix)", variable=engine_mode, value="EXAM", font=("Arial", 9, "bold"), bg=colors["bg"], fg=colors["text"])
        rb_exam.pack(side=tk.LEFT, padx=10)
        
        btn_fire = tk.Button(mod_card, text="⚡ Instantiate Operational Test Session", font=("Arial", 11, "bold"), 
                             bg=colors["accent"], fg="white", bd=0, padx=15, pady=8, cursor="hand2",
                             command=lambda: self.initialize_test_vectors(selected_mod.get(), engine_mode.get()))
        btn_fire.pack(fill=tk.X, side=tk.BOTTOM, padx=15)

        right_panel = tk.Frame(main_paned, bg=colors["surface"], width=360, bd=1, relief=tk.GROOVE)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        tk.Label(right_panel, text="Diagnostic Historical Matrix", font=("Arial", 11, "bold"), fg=colors["text"], bg=colors["surface"]).pack(pady=10)
        
        tree_frame = tk.Frame(right_panel)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("date", "scope", "efficiency")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        tree.heading("date", text="Timeline Stamp")
        tree.heading("scope", text="Target Scope")
        tree.heading("efficiency", text="Efficiency Score")
        
        tree.column("date", width=90, anchor=tk.CENTER)
        tree.column("scope", width=120, anchor=tk.W)
        tree.column("efficiency", width=80, anchor=tk.CENTER)
        tree.pack(fill=tk.BOTH, expand=True)
        
        total_correct, total_wrong, total_skipped = 0, 0, 0
        for entry in user_history:
            tree.insert("", tk.END, values=(entry.get("date", "N/A"), entry.get("scope", "All"), f"{entry.get('percentage', 0)}%"))
            total_correct += entry.get("correct", 0)
            total_wrong += entry.get("wrong", 0)
            total_skipped += entry.get("skipped", 0)
            
        tk.Label(right_panel, text="Aggregated Micro-Efficiency Distribution", font=("Arial", 9, "bold"), fg=colors["text_muted"], bg=colors["surface"]).pack(pady=(10, 2))
        chart = ModernChart(right_panel, width=340, height=180, bg_color=colors["surface"])
        chart.pack(pady=5)
        chart.draw_pie(total_correct, total_wrong, total_skipped, colors)

    # ==========================================
    # SESSION CORE INITIALIZATION
    # ==========================================
    def initialize_test_vectors(self, filter_scope, mode_key):
        if filter_scope == "ALL":
            self.questions = list(ALL_QUESTIONS)
        else:
            self.questions = [q for q in ALL_QUESTIONS if q["exercise"] == filter_scope]
            
        if not self.questions:
            messagebox.showwarning("Index Exception", "Requested criteria targets an empty registry vector.")
            return
            
        random.shuffle(self.questions)
        for idx, q in enumerate(self.questions):
            q_copy = dict(q)
            opts = list(q["options"])
            random.shuffle(opts)
            q_copy["shuffled_options"] = opts
            q_copy["index_pointer"] = idx
            self.questions[idx] = q_copy
            
        self.current_index = 0
        self.score = 0
        self.user_answers = {}
        self.is_exam_mode = (mode_key == "EXAM")
        self.active_session = filter_scope
        self.start_time_stamp = time.time()
        
        if self.current_user not in self.db["bookmarks"]:
            self.db["bookmarks"][self.current_user] = []
        self.bookmarks = self.db["bookmarks"][self.current_user]
        
        if self.is_exam_mode:
            self.time_remaining = len(self.questions) * 45 
            self.timer_running = True
            
        self.setup_quiz_interface()
        self.load_question()
        if self.is_exam_mode:
            self.heartbeat_timer_tick()

    # ==========================================
    # SCREEN 3: RUNTIME TESTBED
    # ==========================================
    def setup_quiz_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        colors = THEMES[self.current_theme]
        self.create_branded_header(self.root, "Active Evaluation Environment Engine")
        
        split_panes = tk.Frame(self.root, bg=colors["bg"])
        split_panes.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        left_workspace = tk.Frame(split_panes, bg=colors["bg"])
        left_workspace.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        meta_strip = tk.Frame(left_workspace, bg=colors["surface"], bd=1, relief=tk.GROOVE)
        meta_strip.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=5)
        
        self.lbl_meta = tk.Label(meta_strip, text="", font=("Arial", 10, "bold"), fg=colors["text_muted"], bg=colors["surface"])
        self.lbl_meta.pack(side=tk.LEFT, padx=5)
        
        self.lbl_timer = tk.Label(meta_strip, text="", font=("Arial", 11, "bold"), fg=colors["danger"], bg=colors["surface"])
        self.lbl_timer.pack(side=tk.RIGHT, padx=5)
        
        self.progress = ttk.Progressbar(left_workspace, orient="horizontal", mode="determinate", style="TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 15))
        
        q_container = tk.Frame(left_workspace, bg=colors["surface"], bd=1, relief=tk.GROOVE, padx=20, pady=20)
        q_container.pack(fill=tk.BOTH, expand=True)
        
        self.lbl_question = tk.Label(q_container, text="", font=("Arial", 12, "bold"), fg=colors["text"], bg=colors["surface"], wraplength=540, justify=tk.LEFT)
        self.lbl_question.pack(anchor="w", pady=(0, 20))
        
        self.options_group = tk.Frame(q_container, bg=colors["surface"])
        self.options_group.pack(fill=tk.X)
        
        self.selected_option = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_group, text="", font=("Arial", 10), bg=colors["bg"], fg=colors["text"], 
                            activebackground=colors["primary_light"], activeforeground=colors["text"],
                            bd=1, relief=tk.SOLID, anchor="w", padx=15, pady=10, cursor="hand2")
            btn.pack(fill=tk.X, pady=6)
            self.option_buttons.append(btn)
            
        control_bar = tk.Frame(left_workspace, bg=colors["bg"], pady=15)
        control_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.btn_prev = tk.Button(control_bar, text="◀ Previous", font=("Arial", 10, "bold"), bg=colors["primary"], fg="white", bd=0, padx=12, pady=6, command=self.go_previous_node)
        self.btn_prev.pack(side=tk.LEFT, padx=2)
        
        self.btn_skip = tk.Button(control_bar, text="Skip Question ⏭", font=("Arial", 10), bg=colors["text_muted"], fg="white", bd=0, padx=12, pady=6, command=self.skip_current_node)
        self.btn_skip.pack(side=tk.LEFT, padx=2)
        
        self.btn_bookmark = tk.Button(control_bar, text="🔖 Bookmark Vector", font=("Arial", 10), bg=colors["primary"], fg="white", bd=0, padx=12, pady=6, command=self.toggle_bookmark_state)
        self.btn_bookmark.pack(side=tk.LEFT, padx=2)
        
        self.btn_commit = tk.Button(control_bar, text="Submit Answer ✔", font=("Arial", 10, "bold"), bg=colors["success"], fg="white", bd=0, padx=18, pady=6, command=self.commit_selected_answer)
        self.btn_commit.pack(side=tk.RIGHT, padx=2)
        
        self.btn_terminate = tk.Button(control_bar, text="Halt & Finalize", font=("Arial", 10, "bold"), bg=colors["danger"], fg="white", bd=0, padx=12, pady=6, command=self.manual_abort_sequence)
        self.btn_terminate.pack(side=tk.RIGHT, padx=15)

        right_sidebar = tk.Frame(split_panes, bg=colors["surface"], width=240, bd=1, relief=tk.GROOVE, padx=10, pady=10)
        right_sidebar.pack(side=tk.RIGHT, fill=tk.BOTH)
        right_sidebar.pack_propagate(False)
        
        tk.Label(right_sidebar, text="Structural Map Index Layout", font=("Arial", 10, "bold"), fg=colors["text"], bg=colors["surface"]).pack(pady=(0, 10))
        
        self.matrix_container = tk.Frame(right_sidebar, bg=colors["surface"])
        self.matrix_container.pack(fill=tk.BOTH, expand=True)
        self.render_navigation_matrix_grid()

    def render_navigation_matrix_grid(self):
        for w in self.matrix_container.winfo_children():
            w.destroy()
            
        colors = THEMES[self.current_theme]
        cols = 4
        for i, q in enumerate(self.questions):
            btn_bg = colors["bg"]
            btn_fg = colors["text"]
            
            if i == self.current_index:
                btn_bg = colors["accent"]
                btn_fg = "white"
            elif i in self.user_answers:
                if self.is_exam_mode:
                    btn_bg = colors["primary_light"]
                else:
                    is_ok = (self.user_answers[i] == self.questions[i]["correct"])
                    btn_bg = colors["success"] if is_ok else colors["danger"]
                    if not is_ok: btn_fg = "white"
            
            r, c = divmod(i, cols)
            m_btn = tk.Button(self.matrix_container, text=str(i+1), font=("Arial", 9, "bold"), bg=btn_bg, fg=btn_fg,
                              width=4, height=2, bd=1, relief=tk.GROOVE, command=lambda target=i: self.jump_to_node_index(target))
            m_btn.grid(row=r, column=c, padx=3, pady=3)

    # ==========================================
    # DIAGNOSTIC ENGINE COMPONENT PIPELINES
    # ==========================================
    def load_question(self):
        colors = THEMES[self.current_theme]
        if self.current_index >= len(self.questions):
            self.current_index = len(self.questions) - 1
            
        q = self.questions[self.current_index]
        self.lbl_meta.config(text=f"📌 Module: {q['exercise']}  |  Book Ref: Q.{q['book_num']}  |  Index Block: {self.current_index + 1} / {len(self.questions)}")
        self.lbl_question.config(text=q["question"])
        
        self.progress['value'] = ((self.current_index + 1) / len(self.questions)) * 100
        
        is_bookmarked = any(b["question"] == q["question"] for b in self.bookmarks)
        self.btn_bookmark.config(text="🔖 Bookmarked" if is_bookmarked else "🔖 Bookmark Vector", bg=colors["success"] if is_bookmarked else colors["primary"])
        
        shuffled_opts = q["shuffled_options"]
        ans_committed = self.user_answers.get(self.current_index, None)
        
        for i in range(4):
            opt_val = shuffled_opts[i]
            self.option_buttons[i].config(text=opt_val, bg=colors["bg"], fg=colors["text"], state=tk.NORMAL, command=lambda v=opt_val: self.selected_option.set(v))
            
            if ans_committed:
                self.option_buttons[i].config(state=tk.DISABLED)
                if self.is_exam_mode:
                    if opt_val == ans_committed:
                        self.option_buttons[i].config(bg=colors["primary_light"])
                else:
                    if opt_val == q["correct"]:
                        self.option_buttons[i].config(bg=colors["success"], fg="white")
                    elif opt_val == ans_committed:
                        self.option_buttons[i].config(bg=colors["danger"], fg="white")
                        
        if ans_committed:
            self.btn_commit.config(text="Locked", state=tk.DISABLED, bg=colors["text_muted"])
        else:
            self.btn_commit.config(text="Submit Answer ✔", state=tk.NORMAL, bg=colors["success"])
            
        self.selected_option.set(ans_committed if ans_committed else "")
        self.render_navigation_matrix_grid()
        self.write_auto_save_recovery_checkpoint()

    def commit_selected_answer(self):
        val = self.selected_option.get()
        if not val:
            messagebox.showwarning("Execution Warn", "Selection mapping is empty. Allocate target register tracking vector parameter.")
            return
            
        self.user_answers[self.current_index] = val
        q = self.questions[self.current_index]
        
        if not self.is_exam_mode:
            if val == q["correct"]:
                self.score += 1
                
        self.load_question()
        self.root.after(400, self.go_next_node)

    def go_next_node(self):
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            self.load_question()
        elif len(self.user_answers) == len(self.questions):
            self.trigger_final_evaluation_sequence()

    def go_previous_node(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_question()

    def skip_current_node(self):
        self.go_next_node()

    def jump_to_node_index(self, index):
        self.current_index = index
        self.load_question()

    def toggle_bookmark_state(self):
        q = self.questions[self.current_index]
        match = [b for b in self.bookmarks if b["question"] == q["question"]]
        if match:
            self.bookmarks.remove(match[0])
        else:
            self.bookmarks.append({"exercise": q["exercise"], "book_num": q["book_num"], "question": q["question"], "correct": q["correct"]})
            
        self.db["bookmarks"][self.current_user] = self.bookmarks
        DatabaseManager.save_data(self.db)
        self.load_question()

    # ==========================================
    # TIMER HEARTBEAT MODULE ENGINE
    # ==========================================
    def heartbeat_timer_tick(self):
        if not self.timer_running: return
        if self.time_remaining <= 0:
            self.timer_running = False
            messagebox.showinfo("Timeout Limit", "Allocated timeframe expired. Compiling calculations layout results matrix.")
            self.trigger_final_evaluation_sequence()
            return
            
        m, s = divmod(self.time_remaining, 60)
        self.lbl_timer.config(text=f"⏱ Countdown Matrix: {m:02d}:{s:02d}")
        self.time_remaining -= 1
        self.root.after(1000, self.heartbeat_timer_tick)

    # ==========================================
    # AUTO SAVE CHECKPOINT PROTECTION
    # ==========================================
    def write_auto_save_recovery_checkpoint(self):
        checkpoint = {
            "user": self.current_user, "index": self.current_index, "score": self.score,
            "answers": {str(k): v for k, v in self.user_answers.items()},
            "questions": self.questions, "exam": self.is_exam_mode, "time": self.time_remaining,
            "scope": self.active_session
        }
        with open(f"recovery_vol1_{self.current_user}.json", 'w') as f:
            json.dump(checkpoint, f)

    def hydrate_recovered_session(self, path):
        try:
            with open(path, 'r') as f:
                cp = json.load(f)
            self.current_index = cp["index"]
            self.score = cp["score"]
            self.user_answers = {int(k): v for k, v in cp["answers"].items()}
            self.questions = cp["questions"]
            self.is_exam_mode = cp["exam"]
            self.time_remaining = cp["time"]
            self.active_session = cp["scope"]
            
            self.setup_quiz_interface()
            self.load_question()
            if self.is_exam_mode:
                self.timer_running = True
                self.heartbeat_timer_tick()
        except Exception as e:
            messagebox.showerror("Hydration Error", f"Core operational mapping load fault encountered: {e}")
            self.show_home_dashboard()

    def clean_recovery_checkpoint(self):
        path = f"recovery_vol1_{self.current_user}.json"
        if os.path.exists(path): os.remove(path)

    def manual_abort_sequence(self):
        if messagebox.askyesno("Operational Exit Intercept", "Compile partial tracking metric variables data and abort runtime session?"):
            self.trigger_final_evaluation_sequence()

    # ==========================================
    # SCREEN 4: POST ROUTINE PERFORMANCE ANALYTICS
    # ==========================================
    def trigger_final_evaluation_sequence(self):
        self.timer_running = False
        self.clean_recovery_checkpoint()
        
        if self.is_exam_mode:
            self.score = 0
            for idx, q in enumerate(self.questions):
                if self.user_answers.get(idx) == q["correct"]:
                    self.score += 1
                    
        total = len(self.questions)
        skipped = total - len(self.user_answers)
        wrong = total - self.score - skipped
        pct = int((self.score / total) * 100) if total > 0 else 0
        
        log_entry = {
            "date": time.strftime("%Y-%m-%d %H:%M"), "scope": self.active_session,
            "total": total, "correct": self.score, "wrong": wrong, "skipped": skipped, "percentage": pct
        }
        if self.current_user not in self.db["history"]:
            self.db["history"][self.current_user] = []
        self.db["history"][self.current_user].append(log_entry)
        DatabaseManager.save_data(self.db)
        
        self.display_review_screen(log_entry)

    def display_review_screen(self, session_summary):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        colors = THEMES[self.current_theme]
        self.create_branded_header(self.root, "Performance Diagnostics Overview")
        
        outer_layout = tk.Frame(self.root, bg=colors["bg"])
        outer_layout.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        lbl_stats = tk.Label(outer_layout, text=f"Metric Matrix Efficiency Status: {session_summary['percentage']}% Accuracy Calculated", 
                             font=("Arial", 14, "bold"), fg=colors["accent"], bg=colors["bg"])
        lbl_stats.pack(anchor="w", pady=(0, 10))
        
        text_area = ScrolledText(outer_layout, font=("Courier New", 10), bg=colors["surface"], fg=colors["text"], insertbackground=colors["text"], relief=tk.SUNKEN, bd=2)
        text_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        buf = "="*90 + "\n"
        buf += f" MASTER DIAGNOSTIC REPORT LEDGER  | RUN TIMELINE: {session_summary['date']}\n"
        buf += f" Evaluation Scope Targets Matrix Segment Target: {session_summary['scope']}\n"
        buf += f" Core Calculated Parameter Metrics: Correct: {session_summary['correct']} | Wrong: {session_summary['wrong']} | Skipped: {session_summary['skipped']} [Total Pool: {session_summary['total']}]\n"
        buf += "="*90 + "\n\n"
        
        for idx, q in enumerate(self.questions):
            ans = self.user_answers.get(idx, "[Skipped Matrix Register Value]")
            status_flag = "SKIPPED" if idx not in self.user_answers else ("CORRECT" if ans == q["correct"] else "WRONG")
            
            buf += f" Block Line Segment Reference Item {idx+1}: {q['exercise']} - Question textbook pointer key reference: Q.No {q['book_num']}\n"
            buf += f" String Core Text: {q['question']}\n"
            buf += f" Verified Answer Ledger Index Tracking Key: {q['correct']}\n"
            buf += f" Candidate Selection Output Record Matrix: {ans} -> Entry Status Flag Marker Result: [{status_flag}]\n"
            buf += "-"*90 + "\n"
            
        text_area.insert(tk.INSERT, buf)
        text_area.configure(state=tk.DISABLED)
        
        control_panel = tk.Frame(outer_layout, bg=colors["bg"])
        control_panel.pack(fill=tk.X, pady=(15, 0))
        
        btn_home = tk.Button(control_panel, text="↩ Exit Workspace to Home Hub", font=("Arial", 10, "bold"), bg=colors["accent"], fg="white", bd=0, padx=15, pady=8, command=self.show_home_dashboard)
        btn_home.pack(side=tk.LEFT)
        
        btn_export = tk.Button(control_panel, text="💾 Export Audit Report Text File", font=("Arial", 10, "bold"), bg=colors["success"], fg="white", bd=0, padx=15, pady=8, command=lambda: self.export_to_text_report(buf))
        btn_export.pack(side=tk.RIGHT)

    def export_to_text_report(self, report_buffer_data):
        target_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Ledger File Format", "*.txt")], title="Save Performance Data Mapping Profile")
        if target_path:
            try:
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(report_buffer_data)
                messagebox.showinfo("Export Success", "Performance Audit tracking metrics written cleanly to physical disk partition.")
            except Exception as e:
                messagebox.showerror("Export Exception", f"File IO modification operations write context exception fault standard: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApplication(root)
    root.mainloop()
