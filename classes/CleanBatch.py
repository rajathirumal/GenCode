from dataclasses import dataclass, field


@dataclass
class Batch:
    batch_number: int
    batch_metrics: dict = field(repr=False)
    batch_folder_count: int
    batch_py_files: int
