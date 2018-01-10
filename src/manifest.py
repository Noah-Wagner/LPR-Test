import pandas


class Manifest:

    @staticmethod
    def load_manifest(manifest_file_path):
        manifest = Manifest()
        manifest.file_path = manifest_file_path
        manifest.data_frame = pandas.read_excel(manifest_file_path)
        return manifest

    def get_image_list(self):
        return self.data_frame.Filepath

    def write_success(self, success, responses):
        writer = pandas.ExcelWriter(self.file_path)
        self.data_frame.to_excel(writer, index=False)
        success_df = pandas.DataFrame({'Success': success, 'Response:': responses})
        success_df.to_excel(writer, startrow=0, startcol=2, index=False)
        writer.save()
