from src import ipfs
from unittest.mock import patch, Mock, MagicMock, call, mock_open
from google.protobuf.message import Message
import os

@patch('subprocess.run')
def test_mkdir(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.mkdir` function """

    # Define the expected directory name
    directory_name = "test_directory"

    # Define the expected command and output of the subprocess
    expected_command = ["ipfs", "files", "mkdir", directory_name]
    mock_subprocess.return_value.stdout = b""

    # Call the mkdir() function with the expected directory name
    ipfs.mkdir(directory_name)

    # Assert that the subprocess was called with the expected command
    mock_subprocess.assert_called_once_with(expected_command)

@patch('subprocess.run')
def test_read(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.read` function """

    # Define the expected filename and file contents
    filename = "test.txt"
    file_contents = b"This is a test file."

    # Define the expected command and output of the subprocess
    expected_command = ["ipfs", "files", "read", f"{ipfs.IPFS_HOME}/{filename}"]
    mock_subprocess.return_value.stdout = file_contents

    # Call the read() function with the mock Message object
    result = ipfs.read(filename)

    # Assert that the subprocess was called with the expected command
    mock_subprocess.assert_called_once_with(expected_command, capture_output=True)

    # Assert that the read() function returned the mock Message object
    assert result == file_contents

@patch('subprocess.run')
@patch('builtins.open', mock_open())
def test_write(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.write` function """

    filename = "test_write.txt"
    data = b"some contents"

    # Mock subprocess to check if the command is called
    mock_subprocess.return_value.stdout.decode.return_value = ""
    mock_subprocess.return_value.stderr.decode.return_value = ""

    # Call the function to update the file
    ipfs.write(filename, data)

    # Check if the subprocess is called with the expected arguments
    mock_subprocess.assert_has_calls([
        call(["ipfs", "files", "write", "-t", f"{ipfs.IPFS_HOME}/{filename}", f"src/generated/tmp/{filename}"], capture_output=True),
        call(["rm", f"src/generated/tmp/{filename}"])
    ])

@patch('subprocess.run')
def test_add(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.add` function """

    # Mock the data for the protobuf object
    file_contents = b"some contents"

    # Call the function
    filename = "data/test.txt"
    ipfs.add(filename, file_contents)

    # Check the calls to subprocess.run
    mock_subprocess.assert_has_calls([
        call(["ipfs", "files", "mkdir", "-p", f"{ipfs.IPFS_HOME}/data"]),
        call(["ipfs", "add", "-r", f"src/generated/tmp/{filename}", "--to-files", f"{ipfs.IPFS_HOME}/{filename}"], capture_output=True),
        call(["rm", f"src/generated/tmp/{filename}"])
    ])

@patch('subprocess.run')
def test_does_file_exist(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.does_file_exist` function """

    # Case where file exists
    mock_subprocess.return_value.stdout.decode.return_value = "NumLinks: 1\nBlockSize: 12\nType: file\n"
    assert ipfs.does_file_exist("existing_file.txt") == True

    # Check that the correct command is called with the correct argument
    expected_cmd = ["ipfs", "files", "stat", f"{ipfs.IPFS_HOME}/existing_file.txt"]
    mock_subprocess.assert_called_with(expected_cmd, capture_output=True)

@patch('subprocess.run')
def test_does_file_not_exist(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.does_file_exist` function """

    # Case where file does not exist
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.return_value.stderr.decode.return_value = "file does not exist"
    assert ipfs.does_file_exist("non_existing_file.txt") == False

    # Check that the correct command is called with the correct argument
    expected_cmd = ["ipfs", "files", "stat", f"{ipfs.IPFS_HOME}/non_existing_file.txt"]
    mock_subprocess.assert_called_with(expected_cmd, capture_output=True)

@patch('subprocess.run')
def test_list_files(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.list_files` function """

    # Set up the mock subprocess
    process_mock = MagicMock()
    process_mock.returncode = 0
    process_mock.stdout.decode.return_value = "file1.txt\nfile2.txt\nfile3.txt\n"
    mock_subprocess.return_value = process_mock

    # Test case where files exist
    result = ipfs.list_files("my_directory")
    assert result == ["file1.txt", "file2.txt", "file3.txt"]

    # Test case where no files exist
    process_mock.stdout.decode.return_value = ""
    result = ipfs.list_files("empty_directory")
    assert result == []

@patch('subprocess.run')
def test_delete(mock_subprocess: MagicMock) -> None:
    """ Test the `utils.delete` function """

    filename = "test_delete_existing_file.txt"
    data = b"some contents"

    mock_subprocess.return_value.stdout.decode.return_value = data
    mock_subprocess.return_value.stderr.decode.return_value = ""

    # Create a file
    ipfs.add(filename, data)

    # Check that the file exists
    mock_subprocess.return_value.returncode = 0
    assert ipfs.does_file_exist(filename)

    # Delete the file
    ipfs.delete(filename)

    # Check that the file no longer exists
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.return_value.stderr.decode.return_value = "file does not exist"
    assert not ipfs.does_file_exist(filename)
