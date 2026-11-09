"""Safe batch-renaming helpers."""
from pathlib import Path


def build_rename_plan(folder: Path, prefix: str, start_number: int = 1, width: int = 3):
    """Return (source, destination) pairs without changing any files."""
    folder = Path(folder)
    if not folder.is_dir():
        raise NotADirectoryError(folder)
    if not prefix.strip():
        raise ValueError("Prefix cannot be empty.")
    if start_number < 0 or width < 1:
        raise ValueError("Starting number must be zero or greater and width must be positive.")

    candidates = sorted(p for p in folder.iterdir() if p.is_file())
    plan = []
    for index, source in enumerate(candidates, start=start_number):
        number = str(index).zfill(width)
        destination = folder / f"{prefix}{number}{source.suffix.lower()}"
        if source != destination:
            plan.append((source, destination))

    sources = {src.resolve() for src, _ in plan}
    destinations = [dst.resolve() for _, dst in plan]
    if len(destinations) != len(set(destinations)):
        raise FileExistsError("The rename plan contains duplicate destination names.")
    for destination in destinations:
        if destination.exists() and destination not in sources:
            raise FileExistsError(f"Destination already exists: {destination.name}")
    return plan


def apply_rename_plan(plan):
    """Apply a validated rename plan, using temporary names to avoid collisions."""
    plan = list(plan)
    if not plan:
        return []

    sources = {src.resolve() for src, _ in plan}
    for _, destination in plan:
        if destination.exists() and destination.resolve() not in sources:
            raise FileExistsError(f"Destination already exists: {destination.name}")

    temporary = []
    for index, (source, destination) in enumerate(plan):
        temp = source.with_name(f".odt_tmp_{index}_{source.name}")
        if temp.exists():
            raise FileExistsError(f"Temporary path already exists: {temp.name}")
        source.rename(temp)
        temporary.append((temp, destination))

    completed = []
    try:
        for temp, destination in temporary:
            temp.rename(destination)
            completed.append(destination)
    except Exception:
        # Best-effort rollback for files that have not reached their final name.
        for temp, destination in temporary[len(completed):]:
            if temp.exists():
                temp.rename(plan[len(completed)][0])
                completed.append(None)
        raise
    return [destination for destination in completed if destination is not None]
