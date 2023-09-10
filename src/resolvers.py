from typing import TYPE_CHECKING, Optional, Union, Any

from src.enums import PlayerAction
from src.service import Service
from src.utils import casefold_equals, casefold_in, enum_get
from src.object.base import Object

if TYPE_CHECKING:
    from src.containers import CustomContainer, Services, Objects, Items
    from src.command import Command
    from src.object.base import Item


class Resolver:
    def __init__(self, container: type["CustomContainer"]):
        self.container = container


class ObjectResolver(Resolver):
    def __init__(self, container: Union[type["Objects"], type["Items"]]):
        super().__init__(container)

    def resolve(self, object_: Union[str, type["Object"]]) -> Optional["Object"]:
        """Returns the object with the given name."""
        for k, v in self.container.members().items():
            v = v()
            resolved = self._resolve_by_str(object_, k, v)
            resolved = resolved or self._resolve_by_object_type(object_, v)
            if resolved:
                return resolved

    @staticmethod
    def _resolve_by_str(object_: Any, k: Any, v: Any) -> Optional["Object"]:
        if not isinstance(object_, str):
            return
        if casefold_equals(object_, k):
            return v
        if hasattr(v, "name") and casefold_equals(object_, v.name):
            return v
        if hasattr(v, "_references") and casefold_in(object_, v._references):
            return v

    @staticmethod
    def _resolve_by_object_type(object_: Any, v: Any) -> Optional["Object"]:
        if not type(object_) is type:
            return
        if not issubclass(type(v), Object):
            return
        if v is object_:
            return v
        if isinstance(v, object_):
            return v


class ItemResolver(ObjectResolver):
    def __init__(self, container: type["Items"]):
        super().__init__(container)


class ServiceResolver(Resolver):
    def __init__(self, container: type["Services"], objects_r: ObjectResolver):
        self._objects_r = objects_r
        super().__init__(container)

    def resolve(self, object_: Union["Object", "Item"]) -> Optional["Service"]:
        """Returns the service with related to an object with the given name or
        serving the passed object class"""
        for k, v in self.container.members().items():
            v = v()
            resolved = self._resolve_by_object_type(object_, v)
            if resolved:
                return resolved

    @staticmethod
    def _resolve_by_object_type(object_: Union["Object", "Item"], v: Any) -> Optional["Object"]:
        type_ = object_
        if not isinstance(object_, type):
            type_ = type(object_)
        if type_ is v.object_type:
            return v


class CommandObjectResolver:
    def __init__(self, items_r: ItemResolver, objects_r: ObjectResolver):
        self._resolvers = [items_r, objects_r]

    def resolve(self, object_: Union[str, "Item", "Object"]) -> Optional[Union["Item", "Object"]]:
        return self._resolve_with_resolvers(object_)

    def resolve_command(self, command: "Command") -> "Command":
        command.action = enum_get(command.action_str, PlayerAction)
        command.preposition = enum_get(command.preposition_str, PlayerAction)
        command.object = self._resolve_with_resolvers(command.object_str or "")
        command.preposition_object = self._resolve_with_resolvers(
            command.preposition_object_str or ""
        )
        return command

    def _resolve_with_resolvers(self, object_: str) -> Optional[Union["Item", "Object"]]:
        for resolver in self._resolvers:
            resolved_object = resolver.resolve(object_)
            if resolved_object:
                return resolved_object
