from dataclasses import dataclass as _dataclass

frozen_slots_dataclass = _dataclass(frozen=True, slots=True)
