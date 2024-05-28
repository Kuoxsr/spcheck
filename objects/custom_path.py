import pathlib


class CPath(pathlib.Path):
    def __init__(self, *args):
        super().__init__(*args)

        self.is_symbolic_link = False
        self.target_path = None

        # If the path is a symlink, store its target
        # If it cannot be resolved, target is none
        if self.is_symlink():
            self.is_symbolic_link = True
            try:
                self.target_path = self.resolve()
            except FileNotFoundError:
                self.target_path = None

    # def __new__(cls, *args, **kwargs):
    #     self = super().__new__(cls, *args, **kwargs)
    #
    #     self.is_symbolic_link = False
    #     self.target_path = None
    #
    #     # If the path is a symlink, store its target
    #     # If it cannot be resolved, target is none
    #     if self.is_symlink():
    #         self.is_symbolic_link = True
    #         try:
    #             self.target_path = self.resolve()
    #         except FileNotFoundError:
    #             self.target_path = None
    #
    #     return self
