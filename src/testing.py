import subprocess

tex = r"This is some basic tex ! \int_c x^2 dx !"

cmd = ["./parser", tex]

subprocess.run(cmd)