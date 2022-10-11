import os

def addSufix(path, suffix):
# This function takes a file path and adds a suffix to the file name
	fpath = os.path.split(path)
	fname = os.path.splitext(fpath[1])
	
	#in case of nifti was compressed as 'gz'
	if fname[1] == '.gz':
		fname = os.path.splitext(fname[0])

	new_fname = os.path.join(fpath[0], (fname[0] + suffix + fname[1]))
	
	return new_fname

def changeExt(path, ext):
	fpath = os.path.split(path)
	fname = os.path.splitext(fpath[1])
	return os.path.join(fpath[0], fname[0] + "." + ext)


def print_info(path, process_type = "Processing"):
	print("[INFO] " + process_type + ": " + path)

def clean_path(string):
    # clean and standardize text descriptions, which makes searching files easier
	# forbidden_symbols = ["*", ".", ",", "\"", "\\", "/", "|", "[", "]", ":", ";", " "]
	forbidden_symbols = ["\"", "\\"]
	for symbol in forbidden_symbols:
		string = string.replace(symbol, "/") # replace everything with an underscore
	return string.lower()