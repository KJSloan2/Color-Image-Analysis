#Import os for directory and file operations
import os
from os import listdir
from os.path import isfile, join

#Import json for storing and writing image stats
import json

#Import datetime for handeling the date information from image metadata
import datetime
from datetime import datetime, timezone

#Import PIL for handeling image resizing
from PIL import Image, ImageOps
######################################################################################
def format_number(number):
  '''Take a raw number and adds zeros to the start of the number.
  This function is used for making a unique ID for images processed.'''
    number_str = str(number)
    num_zeros = 5 - len(number_str)
    num_zeros = min(num_zeros, 3)
    formatted_number = '0' * num_zeros + number_str
    return str(formatted_number)
######################################################################################
def get_directories_in_directory(directory_path):
  '''Gets the diretories in the root directory. This is used when images are
  located across multiple subdirectories'''
    directory_list = [f.path for f in os.scandir(directory_path) if f.is_dir()]
    return directory_list
######################################################################################
#imageStats_ is a dict where summary data for processed images will be stored
imageStats_ = {}
#provide the root directory path and name of the subdirectory where images are stored
dirKey = "DIRECTORY NAME"
rootDir = "ROOT DIRECTORY PATH"
######################################################################################
'''Images will be rescaled when shuttled. Give the maximun dimension (in pixled) for
shuttled images. Images are copied and reszed. The resized copy is shuttled.'''
max_dimension = 150
######################################################################################
'''The following loop reads over the specified directory and shuttles images to 
the designated location. Images are resized according to the 'max_dimension' variable
and meta data is written to 'imageStats_''''
dirPath = r"{}/{}/".format(rootDir,dirKey)
files_ = [f for f in listdir(dirPath) if isfile(join(dirPath, f))]
imId = 0
for f in files_:
	parse_f  = f.split(".")
	if parse_f[-1].lower() in ["jpg","jpeg"]:
		print(f)
		impath =  "%s%s%s" % (dirPath,"/",f)
		im_stats = os.stat(impath)
		im_created = im_stats.st_ctime
		im_modified = im_stats.st_mtime
		im_cretaed_formated = datetime.fromtimestamp(im_stats.st_ctime, tz=timezone.utc)
		im_modified_formated = datetime.fromtimestamp(im_stats.st_mtime, tz=timezone.utc)
		date_modified = im_modified_formated.strftime("%m/%d/%Y")
		im = Image.open(impath)
		im_width, im_height = im.size
		if im_width > im_height:
			new_width = max_dimension
			new_height = int(im_height * (max_dimension / im_width))
		else:
			new_height = max_dimension
			new_width = int(im_width * (max_dimension / im_height))
		try:
			imResized = im.resize((new_width,new_height))
			imResized = imResized.convert("RGB")
			parse_dateModified = date_modified.split("/")
			imName = "_".join([
				dirKey,
				dirKey,format_number(imId),
				str(parse_dateModified[2]),
				str(parse_dateModified[0]),
				str(parse_dateModified[1])])
			imResized.save(os.path.join(r"01_data/textures/", f"{imName}.jpg"))
			imageStats_[imName] = {
				"image_name_original":parse_f[0],
				"width_orig":im_width,"height_orig":im_height,
				"width_new":new_width,"height_new":new_height,				
				"date_modified":date_modified
			}
			imId+=1
		except Exception as e:
			print(f"Error processing {f}: {e}")
			pass
######################################################################################
with open(str(
	"%s%s" % (r"02_output/","imageStats_ref.json")
	), "w", encoding='utf-8') as json_output:
	json_output.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
######################################################################################
print("DONE")
