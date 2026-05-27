import datetime


def calculate_next(
    interval: int, repetitions: int, rating: str
) -> tuple[float, int, str]:
    match rating:
        case "bad":
            new_interval = 1
            new_repetitions = 0
        case "normal":
            new_interval = interval
            new_repetitions = repetitions + 1
        case "good":
            new_interval = interval * 2
            new_repetitions = repetitions + 1
        case "easy":
            new_interval = interval * 3
            new_repetitions = repetitions + 1
        case _:
            return None

    new_interval = max(1, new_interval)
    next_review = datetime.datetime.now() + datetime.timedelta(hours=new_interval)
    next_review_iso = next_review.strftime("%Y-%m-%d %H:%M:%S")

    return (new_interval, new_repetitions, next_review_iso)


if __name__ == "__main__":
    print(calculate_next(1, 0, "bad"))
    print(calculate_next(1, 1, "normal"))
    print(calculate_next(2, 2, "good"))
    print(calculate_next(4, 3, "good"))
    print(calculate_next(12, 4, "easy"))
    print(calculate_next(36, 5, "easy"))
