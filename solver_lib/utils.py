class Utils:
    def calculate_gcd(value1, value2):
        if value1 == 0:
            return value2
        elif value2 == 0:
            return value1
        else:
            return Utils.calculate_gcd(value2, value1 % value2)

    def calculate_lcm(value1, value2):
        gcd = Utils.calculate_gcd(value1, value2)
        return (value1 * value2) / gcd
