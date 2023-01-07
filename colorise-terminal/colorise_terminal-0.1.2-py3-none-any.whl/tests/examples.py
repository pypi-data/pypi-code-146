from colorise_terminal import cprint


def print_examples():
    cprint("No text color; no background; no bold", bold=False)
    cprint("No text color; no background; bold", bold=True)
    cprint("Green text; no background; no bold", text_color="#33DD44")
    cprint("Green text; no background; bold", text_color="#33DD44", bold=True)
    cprint("White text; pink background; no bold", text_color="#EEEEEE", bg_color="#EE4488")
    cprint("White text; pink backgroud; bold", text_color="#EEEEEE", bg_color="#EE4488", bold=True)
    cprint("Blue text; pink background; no bold", text_color="#2233DD", bg_color="#EE4488")
    cprint("Blue text; pink backgroud; bold", text_color="#2233DD", bg_color="#EE4488", bold=True)
    cprint("Red text; white background; no bold", text_color="#FF0000", bg_color="#EEFFFF")
    cprint("Red text; white background; bold", text_color="#FF0000", bg_color="#EEFFFF", bold=True)


if __name__ == "__main__":
    print_examples()
