import shutil
import tracking_file_db

class FileHandler():
    """
    This would do all the file handling operations 
    
    """
    def __init__(self,conf):
        self.conf = conf

    def save(self, contents, filename="Default.pos"):
        with open('data/'+filename, 'wb') as inf:
            shutil.copyfileobj(contents, inf)

        tf_db = tracking_file_db.TrackingFileDB(self.conf)
        tf_db.add_file(filename)

        return "Done!"


