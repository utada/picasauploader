#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import gdata.photos.service
import gdata.media
import gdata.geo
from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
import argparse
import glob

PHOTO_BASE = '/home/utada/Pictures/'
PICASA_MAX_FREE_IMAGE_DIMENSION = 2048
PICASA_MAX_VIDEO_SIZE_BYTES = 104857600

# Auth
gd_client = gdata.photos.service.PhotosService()
def auth(email, password):
    gd_client.email = email
    gd_client.password = password
    gd_client.source = 'exampleCo-exampleApp-1'
    gd_client.ProgrammaticLogin()

# list of albums
def listAlbum():
    albums = gd_client.GetUserFeed()
    #for album in albums.entry:
    #    print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
    #              album.numphotos.text, album.gphoto_id.text)
    return albums

def listPhotos(album_id):
    photos = gd_client.GetFeed(
          '/data/feed/api/user/%s/albumid/%s?kind=photo' % ('default', album_id))
    #for photo in photos.entry:
    #    print 'Photo title:', photo.title.text
    return photos

# add an allbum
def addAlbum(name):
    album = gd_client.InsertAlbum(title=name, summary='This is an album', access='private')
    return album

# list of local directories
#def listPhotoDir(source):
#    names = []
#    for root, dirs, files in os.walk(source):
#        if files:
#             year, month, day = root.replace(PHOTO_BASE, '').split('/')
#             names.append(year + "/" + month)
#    return names

def postPhoto(album_id, root, filename):
    album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', album_id)
    photo = gd_client.InsertPhotoSimple(album_url, filename,
        'Uploaded using the API', root + "/" + filename, content_type='image/jpeg')
        #'Uploaded using the API', root + "/" + filename.decode(), content_type='image/jpeg')
        #'Uploaded using the API', root + "/" + filename.encode(), content_type='image/jpeg')
    return photo

def imageMaxSize(filepath):
    im=Image.open(filepath)
    return (im.size)

def parseArgs():
    parser = argparse.ArgumentParser(description='Upload pictures to picasa web albums / Google+.')
    parser.add_argument('--email', help='the google account email to use (example@gmail.com)', required=True)
    parser.add_argument('--password', help='the password (you will be promted if this is omitted)', required=True)
    parser.add_argument('--source', help='the directory to upload (/home/utada/Pictures/2013/12)', required=True)
    #parser.add_argument(
    #    '--no-resize',
    #    help="Do not resize images, i.e., upload photos with original size.", 
    #    action='store_true')

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parseArgs()
    #pprint(args)
    source = args.source
    auth(args.email, args.password)

    # server albums
    albums = listAlbum()
    #for album in albums.entry:
    #    print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
    #              album.numphotos.text, album.gphoto_id.text)

    # local photo directories
    #for photo_dir in list(set(listPhotoDir(source))):
    #print(source)
    year, month = source.replace(PHOTO_BASE, '').split('/')
    photo_dir = year + '/' + month

    # if album does not exists on the server
    if (photo_dir in [album.title.text for album in albums.entry]) == False:
        album_name = photo_dir
        print('Create album ' + album_name)
        new_album = addAlbum(album_name)
        #pprint(new_album)
        album_id = new_album.gphoto_id.text
        print("new album_id = " + album_id)

    # photos in the local directory
    root = PHOTO_BASE + photo_dir
    #for files in glob.glob(PHOTO_BASE + photo_dir + '/*/*'):
    #    print(files)
    #sys.exit()
    for filepath in glob.glob(PHOTO_BASE + photo_dir + '/*/*'):
        print(filepath)
        for album in albums.entry:
            if photo_dir == album.title.text:
                album_id = album.gphoto_id.text
                #print("album_id = " + album_id)
                # server photos in album
                photos = listPhotos(album_id)
                #for photo in photos.entry:
                #    print(photo.title.text)

        filename = os.path.basename(filepath)
        #print(' =' + filename)
        fname, fileExtension = os.path.splitext(filename)
        filename2 = fname + "_2048" + fileExtension
        if fileExtension.lower() in [".jpg", ".png"]:
            if 'photos' in locals() and (filename2 in [photo.title.text for photo in photos.entry]):
                # same photo on the server
                print(" --> " + filename2 + ' exists.')
            elif 'photos' in locals() and (filename in [photo.title.text for photo in photos.entry]):
                # same photo on the server
                print(" --> " + filename + ' exists.')
            else:
                #print(fname + ' not exists in server album')
                imsize = imageMaxSize(filepath)
                if int(max(imsize)) > PICASA_MAX_FREE_IMAGE_DIMENSION:
                    image = Image.open(filepath)
                    size = (2048, 2048)
                    image.thumbnail(size, Image.ANTIALIAS)
                    #pprint(image.info)
                    if 'exif' in image.info:
                        exif = image.info['exif']
                        image.save(root + "/" + filename2, 'JPEG', quality=100, exif=exif)
                    else:
                        image.save(root + "/" + filename2, 'JPEG', quality=100)
                    # upload photo
                    print(" --> upload " + filename2)
                    postPhoto(album_id, root, filename2)
                else:
                    # upload photo
                    print(" --> upload " + filename)
                    postPhoto(album_id, root, filename)
                if os.path.isfile(root + "/" + filename2):
                    os.remove(root + "/" + filename2)

