# Open Design Toolkit

An open-source desktop toolkit for designers to optimize images and batch-rename design assets.

## Current features

- Batch image optimization for PNG and JPEG files.
- Batch file renaming with a preview before changes are applied.
- Keeps original files unchanged when optimizing images (saves results in an `optimized` folder).
- Simple desktop interface built with Python and Tkinter.

## Project status

**Early development (v0.1.0).** This is a starter project. Test it with copies of your files before using it in an important production workflow. Features and supported formats may change.

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10 or newer
- Pillow (installed from `requirements.txt`)
- Tkinter (usually included with standard Python installations)

## Installation

1. Install Python 3.10 or newer from [python.org](https://www.python.org/downloads/).
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Create and activate a virtual environment:

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the application

```bash
python -m src.main
```

## How to use

### Optimize images

1. Open the application and choose **Image Optimizer**.
2. Select a folder containing PNG or JPEG images.
3. Choose an output folder (or use the default `optimized` folder).
4. Set JPEG quality and click **Optimize images**.
5. Review the output files. Your originals are not modified.

PNG optimization uses Pillow's lossless optimization option. JPEG optimization uses the selected quality setting.

### Batch rename

1. Choose **Batch Renamer**.
2. Select a folder.
3. Enter a filename prefix and starting number.
4. Review the proposed names in the preview.
5. Click **Rename files** only after checking the preview.

The renamer works on files in the selected folder and refuses to overwrite an existing destination.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Supported formats

- Image optimizer: `.png`, `.jpg`, `.jpeg`
- Batch renamer: all files in the selected folder (does not rename subfolders)

## Roadmap

- [ ] Add SVG file information and organization tools
- [ ] Add drag-and-drop support
- [ ] Add more image formats after testing
- [ ] Add packaging instructions for a Windows executable
- [ ] Improve accessibility and localization

## Contributing

Contributions, bug reports, and feature suggestions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. For bugs, use the Bug Report issue template.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

This project is provided "as is", without warranty. Always keep backups of important files and verify optimized outputs before using them commercially.
