import click
from pick import pick

from ftrack_ams.fileserver import create_project_on_fileserver, get_deal_info, get_latest_proj
from ftrack_ams.functions import clearConsole, get_int_from_user, select_artist
from ftrack_ams.functions import create_project_name, get_yes_no


def create_new_project(session):

    continue_project_creation = get_yes_no(
        "Are you sure you want to create a new project? 🕵️‍♂️"
    )

    if not continue_project_creation:
        print("Ok bye 👋")
        quit()

    projects = session.query("Project")
    users = session.query("User")
    client = None
    projname = None

    logo_handle = session.query('Folder where name is "AMSVFB_Logo"').one()

    for logo in logo_handle["children"]:
        if logo["name"] == "VFB-LOGO":
            vfb_thumb = logo["thumbnail_id"]
        if logo["name"] == "AMSVFB-LOGO":
            amsvfb_thumb = logo["thumbnail_id"]
        if logo["name"] == "AMS-LOGO":
            ams_thumb = logo["thumbnail_id"]

    clearConsole()
    num = None
    dealnumber = None
    deal = None
    if get_yes_no("Do you have a deal number?"):
        while True:
            dealnumber = input("👀 Enter deal number: ")
            try:
                int(dealnumber)
            except ValueError:
                print("🤯 Sorry, I didn't understand that? Did you type a number?")
                continue
            else:
                if len(dealnumber) == 4:
                    click.secho(
                        f"Looks like {dealnumber} already existing, try adding to this project instead of creating a new one", fg="yellow")
                    input("press enter to re-run")
                    quit()
                if len(dealnumber) == 3:
                    click.secho("nieuw project op basis van een deal, cool story brah")
                    break
                else:
                    click.secho("🤯 Try typing 3 or 4 numbers", fg="red")
                    continue

    if dealnumber is not None:
        deal = get_deal_info(dealnumber)
        if deal is not None:
            split = deal.split('_')
            client = split[3]
            projname = split[4]

    print(f"👍 Ok {session.api_user}, which team are we making a project for?")

    option, index = pick(
        sorted([p["name"] for p in projects if "invoice" not in p["name"]]),
        "👬 Select the team:",
        indicator="👉",
    )

    clearConsole()

    num = get_latest_proj()
    if get_yes_no(f"🤹‍♂️ Based on the latest X: project, your project number is {num}, u like?"):
        print(f"🤩 Ok, we're rolling with {num}")
    else:
        while True:
            raw_input = input("😮 Ok, enter desired project number: ")
            try:
                int(raw_input)
            except ValueError:
                print("Sorry, I didn't understand that? Did you type a number?")
                continue
            else:
                if len(raw_input) != 4:
                    click.secho("🤯 Try typing 4 numbers", fg="red")
                    continue
                num = raw_input
                break

    team = [t for t in projects if option.lower() == t["name"].lower()][0]
    print(f"💁‍♂️ Making a new project for {team['name']}")

    mgmt = []
    for m in team["managers"]:
        if "Annelies" not in m["user"]["username"]:
            mgmt.append(m["user"])
        else:
            annelies = m["user"]

    project_team = []

    for a in team["allocations"]:
        resource = a["resource"]
        if isinstance(resource, session.types["User"]):
            user = resource
            project_team.append(user)

    internal_project = True if "Intern" in team["name"] else False

    if internal_project:
        departement_choice, departement_index = pick(
            ["AMS", "VFB"], "Select internal department:"
        )

    project_thumb = amsvfb_thumb

    if internal_project and departement_choice == "AMS":
        project_thumb = ams_thumb

    if internal_project and departement_choice == "VFB":
        project_thumb = vfb_thumb

    dest_folder = None
    for child in team["children"]:
        if child["name"] == "Projects":
            dest_folder = child

    if dest_folder is None:
        click.secho(
            f"could not find a 'Projects' folder for team {team['name']}", fg="red")
        quit()
    if client is None:
        while True:
            client = input("Enter client letter code (3 characters):")
            if len(client) == 3:
                print(f"making project number {num} for client {client}")
                break
            else:
                print("didnt get ya fully")
                continue
    if projname is None:
        while True:
            projname = input("Enter project letter code (3 characters):")
            if len(projname) == 3:
                break
            else:
                print("Didnt get ya fully? Type three characters.")
                continue

    project_name = create_project_name(num, client, projname)

    num_int = get_int_from_user("Enter amount of INT shots: ")
    num_ext = get_int_from_user("Enter amount of EXT shots: ")
    num_moving = get_int_from_user("Enter amount of MOVING IMAGES: ")

    if num_int == 0:
        desc = f"{num_ext} EXT"
    elif num_ext == 0:
        desc = f"{num_int} INT"
    else:
        desc = f"{num_int} INT/{num_ext} EXT"

    if internal_project and departement_choice == "VFB":
        proj = session.create(
            "Vfbproj",
            {
                "name": project_name,
                "parent": dest_folder,
                "description": desc,
                "thumbnail_id": project_thumb,
            },
        )
    else:
        proj = session.create(
            "Amsproj",
            {
                "name": project_name,
                "parent": dest_folder,
                "description": desc,
                "thumbnail_id": project_thumb,
            },
        )

    task_templates = team["project_schema"]["task_templates"]

    for template in task_templates:
        if template["name"] == "Annelies_Template":
            annelies_template = template
        if template["name"] == "Image_Template":
            image_template = template
        if template["name"] == "PM_Template":
            production_template = template
        if template["name"] == "Timetracking_Template":
            timetrack_template = template
        if template["name"] == "MovingImage_Template":
            moving_image_template = template

    pm_choice, index = pick([m["username"] for m in mgmt], "👩‍🏫 Select project manager")
    project_manager = mgmt[index]

    for task_type in [t["task_type"] for t in production_template["items"]]:
        task = session.create(
            "Task",
            {
                "name": task_type["name"],
                "type": task_type,
                "thumbnail_id": project_thumb,
                "parent": proj,
            },
        )
        session.create(
            "Appointment",
            {"context": task, "resource": project_manager, "type": "assignment"},
        )

    for task_type in [t["task_type"] for t in annelies_template["items"]]:
        task = session.create(
            "Task",
            {
                "name": task_type["name"],
                "type": task_type,
                "thumbnail_id": project_thumb,
                "parent": proj,
            },
        )

        session.create(
            "Appointment", {"context": task, "resource": annelies, "type": "assignment"}
        )

    if num_int > 0:
        int_folder = session.create(
            "Folder",
            {"name": f"{num}_INT",
             "parent": proj,
             "thumbnail_id": project_thumb}
        )

        if len(project_team) > 1:
            int_artist = select_artist(project_team, users, "👩‍🎨🛋 Select INT artist: ")
        else:
            int_artist = project_team[0]

        for i in range(num_int):
            int_shot_name = f"{num}_INT_{chr(ord('@')+i+1)}"

            int_shot = session.create(
                "Image",
                {
                    "name": int_shot_name,
                    "parent": int_folder,
                    "thumbnail_id": project_thumb,
                },
            )

            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create(
                    "Task",
                    {
                        "name": task_type["name"],
                        "type": task_type,
                        "parent": int_shot,
                        "thumbnail_id": project_thumb,
                    },
                )
                session.create(
                    "Appointment",
                    {"context": task, "resource": int_artist, "type": "assignment"},
                )

    if num_ext > 0:
        ext_folder = session.create(
            "Folder",
            {"name": f"{num}_EXT", "parent": proj, "thumbnail_id": project_thumb},
        )

        if len(project_team) > 1:
            ext_artist = select_artist(project_team, users, "👨‍🎨🏞 Select EXT artist: ")
        else:
            ext_artist = project_team[0]

        for i in range(num_ext):
            ext_shot_name = f"{num}_EXT_{chr(ord('@')+i+1)}"
            ext_shot = session.create(
                "Image",
                {
                    "name": ext_shot_name,
                    "parent": ext_folder,
                    "thumbnail_id": project_thumb,
                },
            )
            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create(
                    "Task",
                    {
                        "name": task_type["name"],
                        "type": task_type,
                        "parent": ext_shot,
                        "thumbnail_id": project_thumb,
                    },
                )
                session.create(
                    "Appointment",
                    {"context": task, "resource": ext_artist, "type": "assignment"},
                )

    if num_moving > 0:
        moving_image_folder = session.create(
            "Folder",
            {"name": f"{num}_MovingImage", "parent": proj,
             "thumbnail_id": project_thumb},
        )

        if len(project_team) > 1:
            movingImage_artist = select_artist(
                project_team, users, "👨‍🎨🏞 Select MovingImage artist: ")
        else:
            movingImage_artist = project_team[0]

        for i in range(num_moving):
            moving_image_name = f"{num}_MovingImage_{chr(ord('@')+i+1)}"
            moving_image_shot = session.create(
                "MovingImage",
                {
                    "name": moving_image_name,
                    "parent": moving_image_folder,
                    "thumbnail_id": project_thumb,
                },
            )
            for task_type in [t["task_type"] for t in moving_image_template["items"]]:
                task = session.create(
                    "Task",
                    {
                        "name": task_type["name"],
                        "type": task_type,
                        "parent": moving_image_shot,
                        "thumbnail_id": project_thumb,
                    },
                )
                session.create(
                    "Appointment",
                    {"context": task, "resource": moving_image_shot, "type": "assignment"},
                )

    # using a set here to make sure users aren't added multiple times
    project_set = set()
    if num_int > 0:
        project_set.add(int_artist)
    if num_ext > 0:
        project_set.add(ext_artist)

    if internal_project:
        for artist in project_set:
            for task_type in [t["task_type"] for t in timetrack_template["items"]]:
                task = session.create(
                    "Task",
                    {
                        "name": f"TT_{artist['first_name']}",
                        "type": task_type,
                        "thumbnail_id": project_thumb,
                        "parent": proj,
                    },
                )
                session.create(
                    "Appointment",
                    {
                        "context": task,
                        "resource": artist,
                        "type": "assignment",
                    },
                )

    drone = get_yes_no("📸 Does the project require photography?")

    session.commit()

    print(f"✅ Succesfully created {project_name} for {team['name']}")
    if deal is not None:
        print(f"Based on deal {deal}")
    print(f"--- creating objects for {project_name} on ftrack")
    # print(f"--- creating outlook folder for {project_name}")
    print(f"--- creating directory for {project_name} on X:/")
    create_project_on_fileserver(project_name, internal_project, deal)
    print(
        f"-- {num_int} INT tasks for {int_artist['username']}"
    ) if num_int > 0 else None
    print(
        f"-- {num_ext} EXT tasks for {ext_artist['username']}"
    ) if num_ext > 0 else None
    print(
        f"-- {num_moving} EXT tasks for {movingImage_artist['username']}"
    ) if num_moving > 0 else None
    print("--- creating photography tasks") if drone else None
    print(f"--- creating {project_name}.mxp for 3dsmax project")
    print(f"--- updating {project_name} on teamleader")
