#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gdata.photos.service
import gdata.media
import gdata.geo
from PIL import Image
from PIL.ExifTags import TAGS
from pprint import pprint
import argparse

PHOTO_BASE = '/home/utada/picasa_test/'
PICASA_MAX_FREE_IMAGE_DIMENSION = 2048
PICASA_MAX_VIDEO_SIZE_BYTES = 104857600

# Auth
gd_client = gdata.photos.service.PhotosService()
def auth(email, password):
    gd_client.email = email
    gd_client.password = password
    gd_client.source = 'exampleCo-exampleApp-1'
    gd_client.ProgrammaticLogin()
    #return gd_client

# list of albums
def listAlbum():
    albums = gd_client.GetUserFeed()
    #for album in albums.entry:
    #    print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
    #              album.numphotos.text, album.gphoto_id.text)
    return albums

def listPhotos(album_id):
    photos = gd_client.GetFeed(
          '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
                    'default', album_id))
    #for photo in photos.entry:
    #    print 'Photo title:', photo.title.text
    return photos

# add an allbum
def addAlbum(name):
    album = gd_client.InsertAlbum(title=name, summary='This is an album', access='private')
    return album

# list of local directories
def listPhotoDir(source):
    names = []
    #for root, dirs, files in os.walk(PHOTO_BASE):
    for root, dirs, files in os.walk(source):
        if files:
            #print(root, dirs, files)
            [year,month,day] = root.replace(PHOTO_BASE, "").split("/")
            #print(year,month,day)
            names.append(year + "/" + month)
    return names

def postPhoto(album_id, root, filename):
    album_url = '/data/feed/api/user/%s/albumid/%s' % ('default', album_id)
    photo = gd_client.InsertPhotoSimple(album_url, filename, 
        'Uploaded using the API', root + "/" + filename, content_type='image/jpeg')
    return photo

def imageMaxSize(filepath):
    im=Image.open(filepath)
    return (im.size)

def parseArgs():
    parser = argparse.ArgumentParser(description='Upload pictures to picasa web albums / Google+.')
    parser.add_argument('--email', help='the google account email to use (example@gmail.com)', required=True)
    parser.add_argument('--password', help='the password (you will be promted if this is omitted)', required=True)
    parser.add_argument('--source', help='the directory to upload', required=True)
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
    for photo_dir in list(set(listPhotoDir(source))):
        print(photo_dir)
        # if album does not exists on the server
        if (photo_dir in [album.title.text for album in albums.entry]) == False:
            album_name = photo_dir
            print('Create album ' + album_name)
            new_album = addAlbum(album_name)
            #pprint(new_album)
            album_id = new_album.gphoto_id.text
            print("new album_id = " + album_id)

        # photos in the local directory
        for root, dirs, files in os.walk(PHOTO_BASE + photo_dir):
            print(root)
            if files:
                #print(root, dirs, files)

                for album in albums.entry:
                    if photo_dir == album.title.text:
                        album_id = album.gphoto_id.text
                        #print("album_id = " + album_id)
                        # server photos in album
                        photos = listPhotos(album_id)

                for filename in sorted(files):
                    fname, fileExtension = os.path.splitext(filename)
                    filename2 = fname + "_2048.JPG"
                    #if not filename.lower().endswith('.mp4'):
                    if fileExtension.lower() != ".mp4":
                        filepath = root + "/" + filename
                        if 'photos' in locals() and (filename2 in [photo.title.text for photo in photos.entry]):
                            # same photo on the server
                            print(" --> " + fname + ' exists.')
                        else:
                            #print(fname + ' not exists in server album')
                            print(" --> upload " + fname)
                            imsize = imageMaxSize(filepath)
                            if max(imsize) > PICASA_MAX_FREE_IMAGE_DIMENSION:
                                image = Image.open(filepath)
                                size = (2048, 2048)
                                image.thumbnail(size, Image.ANTIALIAS)
                                exif = image.info['exif']
                                image.save(root + "/" + filename2, exif=exif)
                            # upload photo
                            postPhoto(album_id, root, filename2)
                            os.remove(root + "/" + filename2)

