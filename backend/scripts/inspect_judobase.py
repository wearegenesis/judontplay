import asyncio
import inspect

import judobase
from judobase import JudoBase


def list_classes() -> list[str]:
    return [name for name, obj in inspect.getmembers(judobase, inspect.isclass) if obj.__module__.startswith("judobase")]


def list_judobase_methods() -> list[str]:
    return [name for name, fn in inspect.getmembers(JudoBase, inspect.isfunction) if not name.startswith("_")]


async def demo_competition_by_id(competition_id: int = 2653):
    try:
        async with JudoBase() as api:
            competition = await api.competition_by_id(competition_id)
            city = getattr(competition, "city", None)
            name = getattr(competition, "name", None)
            print(f"competition_by_id({competition_id}) OK -> name={name}, city={city}")
    except Exception as exc:
        print(f"competition_by_id({competition_id}) failed: {exc}")


if __name__ == "__main__":
    print("Classes in judobase:")
    for c in list_classes():
        print(f"- {c}")

    print("\nPublic methods in JudoBase:")
    for m in list_judobase_methods():
        print(f"- {m}")

    print("\nDemo call:")
    asyncio.run(demo_competition_by_id())
