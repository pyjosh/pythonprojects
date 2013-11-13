"""Find duplicate files inside a directory tree."""
 
 
import fnmatch
import os
import hashlib
import time
import shutil
import logging

# --report=foo.txt (report is always verbose)
# --verbose
# --filter=jpeg,png,txt
# --recursively
# --threshold=1024 (num of bytes for md5) -> .read()
# --move / remove        duplicates to separate folder
# -- define which hash md5 sh..
# -- should take the oldest file as reference
# -- print possible GB saving after file deletion
# -- skip="CLIENTS/" == blacklist


# default:
#  - filters: jpg, png, tiff
#  - not recurcive
#  - no threshold
#  - not remove
#  - not report





from argparse import ArgumentParser

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        try:
            chunk = fobj.read(chunk_size)
            if not chunk:
                return
            yield chunk
        except IOError as e:
           logger.error(u"I/O error({0}): {1} {2}".format(e.errno, e.strerror, fobj))


def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def get_filenames_by_extensions(dir_to_search, filters):
    logger.info("Looking for relevant files in defined location...")

    relevant_files = []
    for root, dirnames, filenames in os.walk(dir_to_search):
        for extension in filters:
            for filename in fnmatch.filter(filenames, extension):
                relevant_files.append(os.path.join(root, filename))

    return relevant_files


def print_results(unique_hashes):

    destPath = "found_duplicates"
    if not os.path.exists(destPath):
        os.makedirs(destPath)


    moved_files = set()
    savings = 0
    for k, v in unique_hashes.iteritems():
        counter = 0
        if len(v) > 1:
            print "--------------------------------"
            # sort by creation data - oldest on top
            a = 0
            for i in sorted(v, key=lambda x: x[0]):
                duplicate_filename = i[2]
                if not a:
                    print " + " + time.ctime(i[0]), sizeof_fmt(i[1]), duplicate_filename
                    a = 1
                    continue
                print " - " + time.ctime(i[0]), sizeof_fmt(i[1]), duplicate_filename
                savings += i[1]

                basename_filename = os.path.basename(duplicate_filename)
                if basename_filename in moved_files:
                    counter += 2
                    basename_filename = str(counter) + "__" + basename_filename
                    print "aaa: ", basename_filename
                    print "bbb: ", os.path.join(os.path.abspath(destPath), basename_filename)
                moved_files.add(basename_filename)
                shutil.move(duplicate_filename, os.path.join(os.path.abspath(destPath), basename_filename) )

    print "possible saved memory: ",  sizeof_fmt(savings)



def find_duplicates(relevant_files, hashfun = hashlib.sha512):
    logger.info("Searching for duplicates within relevant files...")


    unique_hashes = {}
    for full_path in relevant_files:
        hashobj = hashfun()
        try:
            for chunk in chunk_reader(open(full_path, 'rb')):
                hashobj.update(chunk)
            file_id = (hashobj.hexdigest(), os.path.getsize(full_path))
            print file_id
            (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(full_path)


            if not unique_hashes.get(file_id[0], None):
                unique_hashes[file_id[0]] = [(ctime, size, full_path)]
            else:
                unique_hashes[file_id[0]].append((ctime, size, full_path))

        except IOError as e:
           logger.error(u"I/O error({0}): {1} {2}".format(e.errno, e.strerror, full_path.decode('utf-8', 'ignore')))

    #print_results(unique_hashes)



def set_logger(args):
    logger = logging.getLogger()
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_form = logging.Formatter(u"[%(levelname)7s] %(message)s")
    ch.setFormatter(ch_form)
    logger.setLevel(logging.DEBUG)
    if args.verbose:
        ch.setLevel(logging.DEBUG)
    if args.quiet:
        ch.setLevel(logging.ERROR)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
 
    parser = ArgumentParser( description='Finds duplicate files.' )
    parser.add_argument(u"root", metavar='R', help='Dir to search.' )
    parser.add_argument(u"--filters", dest=u"filters", type=unicode, default=None, help=u"specify file extensions e.g. --filters=*.java, *.cpp, *.py")
    group_a = parser.add_mutually_exclusive_group()
    group_a.add_argument(u"--verbose", action=u"store_true", help=u"shows more information than the usual logging mode")
    group_a.add_argument(u"--quiet", action=u"store_true", help=u"shows less information than the usual logging mode")
    group_b = parser.add_mutually_exclusive_group()
    group_b.add_argument(u"--remove", action=u"store_true", help=u"remove duplicated files on the fly")
    group_b.add_argument(u"--move", action=u"store_true", help=u"move duplicated files to separate directory")

    args = parser.parse_args()
    logger = set_logger(args)
 
    relevant_files = get_filenames_by_extensions(args.root, args.filters.split(","))
    find_duplicates(relevant_files)
 
    # print '%d Duplicate files found.' % len(DUPS)
    # for f in sorted(DUPS):
    #     if ARGS.remove == True:
    #         remove( f )
    #         print '\tDeleted '+ f
    #     else:
    #         print '\t'+ f
