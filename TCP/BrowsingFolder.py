from os import listdir
from os.path import join, isfile, getsize, getmtime
from time import ctime


class BrowsingFolder:
    def create_html(self, path='/files'):
        file_list_names = self.__list_folder(path)
        html = self.__mount_html(path, file_list_names)
        return html

    @staticmethod
    def __mount_html_item(file_path, name):
        file_size = getsize(f'{file_path}/{name}')
        last_modify = ctime(getmtime(f'{file_path}/{name}'))
        icon = 'file.svg' if isfile(name) else 'folder.svg'
        a_html = ('<tr>'
                  f'<td valign="top"><img src="./icons/{icon}" alt="icon" /></td>'
                  f'<td><a href="{file_path}/{name}">{name}</a></td>'
                  f'<td align="right">{last_modify}</td>'
                  f'<td align="right">{file_size} bytes</td>'
                  '<td>&nbsp;</td>'
                  '</tr>')

        return a_html

    def __mount_html_list(self, path, files_list_names):
        list_html = ''

        for file_name in files_list_names:
            list_html += self.__mount_html_item(path, file_name)

        if list_html == '':
            return '<tr><td><p>no files found</p></td><tr/>'

        return list_html

    def __mount_html(self, path, files):
        html_list = self.__mount_html_list(path, files)

        html = ('<!DOCTYPE html>'
                '<html lang="en">'
                '<head>'
                '<meta charset="UTF-8" />'
                '<meta http-equiv="X-UA-Compatible" content="IE=edge" />'
                '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
                '<title>socket TPC</title>'
                '</head>'
                '<body>'
                '<h1>Socket TCP</h1>'
                '<table>'
                '<tr>'
                '<th valign="top"></th>'
                '<th><h3>Name</h3></th>'
                '<th><h3>Last modified</h3></th>'
                '<th><h3>Size</h3></th>'
                '</tr>'
                '<tr>'
                '<th colspan="4"><hr /></th>'
                '</tr>'
                f'{html_list}'
                '<tr>'
                '<th colspan="4"><hr /></th>'
                '</tr>'
                '</table>'
                '</body>'
                '</html>'
                )

        return html

    @staticmethod
    def __list_folder(path):
        try:
            file_list_names = [f for f in listdir(path) if join(path, f)]
            return file_list_names
        except:
            return []

    def create_html_file(self, path):
        html = self.create_html(path)
        with open(f'{path}/index.html', 'w') as file:
            file.write(html)
