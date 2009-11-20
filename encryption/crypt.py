#!/usr/bin/env python2.4

from Crypto.Cipher import AES as coder
from Crypto.Hash import SHA as hasher
import os,random # for random number generation

class BadVersion(Exception):
    '''Used when we try to decrypt something and version numbers do not match'''
    pass

PADCHAR = '?'
HEADERSIZE = 2
VERSION = '2.0'
VERSIONHEADERSIZE = len(VERSION)
OLD_VERSIONS = ['$'+'Revision: 1.19 '+'$',] # used for backwards compatability tests
# MODE is either coder.MODE_CBC or coder.MODE_ECB (others will work, but have not been tested)
MODE = coder.MODE_CBC

def pad(data,to_len=coder.block_size):
    '''pad data to coder.block_size'''
    datalen = len(data)
    remainder = datalen % to_len
    if remainder != 0:
        padlen = to_len - remainder
    else:
        padlen = 0
    data = ''.join([data, PADCHAR*padlen])
    return data

class crypt(object):
    def __init__(self, key):
	self.__key = key
        #h = hasher.new()
        #h.update(key)
        #if coder.key_size:
        #    self.__key = h.hexdigest()[:coder.key_size]
        #else:
        #    self.__key = h.hexdigest()[:32]
        self.__version = VERSION

    def encrypt(self,data):
        try:
            iv = '.' * 16 #os.urandom(coder.block_size)
        except:
            iv = []
            for i in xrange(coder.block_size):
                iv.append(chr(random.randrange(0,255)))
            iv = ''.join(iv)
        codeObj = coder.new(self.__key, MODE, iv)
        data = (' '*HEADERSIZE)+data
        padded_data = pad(data)
        padlen = len(padded_data) - len(data)
        header = str(padlen).rjust(HEADERSIZE)
        pieces = [header,padded_data[HEADERSIZE:]]
        cypher = self._version + codeObj.IV + codeObj.encrypt(''.join(pieces))
        return cypher

    def decrypt(self,data):
        if not data:
            return ''
        good = False
        for x in [VERSION]+OLD_VERSIONS:
            version = data[:len(x)]
            if version == x:
                good = True
                break
        if not good:
            raise BadVersion, 'Incompatable version (expected %s, got %s)' % (self._version,version)
        data = data[len(version):]
        ## below will stay the same
        iv = data[:coder.block_size]
        data = data[coder.block_size:]
        codeObj = coder.new(self.__key, MODE, iv)
        plain = codeObj.decrypt(data)
        header = plain[:HEADERSIZE].strip()
        padlen = int(header)
        if padlen != 0:
            ret = plain[HEADERSIZE:-padlen]
        else:
            ret = plain[HEADERSIZE:]
        return ret

    _key = property(lambda self: self.__key)
    _version = property(lambda self: self.__version)
    _rpool = property(lambda self:self.__rpool)

class codeFile(object):
    def __init__(self,*args, **kwargs):
        self.__key = kwargs.get('key','test')
        self.__c = crypt(self.__key)

    def open(self,fileName,mode='rb'):
        self.__fileObj = codeFileObj(self.__c,fileName,mode)
        return self.__fileObj

class codeFileObj(object):
    def __init__(self,c,fileName,mode):
        self.__c = c
        self.__curLocation = 0
        self.__fileData = ''
        self.__outFileData = []
        self.__write_called = False
        self.__mode = mode
        self.__file_name = fileName
        if '+' in mode or 'a' in mode:
            raise Exception, "that mode won't work with all of my functions"
        try:
            self.__fileObj = open(fileName, mode)
        except:
            self.__fileOpen = False
            raise
        else:
            self.__fileOpen = True
    
    def __del__(self,*args, **kwargs):
        if self.__fileOpen:
            self.__fileObj.close()

    def read(self,size=-1):
        if not self.__fileOpen:
            return None
        # cache the data for speed
        if not self.__fileData:
            self.__fileData = self.__fileObj.read()
            self.__fileData = self.__c.decrypt(self.__fileData)
        if self.__fileData and self.__curLocation >= len(self.__fileData):
            raise EOFError, 'EOF found in read'
        # return the part of the file that was asked for
        if size >= 0:
            ret = self.__fileData[self.__curLocation:self.__curLocation+size]
            self.__curLocation += size
            if self.__curLocation > len(self.__fileData):
                self.__curLocation = len(self.__fileData)
        else:
            ret = self.__fileData[self.__curLocation:]
            self.__curLocation = len(self.__fileData)
        return ret

    def readlines(self,size=-1):
        if not self.__fileOpen:
            return None
        # cache the data for speed
        if not self.__fileData:
            self.__fileData = self.__fileObj.read()
            self.__fileData = self.__c.decrypt(self.__fileData)
        if self.__curLocation >= len(self.__fileData):
            raise EOFError, 'EOF found in readlines'
        ret = []
        temp = []
        start = self.__curLocation
        for x in xrange(start,len(self.__fileData)):
            self.__curLocation += 1
            if self.__fileData[x] == '\n':
                temp.append(self.__fileData[x])
                ret.append(''.join(temp))
                temp = []
                continue
            if len(ret) == size:
                ret.append(''.join(temp))
                temp = []
                break
            temp.append(self.__fileData[x])
        ret.append(''.join(temp))
        return ret

    def readline(self,size=-1):
        if not self.__fileOpen:
            return None
        # cache the data for speed
        if not self.__fileData:
            self.__fileData = self.__fileObj.read()
            self.__fileData = self.__c.decrypt(self.__fileData)
        if self.__curLocation >= len(self.__fileData):
            raise EOFError, 'EOF found in readline'
        ret = []
        for x in xrange(self.__curLocation,len(self.__fileData)):
            self.__curLocation += 1
            if self.__fileData[x] == '\n':
                ret.append(self.__fileData[x])
                break
            if len(ret) == size:
                break
            ret.append(self.__fileData[x])
        ret = ''.join(ret)
        return ret

    def write(self,data):
        if not self.__fileOpen:
            raise Exception, 'file not open'
        self.__write_called = True
        self.__outFileData.append(data)
        
    def tell(self):
        return self.__curLocation
        
    def seek(self,pos,how=0):
        if how == 0:
            self.__curLocation = pos
        elif how == 1:
            self.__curLocation += pos
        elif how == 2:
            if not self.__fileData:
                self.__fileData = self.__fileObj.read()
                self.__fileData = self.__c.decrypt(self.__fileData)
            self.__curLocation = len(self.__fileData) + pos
        else:
            raise Exception, 'how must be 0, 1, or 2'

    def flush(self):
        raise NotImplementedError, 'close the file and reopen it instead'

    def close(self,*args, **kwargs):
        if self.__fileOpen and self.__write_called:
            self.__fileObj.write(self.__c.encrypt(''.join(self.__outFileData)))
            self.__outFileData = []
        if self.__fileOpen:
            self.__fileObj.close(*args,**kwargs)
            self.__fileOpen = False
