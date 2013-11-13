import os
from ftplib import FTP

BINARY_STORE = 1

class FtpUploader(object):

    def __init__(self):
        pass

    def connect(self, user, password, server, port=21):
        self.ftp = FTP()
        self.ftp.connect(server, port)
        self.ftp.login(user, password)

    def disconnect(self):
        self.ftp.quit()

    def uploadFile(self, uploadFilePath, uploadDir=None):

        if uploadDir:
            self.ftp.cwd(uploadDir)
            # ftp.mkd('lukas123')

        try:
            with open(uploadFilePath) as uploadFile:

                uploadFileName = os.path.basename(uploadFilePath)

                print "Uploading {0} ...".format(uploadFileName)

                if BINARY_STORE:
                    self.ftp.storbinary('STOR ' + uploadFileName, upload_file, 1024)
                else:
                    self.ftp.storlines('STOR ' + uploadFileName, upload_file)


        except IOError:
            print "No such file: ".format(uploadFilePath)

        print "{0} uploaded sucesfully.".format(uploadFileName)
