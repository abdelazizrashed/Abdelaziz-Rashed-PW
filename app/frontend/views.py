import requests
import jinja2
import os
from flask import render_template, Blueprint, request, current_app as app, request
import json

main = Blueprint("main", __name__)

loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))

enviroment = jinja2.Environment(loader=loader)


nav = [
    {"name": "Home", "url": "/"},
    {"name": "Projects", "url": "/projects"},
    {"name": "Services", "url": "/services"},
    {"name": "Contact", "url": "/contact"},
    # {"name": "Resume", "url": "/resume"},
    # {"name": "Certificates", "url": "/certificates"},
    {"name": "About", "url": "/about"},
]

# url = "http://api.localhost:5000/info"
# content = requests.get(url)
# print(content)


# def generate_nav(json: dict):
#     nav = []
#     if json.get("home"):
#         nav.append({"name": "Home", "url": "/"})
#     if json.get("projects"):
#         nav.append({"name": "Projects", "url": "/projects"})
#     if json.get("services"):
#         nav.append({"name": "Services", "url": "/services"})
#     if json.get("contact"):
#         nav.append({"name": "Contact", "url": "/contact"})
#     if json.get("resume"):
#         nav.append({"name": "Resume", "url": "/resume"})
#     if json.get("certificates"):
#         nav.append({"name": "Certificates", "url": "/certificates"})
#     if json.get("about"):
#         nav.append({"name": "About", "url": "/about"})

#     return nav


@main.route("/")
def home():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()
    # # print(info)
    # print(json.dumps(info))
    # # print(info.get("navbarPages"))
    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    
    return render_template(
        "./index.html",
        # nav=json.dumps(nav),
        title="Abdelaziz Rashed Personal Website",
        current_url="/",
        apiUrl=request.url.removesuffix(request.path) + "/api-v1",
        description="Abdelaziz Rashed is a software developer with wide skill set and experience in Web Development, Cross-platform App Development and Game Development.",
        # info=json.dumps(info),
    )


@main.route("/projects")
def projects():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="Projects",
        current_url="/projects",
        description="Projects that Abdelaziz Rashed worked on in the past.",
        # info=json.dumps(info),
    )


@main.route("/services")
def services():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="Services",
        current_url="/services",
        description="Services that Abdelaziz Rashed provide.",
        # info=json.dumps(info),
    )


@main.route("/contact")
def contact():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="Contact Abdelaziz Rashed",
        current_url="/contact",
        description="Ways you can contact Abdelaziz Rashed for future work.",
        # info=json.dumps(info),
    )


@main.route("/resume")
def resume():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="Abdelaziz Rashed's resume",
        current_url="/resume",
        description="The resume of Abdelaziz Rashed",
        # info=json.dumps(info),
    )


@main.route("/certificates")
def certificates():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="Abdelaziz Rashed's certificates",
        current_url="/certificates",
        description="Certificates that Abdelaziz Rashed acquired through his career.",
        # info=json.dumps(info),
    )


@main.route("/about")
def about():
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title="About Abdelaziz Rashed",
        current_url="/about",
        description="Learn more about Abdelaziz Rashed and know who he is.",
        # info=json.dumps(info),
    )


@main.route("/project")
def project():
    """
    request formate /project?id=1&name=new-project
    """
    # print("recieved request at /project")
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # print("1")
    # # response = requests.get(info_url)
    # print("2")
    # # info = response.json()
    # # print("sent request to /api/info and recieved response")
    # # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # # else:nav = generate_nav(info.get("navbarPages"))
    project_id = request.args.get("id", default=1, type=int)
    project_name = request.args.get("name", default="", type=str)
    # print("generated  nav items and feteched req params")
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title=project_name,
        current_url="/project",
        description="Information about the project "
        + project_name
        + " that Abdelziz Rashed worked on.",
        # info=json.dumps(info),
    )


@main.route("/service")
def service():
    """
    request formate /service?id=1&name=new-service
    """
    print("recieved request at /service")
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    service_id = request.args.get("id", default=1, type=int)
    service_name = request.args.get("name", default="", type=str)
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title=service_name,
        current_url="/service",
        description="Information about the service "
        + service_name
        + " that Abdelziz Rashed provide.",
        # info=json.dumps(info),
    )


@main.route("/certificate")
def certificate():
    """
    request formate /certifcate?id=1&name=new-certificate
    """
    # info_url = request.url.removesuffix(request.path) + "/api/info"
    # response = requests.get(info_url)
    # info = response.json()

    # if isinstance(info.get("navbarPages"), list):nav = generate_nav(info.get("navbarPages")[0])
    # else:nav = generate_nav(info.get("navbarPages"))
    certificate_id = request.args.get("id", default=1, type=int)
    certificate_name = request.args.get("name", default="", type=str)
    return render_template(
        "index.html",
        # nav=json.dumps(nav),
        title=certificate_name,
        current_url="/certificate",
        description="Information about the certificate "
        + certificate_name
        + " that Abdelziz acquired.",
        # info=json.dumps(info),
    )
