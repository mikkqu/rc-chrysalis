goals = [
    "is 10 years younger or older than you",
    "is writing code in a language you are unfamiliar with",
    "is writing code in a language you are familiar with",
    "is studying a subfield of programming you are unfamiliar with",
    "is studying a subfield of programming you are familiar with",
    "is beginning to learn about something you have experience with",
    "is international (not American)",
    "is American (not New Yorker)",
    "is New Yorker",
    "is working in an OOP framework",
    "is working in a functional framework",
    "is from academia",
    "is from industry",
    "is in a different batch",
    "does not have a CS undergrad",
    "has never worked as a programmer",
    "is from a rural area",
    "learned to program more than 10 years ago",
    "learned to program less than 2 years ago",
    "has contributed to a tool you use",
    "is a returner",
    "is an alum"
]

levels = [
    "Egg",
    "Larva",
    "Caterpillar",
    "Cocoon",
    "Hatching butterfly",
    "Wet butterfly",
    "Glory butterfly",
    "Social butterfly"
]

def get_level_by_score(score):
    if score in range(0, 3):
        return levels[0]
    elif score in range(3, 7):
        return levels[1]
    elif score in range (7, 11):
        return levels[2]
    elif score in range(11, 14):
        return levels[3]
    elif score in range (14, 17):
        return levels[4]
    elif score in range(17, 19):
        return levels[5]
    elif score in range(19, 21):
        return levels[6]
    elif score == 22:
        return levels[7]