from os import scandir

path_audio = r'.\AudioBot\CarpetaAudios'

def ls( path: str):
    return([arch.path for arch in scandir(path) if arch.is_file()]) 

print(ls(path_audio)) 

"""Aqui manejo los archivos en la carpeta puedo encontrar el path y asi usarlo para otras tareas, con el directorio relativo"""