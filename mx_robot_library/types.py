import re
from ipaddress import IPv4Address
from typing import TYPE_CHECKING, Union

from pydantic import ConstrainedStr
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class Localhost(ConstrainedStr):
    strip_whitespace = True
    to_upper = False
    to_lower = False
    regex = re.compile(r"^localhost$|^127\.0\.0\.1$")
    strict = False


class Domain(ConstrainedStr):
    strip_whitespace = True
    to_upper = False
    to_lower = False
    min_length = 1
    max_length = 253
    regex = re.compile(
        r"^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|"
        r"([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\."
        r"([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$"
    )
    strict = False


class IPv4AddressStr(str):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, bytes, int]) -> str:
        return str(IPv4Address(value))


HostAddress: TypeAlias = Union[Localhost, Domain, IPv4AddressStr]
