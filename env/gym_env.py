import os
import subprocess
import tempfile

class CodingGymEnv:
    def __init__(self, task_data):
        self.task = task_data
        self.current_code = task_data["buggy_code"]

    def reset(self):
        self.current_code = self.task["buggy_code"]
        return self.current_code

    def step(self, proposed_code):
        self.current_code = proposed_code
        
        # Create a temporary file to execute test cases
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
            combined_script = f"{proposed_code}\n\n{self.task['test_code']}"
            temp_file.write(combined_script)
            temp_file_path = temp_file.name

        try:
            # Run pytest in isolated process
            result = subprocess.run(
                ["pytest", temp_file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            passed = result.returncode == 0
            reward = 1.0 if passed else 0.0
            logs = result.stdout if result.stdout else result.stderr
        except Exception as e:
            passed = False
            reward = 0.0
            logs = str(e)
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return proposed_code, reward, passed, logs
