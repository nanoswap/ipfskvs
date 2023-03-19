import subprocess

def read(filename, reader):
    
    # download the data
    result = subprocess.run(["ipfs", "files", "read", "/data/" + filename], capture_output=True)

    # parse the data
    data = result.stdout.strip()
    reader.ParseFromString(data)
    return reader

def write(filename, data):

    # write data to a local file
    filepath = "generated/tmp/" + filename
    with open(filepath, "wb") as f:
        f.write(data)

    # upload that file
    subprocess.run(["ipfs", "add", filepath, "--to-files", "/data/"], capture_output=True)

    # remove the temporary file
    subprocess.run(["rm", filepath])
