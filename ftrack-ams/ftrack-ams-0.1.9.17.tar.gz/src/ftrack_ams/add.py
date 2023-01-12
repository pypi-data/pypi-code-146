import click

from ftrack_ams.functions import select_artist, shotnumber_to_letter


def add_images_to_existing_project(session, projnumber):
    print('🕰 Patience please while we crawl ftrack for ya....')
    projects = session.query("Project")
    users = session.query("User")

    existing_project = None
    existing_team = None
    projects = [p for p in projects if "invoice" not in p["name"]]
    for p in projects:
        for t in [x for x in p["children"] if "Projects" in x["name"]]:
            for o in t["children"]:
                if projnumber in o["name"]:
                    existing_project = o
                    existing_team = p
                    break
    project_team = []
    if existing_team is not None:
        for a in existing_team["allocations"]:
            resource = a["resource"]
            if isinstance(resource, session.types['User']):
                user = resource
                project_team.append(user)

    if existing_project is None:
        click.secho(
            f"🤯 {projnumber} does not exist ANYWHERE, please create it manually on ams.ftrack.com and run the script again", fg="yellow")
    else:
        print(f'🥳 Found {existing_project["name"]} in {existing_team["name"]}')

        if "Archive" in existing_project['parent']["name"]:
            print(
                f'So {existing_project["name"]} was found but it was archived, so we moved it to Projects')

            for ps in existing_team["children"]:
                if ps["name"] == "Projects":
                    existing_project["parent"] = ps
                    session.commit()

        task_templates = existing_project["parent"]["parent"]['project_schema']["task_templates"]

        for template in task_templates:
            if template["name"] == "Image_Template":
                image_template = template

        interior_shots = [i for i in existing_project['children'] if "INT" in i["name"]]
        num_exist_int = 0
        if interior_shots is not None and len(interior_shots) > 0:
            int_folder = interior_shots[0]
            num_exist_int = len(int_folder["children"])
            print(f'{existing_project["name"]} already has {num_exist_int} INT images')
        else:
            print(
                f"{existing_project['name']} has no INT images, let's create a folder for them!")
            int_folder = session.create(
                "Folder",
                {
                    "name": f"{projnumber}_INT",
                    "parent": existing_project
                })

        exterior_shots = [i for i in existing_project['children'] if "EXT" in i["name"]]
        num_existing_ext = 0
        if exterior_shots is not None and len(exterior_shots) > 0:
            ext_folder = exterior_shots[0]
            num_existing_ext = len(ext_folder["children"])
            print(
                f'{existing_project["name"]} already has {num_existing_ext} EXT images')
        else:
            print(
                f"{existing_project['name']} has no EXT images, let's create a folder for them!")
            ext_folder = session.create(
                "Folder",
                {
                    "name": f"{projnumber}_EXT",
                    "parent": existing_project
                })

        while True:
            try:
                additional_ints = int(input("Enter amount of additional INT shots: "))
            except ValueError:
                print("Sorry, I didn't understand that? Did you type a number?")
                continue
            else:
                print(f"Number of addtional INT:{additional_ints}")
                break

        if additional_ints > 0:
            if len(project_team) > 1:
                int_artist = select_artist(project_team, users, "Select INT artist")
            else:
                int_artist = project_team[0]

        while True:
            try:
                additional_exteriors = int(
                    input("Enter amount of additional EXT shots: "))
            except ValueError:
                print("Sorry, I didn't understand that? Did you type a number?")
                continue
            else:
                print(f"Number of addtional EXT:{additional_exteriors}")
                break

        if additional_exteriors > 0:
            if len(project_team) > 1:
                ext_artist = select_artist(project_team, users, "Select EXT artist")
            else:
                ext_artist = project_team[0]
        num_int = num_exist_int + additional_ints
        for i in range(num_exist_int, num_exist_int + additional_ints):
            shot = shotnumber_to_letter(i)
            print(f"📸 INT {shot} for {int_artist['username']}")
            int_shot_name = f"{projnumber}_INT_{shot}"
            int_shot = session.create("Image", {
                                      "name": int_shot_name,
                                      "parent": int_folder}
                                      )
            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create("Task", {
                                      "name": task_type["name"],
                                      "type": task_type,
                                      "parent": int_shot}
                                      )
                session.create("Appointment", {
                               "context": task,
                               "resource": int_artist,
                               "type": "assignment"}
                               )
        num_ext = num_existing_ext + additional_exteriors
        for i in range(num_existing_ext, num_existing_ext + additional_exteriors):
            shot = shotnumber_to_letter(i)
            print(f"📸 EXT {shot} for {ext_artist['username']}")
            ext_shot_name = f"{projnumber}_EXT_{shot}"

            ext_shot = session.create("Image", {
                                      "name": ext_shot_name,
                                      "parent": ext_folder}
                                      )
            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create("Task", {
                                      "name": task_type["name"],
                                      "type": task_type,
                                      "parent": ext_shot}
                                      )
                session.create("Appointment", {
                               "context": task,
                               "resource": ext_artist,
                               "type": "assignment"}
                               )

        if num_int == 0:
            desc = f"{num_ext} EXT"
        elif num_ext == 0:
            desc = f"{num_int} INT"
        else:
            desc = f"{num_int} INT/{num_ext} EXT"

        existing_project["description"] = desc

        session.commit()
