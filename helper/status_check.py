from tracking_file_db import TrackingFileDB


class StatusCheck(object):

    def __init__(self,conf):
        self.tf_db = TrackingFileDB(conf)

    def check_upload_status(self,filename):
        result = self.tf_db.get_status(filename)
        print("Upload : "+ str(result))
        return result


    def check_status(self):
        result = self.tf_db.get_recent()
        print("Status : "+ str(result))
        return result
