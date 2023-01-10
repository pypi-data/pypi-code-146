class HummingbirdJoystickCalculator:
    NOT_MOVING_WINDOW_SIZE = 20.0
    STRAIGHT_WINDOW_SIZE = 25.0
    FORWARD_TURN_MULTIPLIER = 0.75
    BACKWARD_TURN_MULTIPLIER = 0.33
    BACKWARD_TURN_MULTIPLIER = 0.75

    def straight_back(self, speed, x, y):
        return(-speed, -speed)

    def straight_forward(self, speed, x, y):
        return(speed, speed)

    def left_back(self, speed, x, y):
        return(-speed * HummingbirdJoystickCalculator.BACKWARD_TURN_MULTIPLIER, -speed)

    def left_forward(self, speed, x, y):
        return(-speed * HummingbirdJoystickCalculator.FORWARD_TURN_MULTIPLIER, speed)

    def right_back(self, speed, x, y):
        return(-speed, -speed * HummingbirdJoystickCalculator.BACKWARD_TURN_MULTIPLIER)

    def right_forward(self, speed, x, y):
        return(speed, -speed * HummingbirdJoystickCalculator.FORWARD_TURN_MULTIPLIER)

    def speeds(self, x, y):
        speed = max(abs(x), abs(y))

        if speed < HummingbirdJoystickCalculator.NOT_MOVING_WINDOW_SIZE:
            return(0, 0)

        if abs(x) <= HummingbirdJoystickCalculator.STRAIGHT_WINDOW_SIZE:
            if y > 0:
                # straight forward
                return(self.straight_forward(speed, x, y))
            else:
                # straight back
                return(self.straight_back(speed, x, y))
        elif x < 0:
            if y < 0:
                # left back
                return(self.left_back(speed, x, y))
            else:
                # left forward
                return(self.left_forward(speed, x, y))
        else:
            if y < 0:
                # right back
                return(self.right_back(speed, x, y))
            else:
                # right forward
                return(self.right_forward(speed, x, y))

        return(0, 0)
