# https://www.cnblogs.com/superbaby11/p/15560994.html
from threading import Thread


def run_cmd(cmd):
    """Run shell command and return command output.

    Examples:
        >>> run_cmd("cd ..")
        ''

    Args:
        cmd (string): A shell command.

    Returns:
        string: Command output.
    """
    import subprocess

    return subprocess.getoutput(cmd)


def run_deno_cmd(cmd):
    from pathlib import Path

    return run_cmd(str(Path.home()) + "/.deno/bin/" + cmd)


def print_run_cmd(cmd):
    import subprocess

    # http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html
    p = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
    )
    stdout_buffer = []
    while True:
        line = p.stdout.readline()
        stdout_buffer.append(line)
        print(line, end="")
        if line == "" and p.poll() != None:
            break
    return "".join(stdout_buffer)


def create_text_file(file_name, file_content):
    with open(file_name, "w") as file:
        file.write(file_content)


# https://www.jb51.net/article/232129.htm
class MyThread(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None
    ):
        super().__init__()
        self.fun = target
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.fun(*self.args, **self.kwargs)


def thread_run_cmd(cmd):
    t = MyThread(target=run_cmd, args=(cmd,), kwargs={})
    t.start()
    # t.join()


def thread_run_deno_cmd(cmd):
    t = MyThread(target=run_deno_cmd, args=(cmd,), kwargs={})
    t.start()
    # t.join()


def get_page_content(url):
    # https://www.cnblogs.com/herbert/p/10789343.html
    # https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/#tabs-1-1
    from selenium import webdriver
    import time
    import os

    # https://blog.csdn.net/ad72182009/article/details/116117744
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub", options=chrome_options
    )
    driver.get(url=url)
    # Wait some time for page loading
    time.sleep(4)
    found_page_source = driver.page_source
    driver.close()
    return found_page_source


def display_code(content):
    from IPython.display import Code

    return Code(data=content)


def display_iframe(url):
    from IPython.display import IFrame

    return IFrame(src=url, width="100%", height=300)


def get_file_md5sum(file):
    import hashlib
    import os

    if not os.path.exists(file):
        return "md5sum: {}: No such file or directory".format(file)
    elif os.path.isdir(file):
        return "md5sum: {}: Is a directory".format(file)
    elif os.path.isfile(file):
        with open(file, "rb") as fd:
            data = fd.read()
        # return "{}  {}".format(hashlib.md5(data).hexdigest(), file)
        return hashlib.md5(data).hexdigest()
    else:
        return "md5sum: {}: Unexpected error".format(file)


def get_str_md5sum(content):
    import hashlib

    return hashlib.md5(content.encode("utf8")).hexdigest()


def append_text_file(file_name, file_content):
    with open(file_name, "a") as file:
        file.write(file_content)


def replace_line_in_file(file_path, old_line_number, new_line_content):
    import fileinput

    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if line_number == old_line_number:
                print(new_line_content, end="")
            else:
                print(line, end="")


def insert_line_at_top_of_file(file_path, new_line_content, new_line_content_end="\n"):
    import fileinput

    flag_inserted = False
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            if flag_inserted == False:
                print(new_line_content, end=new_line_content_end)
                flag_inserted = True
            print(line, end="")


def add_line_in_file(
    file_path, old_line_number, new_line_content, new_line_content_end="\n"
):
    import fileinput

    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if line_number == old_line_number:
                print(new_line_content, end=new_line_content_end)
            print(line, end="")


def del_line_in_file(file_path, old_line_number):
    import fileinput

    deleted_line = ""
    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if line_number == old_line_number:
                deleted_line = line
            else:
                print(line, end="")
    return deleted_line


def del_line_block_in_file(file_path, old_line_number_begin, old_line_number_end):
    import fileinput

    deleted_line = ""
    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if old_line_number_begin == line_number:
                deleted_line = line
            else:
                if (
                    old_line_number_begin < line_number
                    and line_number <= old_line_number_end
                ):
                    deleted_line = deleted_line + line
                else:
                    print(line, end="")
    return deleted_line


def move_line_in_file(file_path, old_line_number, new_line_number):
    if old_line_number <= new_line_number and new_line_number <= (old_line_number + 1):
        return ""
    else:
        new_line_content = del_line_in_file(file_path, old_line_number)
        if old_line_number > new_line_number:
            add_line_in_file(file_path, new_line_number, new_line_content, "")
        else:
            add_line_in_file(file_path, new_line_number - 1, new_line_content, "")


def move_line_block_in_file(
    file_path, old_line_number_begin, old_line_number_end, new_line_number
):
    if old_line_number_begin <= new_line_number and new_line_number <= (
        old_line_number_end + 1
    ):
        return
    else:
        new_line_content = del_line_block_in_file(
            file_path, old_line_number_begin, old_line_number_end
        )
        if old_line_number_begin > new_line_number:
            add_line_in_file(file_path, new_line_number, new_line_content, "")
        else:
            add_line_in_file(
                file_path,
                new_line_number - (old_line_number_end - old_line_number_begin + 1),
                new_line_content,
                "",
            )


def read_text_file(file_path):
    from pathlib import Path

    return Path(file_path).read_text()


def display_text(content):
    from IPython.display import Code

    return Code(data=content, language="text")


def remove_indent_space_in_file(
    file_path, block_line_begin, block_line_end, indent_space_number
):
    import fileinput

    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if line_number >= block_line_begin and line_number <= block_line_end:
                if len(line) < indent_space_number:
                    print(line, end="")
                else:
                    new_line_content = line[indent_space_number:]
                    print(new_line_content, end="")
            else:
                print(line, end="")


def rstrip_space_in_file(file_path, line_number):
    import fileinput

    cur_line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            cur_line_number = cur_line_number + 1
            if line_number == cur_line_number:
                print(line.rstrip() + "\n", end="")
            else:
                print(line, end="")


def display_image(img_file):
    from IPython.display import Image

    return Image(img_file)


def del_block_in_file(file_path, block_line_begin, block_line_end):
    import fileinput

    line_number = 0
    with fileinput.FileInput(file_path, inplace=True) as f:
        for line in f:
            line_number = line_number + 1
            if line_number >= block_line_begin and line_number <= block_line_end:
                pass
            else:
                print(line, end="")


def full_page_snapshot(url, dir_snapshot):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    import os

    assert os.path.isdir(dir_snapshot)
    if "http_proxy" in os.environ:
        del os.environ["http_proxy"]
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor="http://127.0.0.1:4444/wd/hub", options=chrome_options
    )
    driver.maximize_window()
    driver.get(url=url)
    # Wait some time for page loading
    time.sleep(4)
    found_page_source = driver.page_source
    try:
        span_collapse = driver.find_element(by=By.XPATH, value='//span[text()="«"]')
        span_collapse.click()
    except Exception as e:
        print(e)
    driver.save_screenshot(dir_snapshot + os.path.sep + "screenshot.png")

    main_scroll_height = 0
    main_scroll_top = 0
    page_height = 0
    flag_main_element = False
    try:
        main_scroll_height = driver.execute_script(
            "return document.getElementById('MAIN').scrollHeight"
        )
        main_scroll_top = driver.execute_script(
            "return document.getElementById('MAIN').scrollTop"
        )
        page_height = driver.execute_script("return document.body.scrollHeight")
        flag_main_element = True
    except Exception as e:
        print(e)
        main_scroll_height = driver.execute_script(
            "return document.body.parentNode.scrollHeight"
        )
        main_scroll_top = driver.execute_script(
            "return document.body.parentNode.scrollTop"
        )
        page_height = driver.execute_script("return window.innerHeight")

    print(
        "main_scroll_height is %d main_scroll_top is %d page_height is %d"
        % (main_scroll_height, main_scroll_top, page_height)
    )
    while True:
        driver.execute_script("window.scrollBy(0, %d);" % page_height)
        time.sleep(1)
        if flag_main_element:
            new_main_scroll_height = driver.execute_script(
                "return document.getElementById('MAIN').scrollHeight"
            )
        else:
            new_main_scroll_height = driver.execute_script(
                "return document.body.parentNode.scrollHeight"
            )
        if new_main_scroll_height == main_scroll_height:
            break
        main_scroll_height = new_main_scroll_height
        print("main_scroll_height is %d" % main_scroll_height)

    driver.execute_script("window.scrollTo(0, 0);")
    page_index = 1
    driver.save_screenshot(dir_snapshot + os.path.sep + ("page_%06d.png" % page_index))

    if flag_main_element:
        main_scroll_height = driver.execute_script(
            "return document.getElementById('MAIN').scrollHeight"
        )
        page_height = driver.execute_script("return document.body.scrollHeight")
    else:
        main_scroll_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )
        page_height = driver.execute_script("return window.innerHeight")

    window_page_y_offset = driver.execute_script("return window.pageYOffset")
    print(
        "page_index is %d window_page_y_offset is %d main_scroll_height is %d page_height is %d"
        % (page_index, window_page_y_offset, main_scroll_height, page_height)
    )

    while (window_page_y_offset + page_height < main_scroll_height) and (
        page_index < 100
    ):
        driver.execute_script("window.scrollBy(0, %d);" % page_height)
        page_index = page_index + 1
        driver.save_screenshot(
            dir_snapshot + os.path.sep + ("page_%06d.png" % page_index)
        )
        window_page_y_offset = driver.execute_script("return window.pageYOffset")
        print(
            "page_index is %d window_page_y_offset is %d main_scroll_height is %d page_height is %d"
            % (page_index, window_page_y_offset, main_scroll_height, page_height)
        )
    assert page_index < 100
    driver.save_screenshot(dir_snapshot + os.path.sep + "screenshot_last_page.png")
    driver.close()
    return page_index
