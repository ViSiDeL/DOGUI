def ade1():
    # Set sole plate (sp) variables.
    sp_length = input("Set sole plate length (IN DECIMAL FEET): ")

    stud_space = float(input("Set center-to-center distance between studs (1.5' or 2') : "))
    while stud_space != 1.5 and stud_space != 2:
        print("\nNo, dummy, wrong value. Enter number with no units.")
        stud_space = float(input("Set center-to-center distance between studs (1.5' or 2') : "))

    while float(sp_length) > 90:
        print("\nNo, dummy, that's too big. Enter number with no units.")
        sp_length = input("Set sole plate length (IN DECIMAL FEET): ")

    number_of_studs = (float(sp_length) - 0.1667) / stud_space
    save_number_of_studs = number_of_studs
    number_of_studs += 1

    number_of_studs = round(number_of_studs)

    sp_thickness = 0.1667
    sp_elev = 0
    sp_width = "0.25"

    set_limits = f"{round(float(sp_length) + 20, 2):.4f}"
    upper_limits = f"{set_limits},{set_limits}"

    ade2(sp_thickness, sp_elev, sp_length, sp_width, set_limits, upper_limits)

def ade2(sp_thickness, sp_elev, sp_length, sp_width, set_limits, upper_limits):
    # Set up drawing parameters.
    command("LIMITS", "0,0", upper_limits)

    set_limits_float = float(set_limits)
    if set_limits_float <= 30:
        set_grid = "1"
    elif 30 < set_limits_float <= 50:
        set_grid = "2"
    elif 50 < set_limits_float <= 100:
        set_grid = "5"

    command("GRID", set_grid)

    # Set up start point according to sole plate size.
    start_pt_y = (- (set_limits_float / 2) - 0.125)
    start_pt_x = 5
    start_pt = [start_pt_x, start_pt_y]

    # Begin drawing sole plate.
    command("ELEV", sp_elev, sp_thickness)
    command("PLINE", start_pt, f"@{sp_length}<0", f"@{sp_width}<90", f"@{sp_length}<180", "close")

    # Set up start point for leader.
    star_pt_y = (- (set_limits_float / 2) - 0.0625)
    star_pt_x = start_pt_x + float(sp_length)
    star_pt = [star_pt_x, star_pt_y]

    command("ELEV", "0", "0")
    command("DIM", "LEADER", star_pt, f"@2.345<0", "", "2 x 4 WOOD STUD SYSTEM", "EXIT")

    # Set up view point.
    command("GRID", "OFF")
    command("VPOINT", "2,-2,2")
    command("ZOOM", "ALL")

def command(*args):
    # Placeholder for the actual command function
    print("Command executed:", args)

if __name__ == "__main__":
    ade1()