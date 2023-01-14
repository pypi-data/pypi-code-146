from math import acos, cos, pi, sin, sqrt
from random import gauss, uniform


class Vector6D:
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float) -> None:
        """class used to perform operations on a vector that has 6 components

        :param x: first component of vector
        :type x: float
        :param y: second component of vector
        :type y: float
        :param z: third component of vector
        :type z: float
        :param vx: fourth component of vector
        :type vx: float
        :param vy: fifth component of vector
        :type vy: float
        :param vz: sixth component of vector
        :type vz: float
        """
        #: first component of the vector
        self.x: float = x

        #: second component of the vector
        self.y: float = y

        #: third component of the vector
        self.z: float = z

        #: fourth component of the vector
        self.vx: float = vx

        #: fifth component of the vector
        self.vy: float = vy

        #: sixth component of the vector
        self.vz: float = vz

    @classmethod
    def from_position_and_velocity(cls, r: "Vector3D", v: "Vector3D") -> "Vector6D":
        """create a 6-dimension vecto from 3-D position and velocity

        :param r: 3-D position vector
        :type r: Vector3D
        :param v: 3-D velocity vector
        :type v: Vector3D
        :return: 6-D state vector
        :rtype: Vector6D
        """
        return cls(r.x, r.y, r.z, v.x, v.y, v.z)

    def __str__(self) -> str:
        """overrides the string method so stored values will be printed

        :return: string representation of the vector
        :rtype: str
        """
        return f"{self.x:.6f} {self.y:.6f} {self.z:.6f} {self.vx:.6f} {self.vy:.6f} {self.vz:.6f}"

    def dot(self, vec_to_dot: "Vector6D") -> float:
        """calculates the dot product of the two vectors

        :param vec_to_dot: the second vector to be used in the dot product
        :type vec_to_dot: Vector6D
        :return: sum of the element products
        :rtype: float
        """
        return (
            self.x * vec_to_dot.x
            + self.y * vec_to_dot.y
            + self.z * vec_to_dot.z
            + self.vx * vec_to_dot.vx
            + self.vy * vec_to_dot.vy
            + self.vz * vec_to_dot.vz
        )

    def copy(self) -> "Vector6D":
        """create a replica of the current vector

        :return: 6-D vector with components that match the calling vector
        :rtype: Vector6D
        """
        return Vector6D(self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def plus(self, vec: "Vector6D") -> "Vector6D":
        """calculates the sum of the elements of the two vectors

        :param vec: second vector to be included in the sum
        :type vec: Vector6D
        :return: vector whose elements are sums of the calling and argument vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.x + vec.x,
            self.y + vec.y,
            self.z + vec.z,
            self.vx + vec.vx,
            self.vy + vec.vy,
            self.vz + vec.vz,
        )

    def minus(self, vec: "Vector6D") -> "Vector6D":
        """calculates the difference of the elements of the two vectors

        :param vec: second vector to be included in the difference
        :type vec: Vector6D
        :return: vector whose elements are the difference of the calling and argument vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.x - vec.x,
            self.y - vec.y,
            self.z - vec.z,
            self.vx - vec.vx,
            self.vy - vec.vy,
            self.vz - vec.vz,
        )


class Vector3D:
    def __init__(self, x: float, y: float, z: float) -> None:
        """class used to perform operations on a 3-dimension vector

        :param x: first component of the vector
        :type x: float
        :param y: second component of the vector
        :type y: float
        :param z: third component of the vector
        :type z: float
        """
        #: first component of the vector
        self.x: float = x

        #: second component of the vector
        self.y: float = y

        #: third component of the vector
        self.z: float = z

    def with_noise(self, range_err: float, ang_err: float) -> "Vector3D":
        """calculate a new vector with noise applied to magnitude and direction

        :param range_err: one-sigma range error in units consistent with the calling vector
        :type range_err: float
        :param ang_err: one-sigma anglular error in radians
        :type ang_err: float
        :return: new vector with gaussian noise applied
        :rtype: Vector3D
        """
        return self.with_magnitude_noise(range_err).with_angular_noise(ang_err)

    def with_magnitude_noise(self, range_err: float) -> "Vector3D":
        """calculate a new vector with noise applied to the magnitude

        :param range_err: one-sigma range error in units consistent with the calling vector
        :type range_err: float
        :return: new vector with the magnitude adjusted by gaussian distribution
        :rtype: Vector3D
        """
        return self.normalized().scaled(gauss(self.magnitude(), range_err))

    def with_angular_noise(self, ang_err: float) -> "Vector3D":
        """calculate a new vector with angular noise applied

        :param ang_err: one-sigma anglular error in radians
        :type ang_err: float
        :return: new vector offset using gaussian distribution for the angle
        :rtype: Vector3D
        """
        return self.rotation_about_axis(self.cross(Vector3D(0, 0, 1)), gauss(0, ang_err)).rotation_about_axis(
            self, uniform(0, 2 * pi)
        )

    def __str__(self) -> str:
        """overrides the string method so the elements can be viewed

        :return: string representation of the vector elements
        :rtype: str
        """
        return f"{self.x:.6f} {self.y:.6f} {self.z:.6f}"

    def copy(self) -> "Vector3D":
        """creates a replica of the vector

        :return: 3-D vector with elements equal to the calling vector
        :rtype: Vector3D
        """
        return Vector3D(self.x, self.y, self.z)

    def plus(self, vec_to_add: "Vector3D") -> "Vector3D":
        """creates a vector whose elements equal the sum of the calling and argument vector

        :param vec_to_add: vector to be included in the sum
        :type vec_to_add: Vector3D
        :return: vector with elements equal to the sum of the calling and argument vector
        :rtype: Vector3D
        """
        return Vector3D(self.x + vec_to_add.x, self.y + vec_to_add.y, self.z + vec_to_add.z)

    def minus(self, vec_to_subtract: "Vector3D") -> "Vector3D":
        """creates a vector whose elements equal the difference of the calling and argument vector

        :param vec_to_subtract: vector to be included in the difference
        :type vec_to_subtract: Vector3D
        :return: vector with elements equal to the difference of the calling and argument vector
        :rtype: Vector3D
        """
        return Vector3D(
            self.x - vec_to_subtract.x,
            self.y - vec_to_subtract.y,
            self.z - vec_to_subtract.z,
        )

    def dot(self, vec_to_dot: "Vector3D") -> float:
        """calculates the dot product of the two vectors

        :param vec_to_dot: the second vector to be used in the dot product
        :type vec_to_dot: Vector3D
        :return: sum of the element products
        :rtype: float
        """
        return self.x * vec_to_dot.x + self.y * vec_to_dot.y + self.z * vec_to_dot.z

    def cross(self, vec_to_cross: "Vector3D") -> "Vector3D":
        """creates a vector orthogonal to the calling and argument vector

        :param vec_to_cross: vector which will be used to complete the right-hand rule
        :type vec_to_cross: Vector3D
        :return: vector produced using the right-hand rule that is orthogonal to the original vectors
        :rtype: Vector3D
        """
        return Vector3D(
            self.y * vec_to_cross.z - self.z * vec_to_cross.y,
            self.z * vec_to_cross.x - self.x * vec_to_cross.z,
            self.x * vec_to_cross.y - self.y * vec_to_cross.x,
        )

    def magnitude(self) -> float:
        """calculates the length of the vector

        :return: square root of the sum of squares
        :rtype: float
        """
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def scaled(self, scalar: float) -> "Vector3D":
        """creates a scaled copy of the calling vector

        :param scalar: value that will be multiplied against all elements
        :type scalar: float
        :return: vector equal to the calling vector scaled by the argument
        :rtype: Vector3D
        """
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalized(self) -> "Vector3D":
        """creates a vector parallel to the calling vector that is of length 1

        :return: unit vector of the calling vector
        :rtype: Vector3D
        """
        return self.scaled(1 / self.magnitude())

    def angle(self, adj_vec: "Vector3D") -> float:
        """calculates the angle between two vectors

        :param adj_vec: second leg of the angle
        :type adj_vec: Vector3D
        :return: angle in radians between the two vectors
        :rtype: float
        """
        arg = self.dot(adj_vec) / (self.magnitude() * adj_vec.magnitude())
        if arg > 1:
            arg = 1
        elif arg < -1:
            arg = -1
        return acos(arg)

    @staticmethod
    def rotation_matrix(axis: "Vector3D", theta: float) -> "Matrix3D":
        """calculates the rotation matrix required for a rotation

        :param axis: axis that will be used to rotate a vector around
        :type axis: Vector3D
        :param theta: angle in radians the vector will be rotated
        :type theta: float
        :return: transition matrix that will rotate a vector
        :rtype: Matrix3D
        """
        unit_ax: Vector3D = axis.normalized()
        ux: float = unit_ax.x
        uy: float = unit_ax.y
        uz: float = unit_ax.z
        c: float = cos(theta)
        s: float = sin(theta)
        cdiff: float = 1 - c

        x1: float = c + ux * ux * cdiff
        y1: float = ux * uy * cdiff - uz * s
        z1: float = ux * uz * cdiff + uy * s
        x2: float = uy * ux * cdiff + uz * s
        y2: float = c + uy * uy * cdiff
        z2: float = uy * uz * cdiff - ux * s
        x3: float = uz * ux * cdiff - uy * s
        y3: float = uz * uy * cdiff + ux * s
        z3: float = c + uz * uz * cdiff

        r1: Vector3D = Vector3D(x1, y1, z1)
        r2: Vector3D = Vector3D(x2, y2, z2)
        r3: Vector3D = Vector3D(x3, y3, z3)

        return Matrix3D(r1, r2, r3)

    def rotation_about_axis(self, axis: "Vector3D", theta: float) -> "Vector3D":
        """create a vector that has been rotated

        :param axis: axis of rotation
        :type axis: Vector3D
        :param theta: angle in radians of rotation
        :type theta: float
        :return: vector that has been rotated
        :rtype: Vector3D
        """
        return Vector3D.rotation_matrix(axis, theta).multiply_vector(self.copy())


class Matrix3D:
    def __init__(self, row1: Vector3D, row2: Vector3D, row3: Vector3D) -> None:
        """used to perform operations on a 3x3 matrix

        :param row1: first row of matrix
        :type row1: Vector3D
        :param row2: second row of matrix
        :type row2: Vector3D
        :param row3: third row of matrix
        :type row3: Vector3D
        """
        #: first row of matrix
        self.row1: Vector3D = row1.copy()

        #: second row of matrix
        self.row2: Vector3D = row2.copy()

        #: third row of matrix
        self.row3: Vector3D = row3.copy()

    def diagonal(self) -> Vector3D:
        """creates a vector with components equal to the diagonal of the matrix

        :return: vector equal to (xx, yy, zz)
        :rtype: Vector3D
        """
        return Vector3D(self.row1.x, self.row2.y, self.row3.z)

    def column_1(self) -> Vector3D:
        """creates a vector with elements equal to the first column of the matrix

        :return: vector with elements equal to the first column of the matrix
        :rtype: Vector3D
        """
        return Vector3D(self.row1.x, self.row2.x, self.row3.x)

    def column_2(self) -> Vector3D:
        """creates a vector with elements equal to the second column of the matrix

        :return: vector with elements equal to the second column of the matrix
        :rtype: Vector3D
        """
        return Vector3D(self.row1.y, self.row2.y, self.row3.y)

    def column_3(self) -> Vector3D:
        """creates a vector with elements equal to the third column of the matrix

        :return: vector with elements equal to the third column of the matrix
        :rtype: Vector3D
        """
        return Vector3D(self.row1.z, self.row2.z, self.row3.z)

    def multiply_vector(self, vec: Vector3D) -> Vector3D:
        """performs matrix multiplication of the calling matrix and the argument vector

        :param vec: vector to be used in the multiplication
        :type vec: Vector3D
        :return: product of the matrix multiplication
        :rtype: Vector3D
        """
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def scaled(self, scalar: float) -> "Matrix3D":
        """creates a matrix whose elements have been scaled by the argument

        :param scalar: multiple to be used in the scale
        :type scalar: float
        :return: matrix with elements equal to the original scaled by the multiple
        :rtype: Matrix3D
        """
        return Matrix3D(self.row1.scaled(scalar), self.row2.scaled(scalar), self.row3.scaled(scalar))

    def transpose(self) -> "Matrix3D":
        """creates a matrix whose rows are equal to the columns of the calling matrix

        :return: transposed matrix of the calling matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            Vector3D(self.row1.x, self.row2.x, self.row3.x),
            Vector3D(self.row1.y, self.row2.y, self.row3.y),
            Vector3D(self.row1.z, self.row2.z, self.row3.z),
        )

    def plus(self, mat: "Matrix3D") -> "Matrix3D":
        """creates a matrix whose elements are equal to the sum of the calling and argument matrix

        :param mat: matrix to be used in the sum
        :type mat: Matrix3D
        :return: sum matrix
        :rtype: Matrix3D
        """
        return Matrix3D(self.row1.plus(mat.row1), self.row2.plus(mat.row2), self.row3.plus(mat.row3))

    def determinant(self) -> float:
        """calculate the determinant of the matrix

        :return: determinant
        :rtype: float
        """
        return (
            self.row1.x * self.row2.y * self.row3.z
            + self.row1.y * self.row2.z * self.row3.x
            + self.row1.z * self.row2.x * self.row3.y
            - self.row1.z * self.row2.y * self.row3.x
            - self.row1.y * self.row2.x * self.row3.z
            - self.row1.x * self.row2.z * self.row3.y
        )

    def cofactor(self) -> "Matrix3D":
        """create a matrix that is the cofactor of the calling matrix

        :return: cofactor matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            Vector3D(
                self.row2.y * self.row3.z - self.row2.z * self.row3.y,
                -(self.row2.x * self.row3.z - self.row3.x * self.row2.z),
                self.row2.x * self.row3.y - self.row3.x * self.row2.y,
            ),
            Vector3D(
                -(self.row1.y * self.row3.z - self.row3.y * self.row1.z),
                self.row1.x * self.row3.z - self.row1.z * self.row3.x,
                -(self.row1.x * self.row3.y - self.row1.y * self.row3.x),
            ),
            Vector3D(
                self.row1.y * self.row2.z - self.row1.z * self.row2.y,
                -(self.row1.x * self.row2.z - self.row2.x * self.row1.z),
                self.row1.x * self.row2.y - self.row1.y * self.row2.x,
            ),
        )

    def adjugate(self) -> "Matrix3D":
        """create a matrix that is the adjugate of the calling matrix

        :return: adjugate matrix
        :rtype: Matrix3D
        """
        return self.cofactor().transpose()

    def inverse(self) -> "Matrix3D":
        """create a matrix that is the inverse of the calling matrix

        :return: inverse matrix
        :rtype: Matrix3D
        """
        return self.adjugate().scaled(1 / self.determinant())

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix3by6":
        """create a matrix that is the product of the calling 3x3 and an argument 3x6 matrix

        :param mat: 3x6 matrix to be used in the product
        :type mat: Matrix3by6
        :return: product matrix
        :rtype: Matrix3by6
        """
        return Matrix3by6(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
        )


class Matrix3by6:
    def __init__(self, row1: Vector6D, row2: Vector6D, row3: Vector6D) -> None:
        """used to perform operations for a 3x6 matrix

        :param row1: first row of the matrix
        :type row1: Vector6D
        :param row2: second row of the matrix
        :type row2: Vector6D
        :param row3: third row of the matrix
        :type row3: Vector6D
        """
        self.row1: Vector6D = row1.copy()
        self.row2: Vector6D = row2.copy()
        self.row3: Vector6D = row3.copy()

    def column_1(self) -> Vector3D:
        """create a vector whose elements are equal to the first column of the calling matrix

        :return: first column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.x, self.row2.x, self.row3.x)

    def column_2(self) -> Vector3D:
        """create a vector whose elements are equal to the second column of the calling matrix

        :return: second column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.y, self.row2.y, self.row3.y)

    def column_3(self) -> Vector3D:
        """create a vector whose elements are equal to the third column of the calling matrix

        :return: third column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.z, self.row2.z, self.row3.z)

    def column_4(self) -> Vector3D:
        """create a vector whose elements are equal to the fourth column of the calling matrix

        :return: fourth column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.vx, self.row2.vx, self.row3.vx)

    def column_5(self) -> Vector3D:
        """create a vector whose elements are equal to the fifth column of the calling matrix

        :return: fifth column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.vy, self.row2.vy, self.row3.vy)

    def column_6(self) -> Vector3D:
        """create a vector whose elements are equal to the sixth column of the calling matrix

        :return: sixth column
        :rtype: Vector3D
        """
        return Vector3D(self.row1.vz, self.row2.vz, self.row3.vz)

    def multiply_vector(self, vec: Vector6D) -> Vector3D:
        """create a vector that is the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: Vector6D
        :return: product vector
        :rtype: Vector3D
        """
        return Vector3D(self.row1.dot(vec), self.row2.dot(vec), self.row3.dot(vec))

    def transpose(self) -> "Matrix6by3":
        """create a matrix whose rows are equal to the columns of the calling matrix

        :return: the transpose of the calling matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: "Matrix6by3") -> Matrix3D:
        """create a matrix equal to the product of the calling matrix and the argument matrix

        :param mat: matrix to be used in the product
        :type mat: Matrix6by3
        :return: product matrix
        :rtype: Matrix3D
        """
        return Matrix3D(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
        )


class Matrix6by3:
    def __init__(
        self,
        r1: Vector3D,
        r2: Vector3D,
        r3: Vector3D,
        r4: Vector3D,
        r5: Vector3D,
        r6: Vector3D,
    ) -> None:
        """used to perform operations for a 6x3 matrix

        :param r1: first row of the matrix
        :type r1: Vector3D
        :param r2: second row of the matrix
        :type r2: Vector3D
        :param r3: third row of the matrix
        :type r3: Vector3D
        :param r4: fourth row of the matrix
        :type r4: Vector3D
        :param r5: fifth row of the matrix
        :type r5: Vector3D
        :param r6: sixth row of the matrix
        :type r6: Vector3D
        """
        #: first row of the matrix
        self.row1: Vector3D = r1.copy()

        #: second row of the matrix
        self.row2: Vector3D = r2.copy()

        #: third row of the matrix
        self.row3: Vector3D = r3.copy()

        #: fourth row of the matrix
        self.row4: Vector3D = r4.copy()

        #: fifth row of the matrix
        self.row5: Vector3D = r5.copy()

        #: sixth row of the matrix
        self.row6: Vector3D = r6.copy()

    def column_1(self) -> Vector6D:
        """create a vector whose elements equal the first column of the matrix

        :return: first column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.x, self.row2.x, self.row3.x, self.row4.x, self.row5.x, self.row6.x)

    def column_2(self) -> Vector6D:
        """create a vector whose elements equal the second column of the matrix

        :return: second column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.y, self.row2.y, self.row3.y, self.row4.y, self.row5.y, self.row6.y)

    def column_3(self) -> Vector6D:
        """create a vector whose elements equal the third column of the matrix

        :return: third column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.z, self.row2.z, self.row3.z, self.row4.z, self.row5.z, self.row6.z)

    def transpose(self) -> Matrix3by6:
        """create a matrix whose rows equal the columns of the calling matrix

        :return: transpose of the calling matrix
        :rtype: Matrix3by6
        """
        return Matrix3by6(self.column_1(), self.column_2(), self.column_3())

    def multiply(self, mat: Matrix3D) -> "Matrix6by3":
        """create a matrix that is the product of the calling and argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix3D
        :return: product matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            Vector3D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            Vector3D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            Vector3D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_vector(self, vec: "Vector3D") -> Vector6D:
        """create a vector equal to the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: Vector3D
        :return: product vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def multiply_matrix3by6(self, mat: "Matrix3by6") -> "Matrix6D":
        """create a matrix equal to the product of the calling and the argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix3by6
        :return: product matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
            Vector6D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
                self.row4.dot(mat.column_4()),
                self.row4.dot(mat.column_5()),
                self.row4.dot(mat.column_6()),
            ),
            Vector6D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
                self.row5.dot(mat.column_4()),
                self.row5.dot(mat.column_5()),
                self.row5.dot(mat.column_6()),
            ),
            Vector6D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
                self.row6.dot(mat.column_4()),
                self.row6.dot(mat.column_5()),
                self.row6.dot(mat.column_6()),
            ),
        )


class Matrix6D:
    def __init__(
        self,
        r1: Vector6D,
        r2: Vector6D,
        r3: Vector6D,
        r4: Vector6D,
        r5: Vector6D,
        r6: Vector6D,
    ) -> None:
        """used to perform operations for a 6x6 matrix

        :param r1: first row of the matrix
        :type r1: Vector6D
        :param r2: second row of the matrix
        :type r2: Vector6D
        :param r3: third row of the matrix
        :type r3: Vector6D
        :param r4: fourth row of the matrix
        :type r4: Vector6D
        :param r5: fifth row of the matrix
        :type r5: Vector6D
        :param r6: sixth row of the matrix
        :type r6: Vector6D
        """
        #: first row of the matrix
        self.row1: Vector6D = r1.copy()

        #: second row of the matrix
        self.row2: Vector6D = r2.copy()

        #: third row of the matrix
        self.row3: Vector6D = r3.copy()

        #: fourth row of the matrix
        self.row4: Vector6D = r4.copy()

        #: fifth row of the matrix
        self.row5: Vector6D = r5.copy()

        #: sixth row of the matrix
        self.row6: Vector6D = r6.copy()

    @classmethod
    def identity(cls) -> "Matrix6D":
        """create a matrix with a diagonal with elements of 1 and off-diagonal elements of 0

        :return: the identity matrix
        :rtype: Matrix6D
        """
        return cls(
            Vector6D(1, 0, 0, 0, 0, 0),
            Vector6D(0, 1, 0, 0, 0, 0),
            Vector6D(0, 0, 1, 0, 0, 0),
            Vector6D(0, 0, 0, 1, 0, 0),
            Vector6D(0, 0, 0, 0, 1, 0),
            Vector6D(0, 0, 0, 0, 0, 1),
        )

    def diagonal(self) -> Vector6D:
        """create a vector whose elements are equal to the diagonal of the matrix

        :return: vector whose elements equal the diagonal
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.x,
            self.row2.y,
            self.row3.z,
            self.row4.vx,
            self.row5.vy,
            self.row6.vz,
        )

    def multiply_vector(self, vec: Vector6D) -> Vector6D:
        """create a vector equal to the product of the calling matrix and the argument vector

        :param vec: vector to be used in the product
        :type vec: Vector6D
        :return: product vector
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.dot(vec),
            self.row2.dot(vec),
            self.row3.dot(vec),
            self.row4.dot(vec),
            self.row5.dot(vec),
            self.row6.dot(vec),
        )

    def column_1(self) -> Vector6D:
        """create a vector whose elements equal the first column of the matrix

        :return: first column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.x, self.row2.x, self.row3.x, self.row4.x, self.row5.x, self.row6.x)

    def column_2(self) -> Vector6D:
        """create a vector whose elements equal the second column of the matrix

        :return: second column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.y, self.row2.y, self.row3.y, self.row4.y, self.row5.y, self.row6.y)

    def column_3(self) -> Vector6D:
        """create a vector whose elements equal the third column of the matrix

        :return: third column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(self.row1.z, self.row2.z, self.row3.z, self.row4.z, self.row5.z, self.row6.z)

    def column_4(self) -> Vector6D:
        """create a vector whose elements equal the fourth column of the matrix

        :return: fourth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.vx,
            self.row2.vx,
            self.row3.vx,
            self.row4.vx,
            self.row5.vx,
            self.row6.vx,
        )

    def column_5(self) -> Vector6D:
        """create a vector whose elements equal the fifth column of the matrix

        :return: fifth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.vy,
            self.row2.vy,
            self.row3.vy,
            self.row4.vy,
            self.row5.vy,
            self.row6.vy,
        )

    def column_6(self) -> Vector6D:
        """create a vector whose elements equal the sixth column of the matrix

        :return: sixth column of the matrix
        :rtype: Vector6D
        """
        return Vector6D(
            self.row1.vz,
            self.row2.vz,
            self.row3.vz,
            self.row4.vz,
            self.row5.vz,
            self.row6.vz,
        )

    def transpose(self) -> "Matrix6D":
        """create a matrix whose rows equal the columns of the calling matrix

        :return: transpose of the calling matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.column_1(),
            self.column_2(),
            self.column_3(),
            self.column_4(),
            self.column_5(),
            self.column_6(),
        )

    def multiply_matrix_6by3(self, mat: Matrix6by3) -> Matrix6by3:
        """create a matrix equal to the product of the calling and argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix6by3
        :return: product matrix
        :rtype: Matrix6by3
        """
        return Matrix6by3(
            Vector3D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
            ),
            Vector3D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
            ),
            Vector3D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
            ),
            Vector3D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
            ),
            Vector3D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
            ),
            Vector3D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
            ),
        )

    def multiply_matrix(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix equal to the product of the calling and the argument matrices

        :param mat: matrix to be used in the product
        :type mat: Matrix6D
        :return: product matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            Vector6D(
                self.row1.dot(mat.column_1()),
                self.row1.dot(mat.column_2()),
                self.row1.dot(mat.column_3()),
                self.row1.dot(mat.column_4()),
                self.row1.dot(mat.column_5()),
                self.row1.dot(mat.column_6()),
            ),
            Vector6D(
                self.row2.dot(mat.column_1()),
                self.row2.dot(mat.column_2()),
                self.row2.dot(mat.column_3()),
                self.row2.dot(mat.column_4()),
                self.row2.dot(mat.column_5()),
                self.row2.dot(mat.column_6()),
            ),
            Vector6D(
                self.row3.dot(mat.column_1()),
                self.row3.dot(mat.column_2()),
                self.row3.dot(mat.column_3()),
                self.row3.dot(mat.column_4()),
                self.row3.dot(mat.column_5()),
                self.row3.dot(mat.column_6()),
            ),
            Vector6D(
                self.row4.dot(mat.column_1()),
                self.row4.dot(mat.column_2()),
                self.row4.dot(mat.column_3()),
                self.row4.dot(mat.column_4()),
                self.row4.dot(mat.column_5()),
                self.row4.dot(mat.column_6()),
            ),
            Vector6D(
                self.row5.dot(mat.column_1()),
                self.row5.dot(mat.column_2()),
                self.row5.dot(mat.column_3()),
                self.row5.dot(mat.column_4()),
                self.row5.dot(mat.column_5()),
                self.row5.dot(mat.column_6()),
            ),
            Vector6D(
                self.row6.dot(mat.column_1()),
                self.row6.dot(mat.column_2()),
                self.row6.dot(mat.column_3()),
                self.row6.dot(mat.column_4()),
                self.row6.dot(mat.column_5()),
                self.row6.dot(mat.column_6()),
            ),
        )

    def plus(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix whose elements are equal to the sum of the elements in the calling and argument matrices

        :param mat: matrix to be used in the sum
        :type mat: Matrix6D
        :return: sum matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.row1.plus(mat.row1),
            self.row2.plus(mat.row2),
            self.row3.plus(mat.row3),
            self.row4.plus(mat.row4),
            self.row5.plus(mat.row5),
            self.row6.plus(mat.row6),
        )

    def minus(self, mat: "Matrix6D") -> "Matrix6D":
        """create a matrix whose elements are equal to the difference of the elements in the calling and argument matrices

        :param mat: matrix to be used in the difference
        :type mat: Matrix6D
        :return: difference matrix
        :rtype: Matrix6D
        """
        return Matrix6D(
            self.row1.minus(mat.row1),
            self.row2.minus(mat.row2),
            self.row3.minus(mat.row3),
            self.row4.minus(mat.row4),
            self.row5.minus(mat.row5),
            self.row6.minus(mat.row6),
        )
