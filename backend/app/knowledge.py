from pathlib import Path

ALLOWED_SUFFIXES = {".md", ".txt"}


def load_knowledge(directory: Path) -> str:
    """Concatena los archivos .md/.txt del directorio, ordenados por nombre."""
    if not directory.is_dir():
        return ""
    parts = []
    for path in sorted(directory.iterdir()):
        if path.is_file() and path.suffix.lower() in ALLOWED_SUFFIXES:
            content = path.read_text(encoding="utf-8").strip()
            if content:
                parts.append(f'<documento nombre="{path.name}">\n{content}\n</documento>')
    return "\n\n".join(parts)


def build_system_prompt(base_prompt: str, directory: Path) -> str:
    knowledge = load_knowledge(directory)
    if not knowledge:
        return base_prompt
    return f"{base_prompt}\n\n<conocimiento>\n{knowledge}\n</conocimiento>"
