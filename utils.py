
def read_text_file(file_name: str, mode: str = "r", encoding: str = "utf-8") -> set:
    try:
        with open(file_name, mode, encoding=encoding) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()


def is_fresh_resource(resource_id: str, published_ids: set) -> bool:
    if resource_id not in published_ids:
        return True
    return False


def track_published(resource_id: str, filename: str, encoding: str = "utf-8"):
    with open(filename,'a', encoding=encoding) as f:
        f.write(resource_id + '\n')