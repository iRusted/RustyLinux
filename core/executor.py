import subprocess
import shlex

command = input("What command do you wish to run > ")

result = subprocess.run(
    shlex.split(command),
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)