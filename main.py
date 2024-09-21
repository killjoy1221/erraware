import random
from dataclasses import dataclass

from erraware import Err, Ok, might_fail


@dataclass
class MyError:
    code: int
    message: str


@dataclass
class SomeError:
    message: str


@might_fail
def do_random():
    if (num := random.randint(0, 5)) > 0:
        return Ok(num)

    return Err(SomeError("random error"))


@might_fail
def test():
    value = yield from (do_random)()
    if value == 1:
        return Err(MyError(0, "Nope"))
    return Ok(value + 1)


def main() -> None:
    match test():
        case Ok(value):
            print(f"Success!: {value}")
        case Err(MyError(code, message)):
            print(f"My Error: {code} - {message}")
        case Err(SomeError(message)):
            print(f"Some Error: {message}")


if __name__ == "__main__":
    main()
