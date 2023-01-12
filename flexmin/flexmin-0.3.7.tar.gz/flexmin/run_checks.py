checks = {
          'all_of_executables': ['nginx','uwsgi'],
          'all_of_files': ['/etc/flexmin/flexmin.conf','/etc/flexmin/menu.yaml'],
          'all_of_folders': ['/etc/flexmin','/home/flexmin'],
          'all_of_users': ['flexmin'],
          'error_threshold': {5: "Please make sure you have run 'flexmin install'"}
         }
