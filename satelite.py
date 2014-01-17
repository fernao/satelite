import sys, os, re
import urllib
import time
import json
import logging

class Satelite:
    
    def __init__(self):
        self.get_default_config()
        
        # le todas as configuracoes
        sourcelist = os.listdir('sources')
        sources = [source for source in sourcelist if re.search('json$', source)]
        for source in sources:
            # executa
            self.parse_source(source)        

    
    def handle_loggin(self, source):
        # TODO: logs nao funcionam direito ainda
        self.logger = logging.getLogger(__name__)
        
        logfile = os.path.join(self.config['logs_folder'], source['name'])
        
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.ERROR)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def get_default_config(self):

        BASE_PATH = "/var/www/satelite"
        os.chdir(BASE_PATH)
        f = open("conf.json", "r")
        config = json.loads(f.read())
        
        ###  tenta na primeira vez, se nao tiver, cria        
        # images folder
        try:
            os.listdir(config['images_folder'])
        except OSError:
            os.mkdir(config['images_folder'])
        # logs folder
        try:
            os.listdir(config['logs_folder'])
        except OSError:
            os.mkdir(config['logs_folder'])
        
        self.config = config
    
    def handle_dir(self, dirname):
        # cria diretorio se necessario
        dirname = os.path.join(self.config['images_folder'], dirname)
        try:
            os.listdir(dirname)
        except OSError:
            os.mkdir(dirname)
        return dirname
    
    def check_new_image(self, newimage, oldimage):
        # checa tamanho da imagem para ver se eh a mesma ou eh nova. Se for igual, nao grava
        newsize = os.stat(newimage).st_size
        oldsize = os.stat(oldimage).st_size
        
        if newsize == oldsize:
            return False
        else:
            return True


    def download_image(self, url, dirname):
        # baixa imagens e grava em arquivo
        try:
            image_dwl = urllib.urlopen(url)
        except HTTPError, e:
            self.logger.error("Erro HTTP ao baixar imagem: ", e.code, url)
        except URLError, e:
            self.logger.error("Erro de URL ao baixar imagem:", e.reason, url)
        
        # grava em temporario
        tmp_file = os.path.join(dirname, 'tmp-image.jpg')
        f = open(tmp_file, "w")
        f.write(image_dwl.read())
        f.close()
        return tmp_file

    def save_image(self, dirname, tmp_file):
        # salva imagem no local certo
        now = time.strftime("%Y,%m,%d,%H,%M").split(',')
        imagename = str(now[0]) + "_" + str(now[1]) + "_" + str(now[2]) + "_" + str(now[3]) + "-" + str(now[4]) + ".jpg"
        filename = os.path.join(dirname, imagename)
        
        os.rename(tmp_file, filename)
        f = open(os.path.join(dirname, "LAST_IMAGE"), "w")
        f.write(filename)
        message = "Imagem " + imagename + " gravada"
        self.logger.info(message)


    def parse_source(self, source):
        f = open(os.path.join('sources' , source), 'r')
        source_cfg = json.loads(f.read())
        # caso nao exista diretorio, cria
        dirname = self.handle_dir(source_cfg['name'])
        self.handle_loggin(source_cfg)
        
        # le configuracoes e baixa imagens
        tmp_file = self.download_image(source_cfg['src'], dirname)

        # checa imagem anterior; se nao existe, passa
        try:
            f = open(os.path.join(dirname, "LAST_IMAGE"), "r")
            last_image = f.read()
        except IOError:
            self.save_image(dirname, tmp_file)
            return True
        
        if self.check_new_image(tmp_file, last_image):
            self.save_image(dirname, tmp_file)
        else:
            os.remove(tmp_file)
            print "imagem igual: " + source_cfg['description']


s = Satelite()
