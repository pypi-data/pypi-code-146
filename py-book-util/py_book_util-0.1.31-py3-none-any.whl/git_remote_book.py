import os
from py_book_util import util

class GitRemoteBook(object):
    def __init__(self, remote_file, git_repo_path, local_dir, current_working_dir):
        self.remote_file = remote_file
        self.git_repo_path = git_repo_path
        self.local_dir = local_dir
        self.current_working_dir = current_working_dir

    def get_remote_path(self):
        return self.git_repo_path + "/" + self.remote_file
    
    def get_git_repo_name(self):
        return self.git_repo_path[self.git_repo_path.rindex("/")+1::]

    def get_local_path(self):
        remote_path = self.get_remote_path()
        local_path = self.local_dir + "/" + remote_path
        if remote_path.startswith("/"):
            local_path = self.local_dir + remote_path
        print("local_path is %s"%local_path)
        return local_path
        
    def get_local_path_in_book(self):
        remote_path = self.get_remote_path()
        local_path_in_book = remote_path
        if remote_path.startswith("/"):
            local_path_in_book = remote_path[1::]
        print("local_path_in_book is %s"%local_path_in_book)
        return local_path_in_book
        
    def download_file_from_remote_repo_to_local_dir(self):
        import shutil
        if os.path.isdir(self.local_dir):
            shutil.rmtree(self.local_dir)
        os.mkdir(self.local_dir)
        cucumber_task = "Download %s %s from server" % (self.get_git_repo_name(), self.remote_file)
        util.print_run_cmd('006_cucumber_parallel "%s"'% cucumber_task)
        util.run_deno_cmd("dos2unix " + self.get_local_path())

    def upload_file_from_local_dir_to_remote_repo(self):
        cucumber_task = "Upload %s %s to server" % (self.get_git_repo_name(), self.remote_file)
        util.run_deno_cmd("dos2unix " + self.get_local_path())
        util.print_run_cmd('006_cucumber_parallel "%s"'% cucumber_task)
        
    def book_git_init(self):
        os.chdir(self.current_working_dir)
        os.chdir(self.local_dir)
        assert(os.getcwd().endswith("book"))
        util.print_run_cmd("git init")
        util.print_run_cmd("git config core.autocrlf input")
        os.chdir(self.current_working_dir)

    def book_git_add(self):
        os.chdir(self.current_working_dir)
        os.chdir(self.local_dir)
        assert(os.getcwd().endswith("book"))
        util.print_run_cmd("git add " + self.get_local_path_in_book())
        os.chdir(self.current_working_dir)
    
    def book_git_status(self):
        os.chdir(self.current_working_dir)
        os.chdir(self.local_dir)
        assert(os.getcwd().endswith("book"))
        util.print_run_cmd('git status"')
        os.chdir(self.current_working_dir)
    
    def book_git_commit(self, message):
        os.chdir(self.current_working_dir)
        os.chdir(self.local_dir)
        assert(os.getcwd().endswith("book"))
        util.print_run_cmd('git commit -m "%s"'%message)
        os.chdir(self.current_working_dir)
    
    def book_checkout_and_check_md5sum(self, md5sum):
        file_name_in_book = self._book_prepare()
        assert(md5sum == util.get_file_md5sum(file_name_in_book))
        print("file_name_downloaded is %s" % file_name_in_book)
        # util.display_code(file_name_in_book)
        # from IPython.display import Code
        # Code(filename=file_name_in_book, language="text")
        os.chdir(self.current_working_dir)

    def book_move_line(self, old_line, new_line, ori_md5, new_md5):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.move_line_in_file(file_name_in_book, old_line, new_line)
            commit_message = "Move line %d to line %d" % str(old_line, new_line)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_move_line_block(self, line_begin, line_end, new_line, ori_md5, new_md5):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.move_line_block_in_file(file_name_in_book, line_begin, line_end, new_line)
            commit_message = "Move line block(%d, %d) to line %d" % str(line_begin, line_end, new_line)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_del_lines(self, line_numbers, ori_md5, new_md5):
        if isinstance(line_numbers, list) == False:
            line_numbers = [line_numbers]        
        line_numbers.sort()
        line_numbers.reverse()
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            for single_line_num in line_numbers:
                util.del_line_in_file(file_name_in_book, single_line_num)
            commit_message = "Del line %s" % str(line_numbers)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_del_blocks(self, line_blocks, ori_md5, new_md5):
        if isinstance(line_blocks, dict) == False:
            line_blocks = {line_blocks:line_blocks}
        # {1:3, 4:4}
        # 4 --> {4:4}
        # {1:3}
        tmp_line_numbers = line_blocks.keys()
        line_numbers = []
        for single_num in tmp_line_numbers:
            line_numbers.append(single_num)
        line_numbers.sort()
        line_numbers.reverse()
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            for single_line_num in line_numbers:
                util.del_block_in_file(file_name_in_book, single_line_num, line_blocks[single_line_num])
            commit_message = "Del block %s" % str(line_blocks)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)
        
    def book_remove_indent(self, block_line_begin, block_line_end, ori_md5, new_md5, indent_space_number=4):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.remove_indent_space_in_file(file_name_in_book, block_line_begin, block_line_end, indent_space_number)
            commit_message = "Remove indent (%d space char) from line %d to line %d"%(indent_space_number, block_line_begin, block_line_end)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_rstrip_lines(self, line_numbers, ori_md5, new_md5):
        if isinstance(line_numbers, list) == False:
            line_numbers = [line_numbers]
        file_name_in_book = self._book_prepare()
        print(util.get_file_md5sum(file_name_in_book))
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            for single_line_num in line_numbers:
                util.rstrip_space_in_file(file_name_in_book, single_line_num)
            commit_message = "Remove white space at end of line %s" % str(line_numbers)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)
        
    def book_append_content(self, file_content, commit_message, ori_md5, new_md5):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.append_text_file(file_name_in_book, file_content)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def _book_prepare(self):
        os.chdir(self.current_working_dir)
        os.chdir(self.local_dir)
        assert(os.getcwd().endswith("book"))
        file_name_in_book = self.get_local_path_in_book()
        os.remove(file_name_in_book)
        util.print_run_cmd("git checkout %s" % file_name_in_book)
        print(util.get_file_md5sum(file_name_in_book))
        return file_name_in_book
    
    def _book_commit(self, file_name_in_book, commit_message, new_md5):
        util.run_deno_cmd("dos2unix " + file_name_in_book)
        util.print_run_cmd("git diff " + file_name_in_book)
        print(util.get_file_md5sum(file_name_in_book))
        assert(new_md5 == util.get_file_md5sum(file_name_in_book))
        util.print_run_cmd("git add " + file_name_in_book)
        util.print_run_cmd('git commit -m "%s"' % commit_message)
        
    def book_replace_lines(self, line_dict, commit_message, ori_md5, new_md5):
        line_numbers = line_dict.keys()
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            for single_line_num in line_numbers:
                util.replace_line_in_file(file_name_in_book, single_line_num, line_dict[single_line_num])            
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_add_line(self, line_num, file_content, commit_message, ori_md5, new_md5):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.add_line_in_file(file_name_in_book, line_num, file_content)
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)

    def book_replace_line(self, line_num, file_content, commit_message, ori_md5, new_md5):
        file_name_in_book = self._book_prepare()
        if (ori_md5 == util.get_file_md5sum(file_name_in_book)):
            util.replace_line_in_file(file_name_in_book, line_num, file_content)            
            self._book_commit(file_name_in_book, commit_message, new_md5)
        os.chdir(self.current_working_dir)
