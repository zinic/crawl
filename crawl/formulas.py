GM_ONLY = "gm_only"


# Costs start at 4 and go up from there by 2
def damage_value_cost(dmg):
    return (dmg - 4) / 2


# cost = number of dice + damage value cost
def damage_cost(value):
    num_st, die_st = value.split('d')

    num = int(num_st)
    die = int(die_st)

    damage_value = num * die
    return num + damage_value_cost(damage_value)


def damage_resistance_cost(value):
    return 100


def base_difficulty_cost(value):
    if value == GM_ONLY:
        # The default base difficulty is currently 10, so
        # returning 2 for the cost is the same cost as 10
        return 2

    valint = int(value)    
    return -1 * (valint - 15) / 2
