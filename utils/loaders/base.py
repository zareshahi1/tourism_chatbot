from abc import ABC, abstractmethod

class BaseLoader(ABC):
    """کلاس پایه برای همه‌ی لودرها"""

    @abstractmethod
    def load(self, path: str = None, text: str = None) -> str:
        """باید متن استاندارد برگرداند"""
        pass
