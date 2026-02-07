"""
Minimal `torch.nn` shim: provides a `Module` base class and minimal helpers
so code that imports `torch.nn` and defines models does not crash on import.
This is intentionally small and not a substitute for real PyTorch.
"""

class Module:
    def __init__(self):
        pass

    def to(self, *args, **kwargs):
        return self

    def eval(self):
        return self

    def train(self, mode=True):
        return self

    def parameters(self):
        return []


class Sequential(Module):
    def __init__(self, *layers):
        super().__init__()
        self.layers = list(layers)

    def __call__(self, x):
        out = x
        for l in self.layers:
            if callable(l):
                out = l(out)
        return out


# Common layers placeholders
class Identity(Module):
    def __call__(self, x):
        return x


def flatten(x):
    return x


# expose a small API
__all__ = ["Module", "Sequential", "Identity", "flatten"]
