import dropbox


class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2"""
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as file:
            dbx.files_upload(file.read(), file_to)
