from enum import Enum

class Source(Enum):
    quasarzone = "quasarzone"
    fmkorea = "fmkorea"

    @property
    def hotdeal_id_header(self) -> str:
        hs = {
            "quasarzone": "QZ",
            "fmkorea": "FM"
        }

        return hs[self.value]