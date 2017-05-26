goals = [
    "is 10 years younger or older than you",
    "is writing code in a language you are unfamiliar with",
    "is writing code in a language you are familiar with",
    "works in a subfield of programming you are unfamiliar with",
    "works in a subfield of programming you are familiar with",
    "is learning about something you have experience with",
    "is learning about something you don't have experience with",
    "is not from the Americas",
    "is from the Americas",
    "is from the US",
    "is a New Yorker",
    "is working in an OOP framework",
    "is working in a functional framework",
    "is from academia",
    "worked for a large company",
    "worked for a startup",
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
    "Hatchling butterfly",
    "Butterfly in bloom",
    "Social butterfly"
]

worktypes = [
    "I shared a desk with",
    "I paired with"
]

def get_level_by_score(score):
    for i, level in enumerate(levels):
        upper_bound = len(goals) * i / (len(levels) - 1)

        if score <= upper_bound:
            return level
