import pytest
import kernels

def test_awkward_reduce_count_64_1():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 19
	outlength = 9
	parents = [1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_2():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 19
	outlength = 8
	parents = [1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [0, 3, 0, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_3():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 1696
	outlength = 331
	parents = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 68, 68, 68, 68, 68, 68, 68, 68, 68, 68, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 119, 119, 119, 119, 119, 119, 119, 119, 119, 119, 136, 136, 136, 136, 136, 136, 136, 136, 136, 136, 153, 153, 153, 153, 153, 153, 153, 153, 153, 153, 170, 170, 170, 170, 170, 170, 170, 170, 170, 170, 187, 187, 187, 187, 187, 187, 187, 187, 187, 187, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 69, 69, 69, 69, 69, 69, 69, 69, 69, 69, 86, 86, 86, 86, 86, 86, 86, 86, 86, 86, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 137, 137, 137, 137, 137, 137, 137, 137, 137, 137, 154, 154, 154, 154, 154, 154, 154, 154, 154, 154, 171, 171, 171, 171, 171, 171, 171, 171, 171, 171, 188, 188, 188, 188, 188, 188, 188, 188, 188, 188, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 53, 53, 53, 53, 53, 53, 53, 53, 53, 53, 70, 70, 70, 70, 70, 70, 70, 70, 70, 70, 87, 87, 87, 87, 87, 87, 87, 87, 87, 87, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 138, 138, 138, 138, 138, 138, 138, 138, 138, 138, 155, 155, 155, 155, 155, 155, 155, 155, 155, 155, 172, 172, 172, 172, 172, 172, 172, 172, 172, 172, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 88, 88, 88, 88, 88, 88, 88, 88, 88, 88, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 156, 156, 156, 156, 156, 156, 156, 156, 156, 156, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 55, 55, 55, 55, 55, 55, 55, 55, 55, 55, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 89, 89, 89, 89, 89, 89, 89, 89, 89, 89, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 157, 157, 157, 157, 157, 157, 157, 157, 157, 157, 174, 174, 174, 174, 174, 174, 174, 174, 174, 174, 191, 191, 191, 191, 191, 191, 191, 191, 191, 191, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 73, 73, 73, 73, 73, 73, 73, 73, 73, 73, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 141, 141, 141, 141, 141, 141, 141, 141, 141, 141, 158, 158, 158, 158, 158, 158, 158, 158, 158, 158, 175, 175, 175, 175, 175, 175, 175, 175, 175, 175, 192, 192, 192, 192, 192, 192, 192, 192, 192, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 57, 57, 57, 57, 57, 57, 57, 57, 57, 57, 74, 74, 74, 74, 74, 74, 74, 74, 74, 74, 91, 91, 91, 91, 91, 91, 91, 91, 91, 91, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 142, 142, 142, 142, 142, 142, 142, 142, 142, 142, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 176, 176, 176, 176, 176, 176, 176, 176, 176, 176, 193, 193, 193, 193, 193, 193, 193, 193, 193, 193, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 58, 58, 58, 58, 58, 58, 58, 58, 58, 58, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 92, 92, 92, 92, 92, 92, 92, 92, 92, 92, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 143, 143, 143, 143, 143, 143, 143, 143, 143, 143, 160, 160, 160, 160, 160, 160, 160, 160, 160, 160, 177, 177, 177, 177, 177, 177, 177, 177, 177, 177, 194, 194, 194, 194, 194, 194, 194, 194, 194, 194, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [626, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_4():
	toptr = [123, 123, 123]
	lenparents = 3
	outlength = 3
	parents = [0, 0, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [2, 0, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_5():
	toptr = [123]
	lenparents = 3
	outlength = 1
	parents = [0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_6():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 9
	outlength = 6
	parents = [0, 0, 0, 2, 2, 3, 4, 4, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 0, 2, 1, 2, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_7():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 9
	outlength = 8
	parents = [0, 0, 0, 6, 6, 1, 1, 7, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 2, 1, 0, 0, 0, 2, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_8():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_9():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 4, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_10():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 22
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_11():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 22
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 0, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_12():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 24
	outlength = 9
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3, 0]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_13():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 24
	outlength = 8
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7, 7]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 2, 5, 4, 0, 4, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_14():
	toptr = [123, 123, 123]
	lenparents = 9
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_15():
	toptr = [123, 123, 123, 123]
	lenparents = 10
	outlength = 4
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 1]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_16():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 18
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_17():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 21
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_18():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 30
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_19():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 23
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 3, 5, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_20():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 23
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 3, 3, 5, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_21():
	toptr = [123, 123, 123]
	lenparents = 10
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_22():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 43
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4, 2, 4, 5, 6, 4, 5, 7]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_23():
	toptr = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	lenparents = 39
	outlength = 10
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 9]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 4, 3, 3, 5, 6, 4, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_24():
	toptr = [123, 123, 123]
	lenparents = 11
	outlength = 3
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_25():
	toptr = [123, 123, 123, 123, 123, 123]
	lenparents = 20
	outlength = 6
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5, 3, 3, 3]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_26():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 25
	outlength = 7
	parents = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [3, 3, 5, 3, 3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_27():
	toptr = [123]
	lenparents = 5
	outlength = 1
	parents = [0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_28():
	toptr = [123, 123]
	lenparents = 10
	outlength = 2
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_29():
	toptr = [123, 123, 123, 123, 123, 123, 123]
	lenparents = 29
	outlength = 7
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [5, 5, 5, 3, 3, 3, 5]
	assert toptr == pytest_toptr


def test_awkward_reduce_count_64_30():
	toptr = [123]
	lenparents = 6
	outlength = 1
	parents = [0, 0, 0, 0, 0, 0]
	funcPy = getattr(kernels, 'awkward_reduce_count_64')
	funcPy(toptr = toptr,lenparents = lenparents,outlength = outlength,parents = parents)
	pytest_toptr = [6]
	assert toptr == pytest_toptr


