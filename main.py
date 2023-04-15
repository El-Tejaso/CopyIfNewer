import os
import sys
import shutil
import tkinter;
import errno;
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

def copy_if_newer(src, dst):
    if os.path.isfile(dst):
        try:
            dst_mtime = os.path.getmtime(dst)
            src_mtime = os.path.getmtime(src)
            if dst_mtime >= src_mtime:
                # dest file is newer or same modify time, do not copy this file over.
                return False

        except Exception as e:
            pass

    try:
        dst_dir = os.path.dirname(dst)
        os.makedirs(dst_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    shutil.copy2(src, dst)
    return True


def copy_tree_if_newer(src, dst):
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    num_copied = 0
    num_skipped = 0
    num_error = 0
    for root, dirs, files in os.walk(src):
        for filepath in files:
            num_total = num_copied + num_skipped + num_error
            if num_total % 500 == 0:
                print(str(num_total) + " files processed ...")

            file_src = os.path.join(root, filepath)
            file_dst = os.path.join(root.replace(src, dst), filepath)
            try:
                if copy_if_newer(file_src, file_dst):
                    num_copied += 1
                else:
                    num_skipped += 1
            except Exception as e:
                print(e)
                num_error += 1


    print("Copied", num_copied, "files")

    return (num_copied, num_skipped, num_error)


## ------------ UI

copy_from_default = "<Select folder to copy files from>"
copy_to_default = "<Select folder to copy files to>"
copy_from = copy_from_default
copy_to = copy_to_default


# can set default paths when opening from the command line
if len(sys.argv) == 3:
    copy_from_argv = sys.argv[1]
    copy_to_argv = sys.argv[2]
    if os.path.exists(copy_from_argv):
        copy_from = copy_from_argv
    if os.path.exists(copy_to_argv):
        copy_to = copy_to_argv


root = tkinter.Tk()
root.title("Copy newer files")
root.minsize(400, 50)
frame = ttk.Frame(root, padding=10)
frame.grid()

src_file_label = ttk.Label(frame, text=copy_from)
src_file_label.grid(column = 1, row = 1, columnspan=4)
dst_file_label = ttk.Label(frame, text=copy_to)
dst_file_label.grid(column = 1, row = 2, columnspan=4)

def select_src(): 
    global copy_from

    copy_from = filedialog.askdirectory()
    src_file_label.config(text=copy_from)

def select_dst():
    global copy_to

    copy_to = filedialog.askdirectory()
    dst_file_label.config(text=copy_to)

ttk.Button(frame, text="Select...", command=select_src).grid(column = 0, row = 1)
ttk.Button(frame, text="Select...", command=select_dst).grid(column = 0, row = 2)

num_copied_text = ttk.Label(frame, text="")
num_copied_text.grid(row = 3, column=4)

def copy_stuff():
    global copy_from, copy_to

    try:
        if copy_from == copy_from_default:
            raise Exception("Select a folder to copy the files from")

        if copy_to == copy_to_default:
            raise Exception("Select a folder to copy the files to")

        num_copied, num_skipped, num_error = copy_tree_if_newer(copy_from, copy_to)
        num_copied_text.config(text=str(num_copied) + " copied, " + str(num_skipped) + " skipped, " + str(num_error) + " errors")
    except Exception as e:
        num_copied_text.config(text="")
        messagebox.showerror("Error when copying files", e)

ttk.Button(frame, text="Copy files", command=copy_stuff).grid(column = 1, row = 3, columnspan=3)

root.mainloop()