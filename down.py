# python3
import urllib.request as request
import os

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

	for i in range(len(urlList)):
		#request with fake header
		videoReq = request.Request(url=urlList[i], headers={'User-Agent': 'Mozilla/5.0', 'referer' : fakeReferer})

		#get video
		videoPiece = request.urlopen(videoReq).read()

	

		fileName = str(i).zfill(4) + ".m3u8"
		filePath = os.path.join(videoName, fileName)

		createFolder(videoName)

		#save video
		with open(filePath, "wb") as file:
			file.write(videoPiece)

		print("file save : " + fileName)

		#write file path with filename
		#using this file in FFMPEG
		temp = "file " + "'" +  filePath + "'\n"
		with open(os.path.join(videoName, "fileList.txt"), 'a') as file:
			file.write(temp)


def mergeFile(videoName):
	command = "ffmpeg -f concat -safe 0 -i fileList.txt -c copy "+ videoName + ".mp4"
	os.system(command)

def main():
	try:
		urlList = readUrlTxt()

		videoName = getVideoName()

		downTsFile(videoName, urlList)

		mergeFile(videoName)

	except Exception as error:
		print('-' * 20)
		print('error occured', error)

if __name__ == "__main__":
	main()