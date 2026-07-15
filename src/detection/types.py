from dataclasses import dataclass

# This class represents a bounding box with coordinates (x1, y1) for the top-left corner and (x2, y2) for the bottom-right corner.
@dataclass(slots=True)
class BoundingBox:

    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1 # Width of the bounding box

    @property
    def height(self) -> int:
        return self.y2 - self.y1 # Height of the bounding box

    @property
    def area(self) -> int:
        return self.width * self.height # Area of the bounding box

    @property
    def center(self) -> tuple[int, int]:
        return (
            self.x1 + self.width // 2,
            self.y1 + self.height // 2,
        ) # Center coordinates of the bounding box

    # This method returns the bounding box coordinates in the format [x1, y1, x2, y2]
    def as_xyxy(self) -> list[int]:

        return [
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        ]