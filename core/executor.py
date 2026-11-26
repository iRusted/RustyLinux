import subprocess 

command = input("What Command do you wish to run >")


result = subprocess.run(
    [f"{command}"],
    capture_output=True,
    text=True
)

print(result.stdout)