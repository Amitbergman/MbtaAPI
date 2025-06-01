from dataclasses import dataclass

# Model that is representing subway route
@dataclass
class Route:
    id: str
    full_name: str

# Model that is representing a subway stop
@dataclass
class Stop:
    id: str
    name: str