import subprocess
import shlex

username = "rustylinuxtest"

command = input("What command do you wish to run > ")

result = subprocess.run(
    ["runuser", "-u", username, "--", *command],
    capture_output=True,
    text=True
)

print(result.stdout)
