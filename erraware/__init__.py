import functools
from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import Any, Never, Self, cast, reveal_type


class UnwrapError(TypeError):
    pass


class Result[T, E]:
    def unwrap(self) -> T:
        raise UnwrapError("unwrap() on Err")

    def unwrap_err(self) -> E:
        raise UnwrapError("unwrap_err() on Ok")

    def __iter__(self) -> Generator[Self, None, T]:
        yield self
        return self.unwrap()


@dataclass(slots=True)
class Ok[T](Result[T, Never]):
    value: T

    def unwrap(self) -> T:
        return self.value


@dataclass(slots=True)
class Err[E](Result[Never, E]):
    err: E

    def unwrap_err(self) -> E:
        return self.err


type ResultFn[T, E] = Generator[Result[Any, E], None, Result[T, E]]


def might_fail[**P, T, E](
    f: Callable[P, ResultFn[T, E] | Result[T, E]],
) -> Callable[P, Result[T, E]]:
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T, E]:
        gener = f(*args, **kwargs)
        if isinstance(gener, Result):
            return gener
        while True:
            try:
                item = gener.send(None)
            except StopIteration as e:
                return cast(Result[T, E], e.value)
            else:
                if isinstance(item, Err):
                    return item

    return wrapper

