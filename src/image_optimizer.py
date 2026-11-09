"""Image optimization helpers for Open Design Toolkit."""
from pathlib import Path
from PIL import Image

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def optimize_image(source: Path, destination: Path, jpeg_quality: int = 85) -> Path:
    """Optimize one PNG or JPEG into destination; never modify source."""
    source = Path(source)
    destination = Path(destination)
    suffix = source.suffix.lower()

    if suffix not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(f"Unsupported image format: {suffix}")
    if not 1 <= int(jpeg_quality) <= 95:
        raise ValueError("JPEG quality must be between 1 and 95.")

    destination.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(source) as image:
        if suffix == ".png":
            image.save(destination, format="PNG", optimize=True)
        else:
            if image.mode not in ("RGB", "L"):
                image = image.convert("RGB")
            image.save(
                destination,
                format="JPEG",
                quality=int(jpeg_quality),
                optimize=True,
                progressive=True,
            )
    return destination


def optimize_folder(source_folder: Path, output_folder: Path, jpeg_quality: int = 85):
    """Optimize supported images directly inside a folder (not subfolders)."""
    source_folder = Path(source_folder)
    output_folder = Path(output_folder)
    if not source_folder.is_dir():
        raise NotADirectoryError(source_folder)

    output_folder.mkdir(parents=True, exist_ok=True)
    results = []
    for source in sorted(source_folder.iterdir()):
        if source.is_file() and source.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS:
            destination = output_folder / source.name
            optimize_image(source, destination, jpeg_quality)
            results.append(destination)
    return results
