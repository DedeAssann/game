"""
The transformation functions have been transferred from the main file, to this one
"""


def transform(self, xvar, yvar):
    "the main transform"
    # return transform2d(xvar, yvar)
    return transform_perspective(self, xvar, yvar)


def transform2d(self, xvar, yvar):
    "the transform in 2 dimensions function"
    return int(xvar), int(yvar)


def transform_perspective(self, xvar, yvar):
    "this function transforms"
    lin_y = yvar * self.perspective_point_y / self.height
    if lin_y > self.perspective_point_y:
        lin_y = self.perspective_point_y

    diff_x = xvar - self.perspective_point_x
    diff_y = self.perspective_point_y - lin_y
    factor_y = diff_y / self.perspective_point_y
    factor_y = pow(factor_y, 4)

    tr_x = self.perspective_point_x + diff_x * factor_y
    tr_y = self.perspective_point_y - factor_y * self.perspective_point_y

    return int(tr_x), int(tr_y)
