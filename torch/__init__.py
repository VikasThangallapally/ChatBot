"""
Minimal, pure-Python shim for `torch` to prevent import errors when PyTorch
is not installed. This provides a very small subset of the API used by
libraries that only import `torch` but do not actually require GPU/Autograd.

NOTE: This is a compatibility shim — it does NOT implement full PyTorch.
If your application requires real PyTorch behavior (training, GPU, autograd),
install PyTorch instead.
"""

from types import SimpleNamespace
import numpy as np

__all__ = [
    "__version__",
    "Tensor",
    "tensor",
    "from_numpy",
    "as_tensor",
    "device",
    "cuda",
    "is_available",
    "no_grad",
    "nn",
]

__version__ = "0.0.0-stub"


def is_available():
    return False


class Tensor:
    """A minimal Tensor wrapper around numpy arrays providing a few helpers."""

    def __init__(self, data):
        self._arr = np.asarray(data)

    def numpy(self):
        return self._arr

    def to(self, *args, **kwargs):
        return self

    def cpu(self):
        return self

    def shape(self):
        return self._arr.shape

    def __repr__(self):
        return f"Tensor(shape={self._arr.shape}, dtype={self._arr.dtype})"

    # basic operations delegated to numpy arrays
    def __add__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self._arr + other._arr)
        return Tensor(self._arr + other)

    def __sub__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self._arr - other._arr)
        return Tensor(self._arr - other)

    def __mul__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self._arr * other._arr)
        return Tensor(self._arr * other)

    def __truediv__(self, other):
        if isinstance(other, Tensor):
            return Tensor(self._arr / other._arr)
        return Tensor(self._arr / other)


def tensor(data, dtype=None, device=None):
    return Tensor(data)


def from_numpy(ndarray):
    return Tensor(np.asarray(ndarray))


def as_tensor(data):
    return Tensor(data)


class _CudaStub:
    def is_available(self):
        return False


cuda = _CudaStub()


class _NoGrad:
    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc, tb):
        return False


def no_grad():
    return _NoGrad()


def device(name_or_obj):
    # simple placeholder
    return str(name_or_obj)


# Provide a minimal `nn` namespace implemented in torch/nn/__init__.py
try:
    from . import nn  # type: ignore
except Exception:
    nn = SimpleNamespace()

# small convenience alias
save = None
load = None
