
import os
import subprocess


PATH_PYTHON_SCRIPTS = u"E:/Python275/Scripts"

PATH_PEP8_CONFIG = u"../lukas_config.pep8"
PATH_PYFLAKES_CONFIG = u""
PATH_PYLINT_CONFIG = u"../pylint_rcfile.txt"

PATH_GIT = "C:/git/Git/bin/git.exe"
BRANCH_NAME = "fix_112"
REPO_URL = "https://github.com/pyjosh/repo.git"

def run_subprocess(subprocess_args, return_output=None):
    p = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print out
    if return_output:
        return out



def main():

    repository_name = os.path.basename(REPO_URL).split(".")[0]

    if os.path.isdir(repository_name):
        os.chdir(repository_name)
        run_subprocess([PATH_GIT, "checkout", "master"])
        run_subprocess([PATH_GIT, "pull", REPO_URL])
    else:
        run_subprocess([PATH_GIT, "clone", REPO_URL])
        os.chdir(repository_name)

    # switch to branch from pull request
    run_subprocess([PATH_GIT, "checkout", BRANCH_NAME])

    out = run_subprocess([PATH_GIT, "diff", "--name-only", "master", BRANCH_NAME], True)
    files_modified_in_pull_request = []
    for i in out.split():
        if i.endswith(".py"):
            print i
            files_modified_in_pull_request.append(i)

    raw_input()


    pep8_path       = os.path.join(PATH_PYTHON_SCRIPTS, "pep8.exe")
    pyflakes_path   = os.path.join(PATH_PYTHON_SCRIPTS, "pyflakes.exe")
    pylint_path     = os.path.join(PATH_PYTHON_SCRIPTS, "pylint.exe")

    for file_to_review in files_modified_in_pull_request:
        print "{0}\n{1}\n{0}".format("=" * 80, "review: " + file_to_review )

        # PEP 8
        print "{0}\n{1}\n{0}".format("-" * 80, "PEP8" )
        run_subprocess([pep8_path, "--config=" + PATH_PEP8_CONFIG, file_to_review])

        # PYFLAKES
        print "{0}\n{1}\n{0}".format("-" * 80, "PYFLAKES" )
        run_subprocess([pyflakes_path, file_to_review])

        # PYLINT
        print "{0}\n{1}\n{0}".format("-" * 80, "PYLINT" )
        run_subprocess([pylint_path, "--rcfile=" + PATH_PYLINT_CONFIG, file_to_review])

        raw_input()



if __name__ == "__main__":
    main()
