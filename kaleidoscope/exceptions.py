class KaleidoscopeError(Exception):
    """Base class for all exceptions in Kaleidoscope"""
    pass

class RenderError(KaleidoscopeError):
    """Something went wrong in the rendering system"""
    pass
