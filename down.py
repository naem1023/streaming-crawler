# python3
import urllib.request as request
import os
import traceback

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('failed to make folder ' + directory)

def readUrlTxt():
	urlTxt = open("tslist.txt", 'r')

	#get all txt line
	urlList = urlTxt.readlines()

	return urlList


def getVideoName():
	videoName = open("name.txt", 'r')
	name = videoName.readline()
	return name

def downTsFile(videoName, urlList):
	fakeReferer = 'https://avgle.com'

	videoFolderExist = False
	len_fileListTxt = 0
	fileListTxtName = os.path.join(videoName, "fileList.txt")


	try:
		command = """aria2c -c -x 4 --header="Referer: """ + fakeReferer + """" -d """ + str(videoName) + " -i tslist.txt"
		os.system(command)

	except Exception as error:
		print('-' * 20)
		traceback.print_exc()

	'''
	#check existence of downloaded files
	if os.path.isfile(fileListTxtName) :
		#text file : already saved m38u file
		
		fileListTxtFile = open(fileListTxtName, 'r')

		fileListTxt = fileListTxtFile.readlines()
		len_fileListTxt = len(fileListTxt)

		videoFolderExist = True

	for i, v in enumerate(urlList):
		fileName = str(i).zfill(4) + ".m3u8"
		filePath = os.path.join(videoName, fileName)

		#check existence of file
		if videoFolderExist:
			if i <= len_fileListTxt - 1 :
				fileListTxtFile.close()
				continue;

		print("start request " + fileName)
		
		#request with fake header
		videoReq = request.Request(url=v, headers={'User-Agent': 'Mozilla/5.0', 'referer' : fakeReferer})

		#get video
		#videoPiece = request.urlopen(videoReq).read()

		createFolder(videoName)

		#save video
		#with open(filePath, "wb") as file:
		#	file.write(videoPiece)
		

		print("file save : " + fileName)

		#write file path with filename
		#using this file in FFMPEG
		#temp = "file " + "'" +  filePath + "'\n"
		#with open(fileListTxtName, 'a') as file:
		#	file.write(temp)
		'''


def mergeFile(videoName):
	command = "ffmpeg -f concat -safe 0 -i "+ str(videoName) + "\\fileList.txt -c copy "+ videoName + ".mp4"
	os.system(command)

def makeTsList(videoName):
	fileListTxtFile = open(os.path.join(videoName, "fileList.txt"), 'w')

	#get file list of video folder
	fileList = os.listdir(videoName)

	#find ts file from list
	for file in fileList:
		ext = os.path.splitext(file)[-1]
		if ext == '.ts':
			temp = "file '" + videoName + '\\' + str(file) + "'\n"
			fileListTxtFile.write(temp)

	fileListTxtFile.close()

def main():
	#try:
		urlList = readUrlTxt()

		videoName = getVideoName()

		downTsFile(videoName, urlList)

		makeTsList(videoName)

		mergeFile(videoName)

	#except Exception as error:
	#	print('-' * 20)
	#	traceback.print_exc()

if __name__ == "__main__":
	main()