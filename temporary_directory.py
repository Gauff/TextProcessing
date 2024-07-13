class TemporaryDirectoryManager:
    def __init__(self):
        self.temp_dir = None

    def create_temp_directory(self):
        """Create a temporary directory and return its path."""
        if self.temp_dir is None:
            import tempfile
            self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir

    def remove_temp_directory(self):
        """Remove the temporary directory if it exists."""
        if self.temp_dir is not None:
            import shutil
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None

# Example usage:
# temp_dir_manager = TemporaryDirectoryManager()
# temp_path = temp_dir_manager.create_temp_directory()
# print(f"Temporary directory created at: {temp_path}")
# temp_dir_manager.remove_temp_directory()
# print("Temporary directory removed.")
