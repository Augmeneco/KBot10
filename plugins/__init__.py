import os
__all__ = [i.split('.')[0] for i in os.listdir('plugins') if os.path.isfile(f'plugins/{i}')]