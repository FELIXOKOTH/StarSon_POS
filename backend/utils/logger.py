def log(message):
    with open("import_log.txt", "a") as file:
        file.write(message + "\n")
