import PyPDF2
from PyPDF2 import PdfFileReader
from pprint import pprint
from tkinter import filedialog
from tkinter import *


def fileName():
    root = Tk()
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    return str(root.filename)

def walk(obj, fnt, emb):
    '''
    We create and add to two sets, fnt = fonts used and emb = fonts embedded.
    '''
    if not hasattr(obj, 'keys'):
        return None, None
    fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
    if '/BaseFont' in obj:
        fnt.add(obj['/BaseFont'])
    if '/FontName' in obj:
        if [x for x in fontkeys if x in obj]:# test to see if there is FontFile
            emb.add(obj['/FontName'])

    for k in obj.keys():
        walk(obj[k], fnt, emb)

    return fnt, emb# return the sets for each page

if __name__ == '__main__':
    fname = fileName()
    pdf = PdfFileReader(fname)
    fonts = set()
    embedded = set()
    for page in pdf.pages:
        obj = page.getObject()
        # updated via this answer:
        # https://stackoverflow.com/questions/60876103/use-pypdf2-to-detect-non-embedded-fonts-in-pdf-file-generated-by-google-docs/60895334#60895334 
        # in order to handle lists inside objects. Thanks misingnoglic !
        # untested code since I don't have such a PDF to play with.
        if type(obj) == PyPDF2.generic.ArrayObject:  # You can also do ducktyping here
            for i in obj:
                if hasattr(i, 'keys'):
                    f, e = walk(i, fonts, embedded_fonts)
                    fonts = fonts.union(f)
                    embedded = embedded.union(e)
        else:
            f, e = walk(obj['/Resources'], fonts, embedded)
            fonts = fonts.union(f)
            embedded = embedded.union(e)

    unembedded = fonts - embedded
    print ('Font List')
    pprint(sorted(list(fonts)))
    if unembedded:
        print ('Unembedded Fonts')
        pprint(unembedded)
